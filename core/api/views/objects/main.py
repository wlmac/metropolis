import importlib

from django.http import Http404
from django.urls import reverse
from rest_framework import generics
from rest_framework.response import Response

from ...utils import ListAPIViewWithFallback, GenericAPIViewWithLastModified, GenericAPIViewWithDebugInfo

__ALL__ = ["ObjectList", "ObjectSingle", "ObjectRetrieve", "ObjectNew"]


def gen_get_provider(mapping):
    providers = {
        key: importlib.import_module(f".{value}", "core.api.views.objects").Provider
        for key, value in mapping.items()
    }

    def get_provider(provider_name: str):
        """
        Gets a provider by type name.
        """
        # TODO; return an exception to automatically return 400
        if provider_name not in providers:
            raise Http404("確り取説読んだ？")
        return providers[provider_name]

    return get_provider


get_provider = gen_get_provider({
    "announcement": "announcement",
    "blog-post": "blog_post",
    "event": "event",
    "organization": "organization",
    "flatpage": "flatpage",
    "user": "user",
    "tag": "tag",
})


class ObjectAPIView(generics.GenericAPIView):
    def initial(self, *args, **kwargs):
        super().initial(*args, **kwargs)
        self.request.mutate = self.mutate  # fixme self.mutate and self.detail do not exist
        self.request.detail = self.detail
        self.provider = provider = get_provider(kwargs.pop("type"))(self.request)
        self.permission_classes = provider.permission_classes
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
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            kwargs.pop("type")
            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response


class ObjectList(ObjectAPIView, ListAPIViewWithFallback, GenericAPIViewWithDebugInfo, GenericAPIViewWithLastModified):
    mutate = False
    detail = False

    def get_last_modified(self):
        return self.provider.get_last_modified_queryset()

    def get_admin_url(self):
        model = self.provider.model
        return reverse(f"admin:{model._meta.app_label}_{model._meta.model_name}_changelist")

    def get_queryset(self):
        return self.provider.get_queryset(self.request)

    def get(self, *args, **kwargs):
        if not self.provider.allow_list:
            return Response({'detail': 'listing not allowed'}, status=422)
        return super().get(*args, **kwargs)


class LookupField:
    @property
    def lookup_field(self):
        if hasattr(self.provider,
                   'lookup_field'):  # fixme self.provider does not exist here you might have intended to subclass ObjectAPIView
            return self.provider.lookup_field
        return 'id'

    lookup_url_kwarg = "id"


class ObjectNew(ObjectAPIView, LookupField, generics.CreateAPIView):
    mutate = True
    detail = None

    def get_queryset(self):
        return self.provider.get_queryset(self.request)


class ObjectRetrieve(ObjectAPIView, LookupField, generics.RetrieveAPIView, GenericAPIViewWithDebugInfo,
                     GenericAPIViewWithLastModified):
    mutate = False
    detail = True

    def get_admin_url(self):
        model = self.provider.model
        return reverse(f"admin:{model._meta.app_label}_{model._meta.model_name}_change", args=[self.get_object().id])

    def get_last_modified(self):
        return self.provider.get_last_modified(self)

    def get_queryset(self):
        return self.provider.get_queryset(self.request)


class ObjectSingle(ObjectAPIView, LookupField, generics.DestroyAPIView, generics.UpdateAPIView):
    mutate = True
    detail = None

    def get_admin_url(self):
        model = self.provider.model
        return reverse(f"admin:{model._meta.app_label}_{model._meta.model_name}_change", args=[self.get_object().id])

    def get_queryset(self):
        return self.provider.get_queryset(self.request)
