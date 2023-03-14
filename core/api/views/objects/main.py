import os

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from django.http import Http404
from django.urls import reverse
from rest_framework import generics, permissions
from rest_framework.response import Response

from .base import BaseProvider
from ...utils import GenericAPIViewWithDebugInfo, GenericAPIViewWithLastModified

__all__ = ["ObjectList", "ObjectSingle", "ObjectRetrieve", "ObjectNew"]


def gen_get_provider(mapping):
    for file in os.listdir(os.path.dirname(__file__)):
        if file.endswith(".py") and file not in ["__init__.py", "base.py", "main.py"]:
            __import__(f"core.api.views.objects.{file[:-3]}", fromlist=["*"])

    provClasses = BaseProvider.__subclasses__()
    try:
        ProvReqNames = [
            mapping[cls.__name__.rsplit("Provider")[0].lower()] for cls in provClasses
        ]
    except KeyError as e:
        raise NotImplementedError(
            f"Provider class {e} is missing a request name. Please add it to the mapping."
        ) from e
    provClassMapping = {key: value for key, value in zip(ProvReqNames, provClasses)}

    def get_provider(provider_name: str):
        """
        Gets a provider by type name.
        """
        # TODO; return an exception to automatically return 400
        if provider_name not in ProvReqNames:
            raise Http404(
                "Invalid object type. Valid types are: " + ", ".join(ProvReqNames) + "."
            )
        return provClassMapping[provider_name]

    return get_provider


get_provider = gen_get_provider(  # k = Provider class name e.g. comment in CommentProvider, v = request name
    {
        "announcement": "announcement",
        "blogpost": "blog-post",
        "event": "event",
        "organization": "organization",
        "flatpage": "flatpage",
        "user": "user",
        "tag": "tag",
        "comment": "comment",
        "like": "like",
    }
)


class ObjectAPIView(generics.GenericAPIView):
    def get_as_su(self):
        return self.as_su

    def initial(self, *args, **kwargs):
        super().initial(*args, **kwargs)
        self.request.mutate = self.mutate
        self.request.kind = self.kind
        self.request.detail = self.detail
        self.provider = provider = get_provider(kwargs.pop("type"))(self.request)
        if as_su := (self.request.GET.get("as-su") == "true"):
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = provider.permission_classes
        self.as_su = as_su
        self.serializer_class = provider.serializer_class
        # NOTE: better to have the following if after initial, but this is easier

    # NOTE: dispatch() is copied from https://github.com/encode/django-rest-framework/blob/de7468d0b4c48007aed734fee22db0b79b22e70b/rest_framework/views.py
    # License for this function:
    #
    # Copyright © 2011-present, [Encode OSS Ltd](https://www.encode.io/).
    # All rights reserved.
    #
    # Redistribution and use in source and binary forms, with or without
    # modification, are permitted provided that the following conditions are met:
    #
    # * Redistributions of source code must retain the above copyright notice, this
    #   list of conditions and the following disclaimer.
    #
    # * Redistributions in binary form must reproduce the above copyright notice,
    #   this list of conditions and the following disclaimer in the documentation
    #   and/or other materials provided with the distribution.
    #
    # * Neither the name of the copyright holder nor the names of its
    #   contributors may be used to endorse or promote products derived from
    #   this software without specific prior written permission.
    #
    # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    # ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    # WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    # DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    # FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    # DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    # SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    # CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    # OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    # OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    # Note: Views are made CSRF exempt from within `as_view` as to prevent
    # accidental removal of this exemption in cases where `dispatch` needs to
    # be overridden.
    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(
                    self, request.method.lower(), self.http_method_not_allowed
                )
            else:
                handler = self.http_method_not_allowed

            kwargs.pop("type")
            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response


class ObjectList(
    GenericAPIViewWithLastModified,
    GenericAPIViewWithDebugInfo,
    ObjectAPIView,
    generics.ListAPIView,
):
    mutate = False
    detail = False
    kind = "list"

    def get_last_modified(self):
        try:
            return self.provider.get_last_modified_queryset()
        except ObjectDoesNotExist:
            return None

    def get_admin_url(self):
        model: Model = self.provider.model
        return reverse(
            f"admin:{model._meta.app_label}_{model._meta.model_name}_changelist"
        )

    def get_queryset(self):
        return self.provider.get_queryset(self.request)

    def get(self, *args, **kwargs):
        if not self.provider.allow_list:
            return Response({"detail": "listing not allowed"}, status=422)
        return super().get(*args, **kwargs)


class LookupField:
    @property
    def lookup_field(self):
        if hasattr(self.provider, "lookup_field"):
            return self.provider.lookup_field
        return "id"

    lookup_url_kwarg = "id"


class ObjectNew(ObjectAPIView, LookupField, generics.CreateAPIView):
    mutate = True
    detail = None
    kind = "new"

    def get_queryset(self):
        return self.provider.get_queryset(self.request)

    def post(self, *args, **kwargs):
        if not self.provider.allow_new:
            return Response({"detail": "creating not allowed"}, status=422)
        return super().post(*args, **kwargs)


class ObjectRetrieve(
    ObjectAPIView,
    LookupField,
    generics.RetrieveAPIView,
    GenericAPIViewWithDebugInfo,
    GenericAPIViewWithLastModified,
):
    mutate = False
    detail = True
    kind = "retrieve"

    def get_admin_url(self):
        model = self.provider.model
        return reverse(
            f"admin:{model._meta.app_label}_{model._meta.model_name}_change",
            args=[self.get_object().id],
        )

    def get_last_modified(self):
        try:
            return self.provider.get_last_modified(self)
        except ObjectDoesNotExist:
            return None

    def get_queryset(self):
        return self.provider.get_queryset(self.request)


class ObjectSingle(
    ObjectAPIView, LookupField, generics.DestroyAPIView, generics.UpdateAPIView
):
    mutate = True
    detail = None
    kind = "single"

    def get_admin_url(self):
        model = self.provider.model
        return reverse(
            f"admin:{model._meta.app_label}_{model._meta.model_name}_change",
            args=[self.get_object().id],
        )

    def get_queryset(self):
        return self.provider.get_queryset(self.request)
