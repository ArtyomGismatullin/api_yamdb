from rest_framework import filters, mixins, viewsets


class CreateListDestroyModelMixin(mixins.CreateModelMixin,
                                  mixins.ListModelMixin,
                                  mixins.DestroyModelMixin,
                                  viewsets.GenericViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
