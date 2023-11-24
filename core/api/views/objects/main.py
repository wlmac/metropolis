from __future__ import annotations

import os
from json import JSONDecodeError
from typing import Dict, Callable, List, Tuple, Set, Final

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, BadRequest
from django.db.models import Model, Q, QuerySet
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from django.urls import reverse, NoReverseMatch
from rest_framework import generics, permissions
from rest_framework.response import Response

from .base import BaseProvider
from ...utils import GenericAPIViewWithDebugInfo, GenericAPIViewWithLastModified

__all__ = ["ObjectList", "ObjectSingle", "ObjectRetrieve", "ObjectNew"]

GLOBAL_LOOKUPS: Final = ["id"]  # lookups allowed for all providers, first value will be the default if not specified


def gen_get_provider(mapping: Dict[str, str]):
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
        if provider_name not in ProvReqNames:
            raise BadRequest(
                "Object type not found. Valid types are: "
                + ", ".join(ProvReqNames)
                + "."
            )
        return provClassMapping[provider_name]

    return get_provider


get_provider = gen_get_provider(  # k = Provider class name e.g. comment in CommentProvider, v = request name
    {
        "announcement": "announcement",
        "blogpost": "blog-post",
        "exhibit": "exhibit",
        "event": "event",
        "organization": "organization",
        "flatpage": "flatpage",
        "user": "user",
        "tag": "tag",
        "term": "term",
        "timetable": "timetable",
        "comment": "comment",
        "like": "like",
        "course": "course",
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
        self.as_su = as_su  # if the user is a SU
        self.serializer_class = provider.serializer_class
        self.additional_lookup_fields = self._compile_lookup_fields()
        self.listing_filters = getattr(
            provider,
            "listing_filters",
            getattr(provider, "listing_filter", {"id": int, "pk": int}),
        )  # NOTE: better to have the following if after initial, but this is easier

    def _compile_lookup_fields(self) -> Set[str]:
        """
        Compiles the additional lookup fields + the two required into one clean set.
        """
        allowed_fields: List = getattr(  # the lookup fields allowed for the provider
            self.provider, "additional_lookup_fields", []
        )
        allowed_fields.extend(GLOBAL_LOOKUPS)
        return set(
            allowed_fields
        )  # use a set for better memory performance & no duplicates.

    @property
    def lookup_field(self) -> str:
        lookup = (
            self.request.query_params.get("lookup", "id")
            if self.request.query_params.get("lookup") in self.additional_lookup_fields
            else "id"
        )

        field_type = self.provider.model._meta.get_field(
            lookup
        ).get_internal_type()  # get value like CharField
        if field_type in settings.LOOKUP_FIELD_REPLACEMENTS.keys():
            lookup += settings.LOOKUP_FIELD_REPLACEMENTS[field_type]
        return lookup

    def validate_lookup(self) -> None:
        """
        checks the lookup field to see if it's a valid lookup field for the provider.
        :return: NoneType
        """
        lookup = self.request.query_params.get("lookup")
        if lookup is None:
            return
        lookup = lookup or GLOBAL_LOOKUPS[0]
        if lookup not in self.additional_lookup_fields:
            raise BadRequest(
                f"Invalid lookup field {lookup}. Valid fields are: {', '.join(self.additional_lookup_fields)}."
            )

    def get_object(self) -> Model | None:  # None if a 404 (obj not found)
        self.validate_lookup()
        queryset = self.get_queryset()

        q = Q()
        raw = {self.lookup_field: self.kwargs.get("lookup")}
        if self.lookup_field == "id":
            if not raw[self.lookup_field][0].isdigit():
                raise BadRequest(
                    "ID must be an integer, if you want to use a different lookup, refer to the docs for the supported lookups."
                )
        if self.lookup_field in raw:
            if self.lookup_field in ("id", "pk") and raw[self.lookup_field][0] == "0":  # todo, check if needed
                # ignore 0 pk
                pass
            q |= Q(**{self.lookup_field: raw[self.lookup_field]})
        else:
            raise BadRequest("Invalid filtering - Most likely a server error")

        obj = get_object_or_404(queryset, q)
        self.check_object_permissions(self.request, obj)
        return obj

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
            if (request_type := request.method.lower()) in self.http_method_names:
                handler = getattr(self, request_type, self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            kwargs.pop("type")
            response = handler(request, *args, **kwargs)

        except (JSONDecodeError, UnicodeDecodeError):
            raise BadRequest("Invalid JWT, token is malformed.")
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
    FALSE_VALUES = ["false", "0"]
    TRUE_VALUES = ["true", "1"]

    def get_last_modified(self):
        try:
            return self.provider.get_last_modified_queryset()
        except ObjectDoesNotExist:
            return None

    def get_admin_url(self):
        model: Model = self.provider.model
        try:
            return reverse(
                f"admin:{model._meta.app_label}_{model._meta.model_name}_changelist"
            )
        except NoReverseMatch:
            return None

    def __convert_query_params__(self, query_params: QueryDict) -> List[Tuple]:
        """
        Removes non-filter params from query_params and converts them to the correct type.
        :param query_params: QueryDict
        :return: Tuple[List[Tuple], str] (params)
        """
        k_filters = []
        for key, value in query_params.lists():
            if (
                    key
                    in settings.IGNORED_QUERY_PARAMS
                    + self.provider.listing_filters_ignore
            ):
                continue
            if key not in self.listing_filters:
                raise BadRequest(
                    f"{key} is not a valid filter for {self.provider.model.__name__} listing. Valid filters are: {', '.join(self.listing_filters.keys())}."
                )
            lookup_type = self.listing_filters[key]
            if isinstance(value, list):
                k_filters.append(
                    (key, [self.__convert_type__(item, lookup_type) for item in value])
                )
            else:
                k_filters.append((key, self.__convert_type__(value, lookup_type)))
        return k_filters

    def __convert_type__(self, lookup_value: str, lookup_type: Callable) -> object:
        lookup_value = lookup_value.casefold()
        if lookup_type == bool:
            if lookup_value in self.FALSE_VALUES:
                return False
            elif lookup_value in self.TRUE_VALUES:
                return True
            else:
                raise BadRequest(
                    f'Invalid value for boolean filter: {lookup_value}. Accepted values for True are {" or ".join(self.TRUE_VALUES)} and for False they are {" or ".join(self.FALSE_VALUES)}'
                )
        if isinstance(lookup_type, list):
            """
            there are multiple types that are accepted for this filter. See which one matches.
            """
            for type_group in lookup_type:
                type_, category = type_group
                if isinstance(lookup_value, type_):
                    try:
                        return {"item": type_(lookup_value), "category": category}
                    except ValueError:
                        continue
        return lookup_type(lookup_value)

    @staticmethod
    def __compile_filters__(query_params: List) -> Dict:
        filters = {}
        if not query_params:
            # No query params, return None to avoid wastefully filtering.
            return None
        for item in query_params:
            lookup_filter, lookup_value = item

            if isinstance(lookup_value, list) and len(lookup_value) > 1:
                if isinstance(lookup_value[0], dict):
                    filters[f"{lookup_filter}__{lookup_value['category']}__in"] = (
                        # todo add option to use ID or specified field (fix option)
                        lookup_value["item"]
                        if not isinstance(lookup_value["item"], list)
                        else lookup_value["item"][0]
                    )
                else:
                    filters[f"{lookup_filter}__in"] = lookup_value
            else:
                if isinstance(lookup_value, list):
                    lookup_value = lookup_value[0]
                if isinstance(lookup_value, dict):
                    filters[f"{lookup_filter}__{lookup_value['category']}"] = (
                        lookup_value["item"]
                        if not isinstance(lookup_value["item"], list)
                        else lookup_value["item"][0]
                    )
                else:
                    filters[lookup_filter] = lookup_value
        return filters

    def get_queryset(self):
        queryset: QuerySet = self.provider.get_queryset(self.request)
        query_params = self.__convert_query_params__(self.request.query_params)
        filters = self.__compile_filters__(query_params=query_params)
        if filters:
            return queryset.filter(**filters).distinct()
        return queryset

    def get(self, request, *args, **kwargs):
        allow_list = getattr(self.provider, "allow_list", True)
        if not allow_list:
            return Response({"detail": "listing not allowed"}, status=422)
        response = super().get(self, request, *args, **kwargs)
        if response.data["next"]:
            response.data["next"] = response.data["next"].replace("http://", "https://")
        if response.data["previous"]:
            response.data["previous"] = response.data["previous"].replace(
                "http://", "https://"
            )
        return response


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
        model: Model = self.provider.model
        try:
            return reverse(
                f"admin:{model._meta.app_label}_{model._meta.model_name}_changelist"
            )
        except NoReverseMatch:
            return None

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

    def check_allow_single(self):
        allow_single = getattr(self.provider, "allow_single", True)
        if not allow_single:
            return Response({"detail": "editing/deletion not allowed"}, status=422)
        return None

    def delete(self, *args, **kwargs):
        if x := self.check_allow_single():
            return x
        return super().delete(*args, **kwargs)

    def put(self, *args, **kwargs):
        if x := self.check_allow_single():
            return x
        return super().put(*args, **kwargs)

    def patch(self, *args, **kwargs):
        if x := self.check_allow_single():
            return x
        return super().patch(*args, **kwargs)

    def get_admin_url(self):
        model: Model = self.provider.model
        try:
            return reverse(
                f"admin:{model._meta.app_label}_{model._meta.model_name}_changelist"
            )
        except NoReverseMatch:
            return None

    def get_queryset(self):
        return self.provider.get_queryset(self.request)
