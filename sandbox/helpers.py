from django.http import HttpResponse
from django.utils.functional import cached_property
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data=None, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json; charset=utf-8'

        super(JSONResponse, self).__init__(content, **kwargs)


class SandboxDefaultPaginator(PageNumberPagination):
    """
    Default paginator class for the project.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return JSONResponse(dict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class SandboxGenericView(GenericAPIView):
    """
    Generic API class for project.
    """

    pagination_class = SandboxDefaultPaginator
    serializer_class_receive = None
    serializer_class_response = None
    serializer_class_query = None
    serializer_class_basis = None

    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._paginated = None

    @cached_property
    def user(self):
        return self.request.user

    @cached_property
    def query_params(self):
        return self.get_query_params()

    def get_query_params(self):
        serializer = self.get_query_serializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data

    def get_query_serializer(self, *args, **kwargs):
        assert self.serializer_class_query is not None, (
                "'%s' should either include a `serializer_class_query` attribute, "
                "or override the `get_query_serializer()` method."
                % self.__class__.__name__)

        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class_query(*args, **kwargs)

    def get_response_serializer(self, *args, **kwargs):
        assert self.serializer_class_response is not None, (
                "'%s' should either include a `serializer_class_response` attribute, "
                "or override the `get_response_serializer()` method."
                % self.__class__.__name__)

        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class_query(*args, **kwargs)

    def get_receive_serializer(self, *args, **kwargs):
        assert self.serializer_class_receive is not None, (
                "'%s' should either include a `serializer_class_receive` attribute, "
                "or override the `get_receive_serializer()` method."
                % self.__class__.__name__)

        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class_query(*args, **kwargs)

    @cached_property
    def validated_data(self):
        return self.get_validated_data()

    def get_validated_data(self, instance=None):
        self.serializer_class_basis = self.serializer_class
        if self.serializer_class_receive:
            self.serializer_class = self.serializer_class_receive

        serializer = self.get_serializer(instance=instance, data=self.request.data)
        self.serializer_class = self.serializer_class_basis
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data

    def get_response_data(self, instance=None, queryset=None):
        assert not any([instance, queryset]), (
                "'%s' should either include an `instance` parameter or `queryset` parameter."
                % self.get_response_data.__qualname__
        )

        self.serializer_class_basis = self.serializer_class
        if self.serializer_class_response:
            self.serializer_class = self.serializer_class_response

        serializer = self.get_serializer(instance, many=bool(queryset))
        self.serializer_class = self.serializer_class_basis

        return serializer.data

    def get_object(self):
        """
        Extended get_object logic with setting default None value to url kwarg if it hasn't been given.
        For backward compatibility (django doesn't provide default None value).
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        self.kwargs.setdefault(lookup_url_kwarg, None)

        return super().get_object()

    def check_permissions(self, request):
        """
        Redefine permissions logic here. We want to grant access as not AND but as OR
        """
        if not any([
            permission.has_permission(request, self)
            for permission in self.get_permissions()
        ]):
            self.permission_denied(request)

    def create_raw(self, request, *args, **kwargs):
        self.serializer_class_basis = self.serializer_class
        if self.serializer_class_receive:
            self.serializer_class = self.serializer_class_receive

        serializer = self.get_serializer(data=request.data)
        self.serializer_class = self.serializer_class_basis
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(**kwargs)

        response_data = self.get_response_data(instance=instance)

        return response_data

    def create(self, request, *args, **kwargs):
        data = self.create_raw(request, *args, **kwargs)

        return JSONResponse(data)

    def list_raw(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            self._paginated = True
            queryset = page

        response_data = self.get_response_data(queryset=queryset)

        return response_data

    def list(self, request, *args, **kwargs):
        data = self.list_raw(request, *args, **kwargs)
        if self._paginated:
            return self.get_paginated_response(data)

        return JSONResponse(data)

    def retrieve_raw(self, request, *args, **kwargs):
        instance = self.get_object()
        response_data = self.get_response_data(instance=instance)

        return response_data

    def retrieve(self, request, *args, **kwargs):
        data = self.retrieve_raw(request, *args, **kwargs)

        return JSONResponse(data)

    def update_raw(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        self.serializer_class_basis = self.serializer_class
        if self.serializer_class_receive:
            self.serializer_class = self.serializer_class_receive

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        self.serializer_class = self.serializer_class_basis
        serializer.is_valid(raise_exception=True)
        serializer.save(**kwargs)

        instance.refresh_from_db()
        response_data = self.get_response_data(instance=instance)

        return response_data

    def update(self, request, *args, **kwargs):
        data = self.update_raw(request, *args, **kwargs)

        return JSONResponse(data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True

        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True
        instance.save()

        return JSONResponse(status=status.HTTP_204_NO_CONTENT)
