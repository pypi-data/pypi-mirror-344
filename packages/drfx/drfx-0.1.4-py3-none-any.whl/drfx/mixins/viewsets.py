from rest_framework import mixins
from rest_framework.response import Response

class OptimizedListModelMixin(mixins.ListModelMixin):
    """
    Optimized list mixin with pagination-first and post-prefetch evaluation.
    """
    select_related_fields = ()
    prefetch_related_fields = ()
    annotation_fields = None

    def list(self, request, *args, **kwargs):
        base_qs = self.filter_queryset(self.get_queryset())
        if self.annotation_fields:
            base_qs = base_qs.annotate(**self.annotation_fields)
        page = self.paginate_queryset(base_qs)
        if page is None:
            return Response([])

        ids = [obj.id for obj in page]

        qs = base_qs.filter(id__in=ids)

        if self.select_related_fields:
            qs = qs.select_related(*self.select_related_fields)
        if self.prefetch_related_fields:
            qs = qs.prefetch_related(*self.prefetch_related_fields)


        id_pos = {id_: i for i, id_ in enumerate(ids)}
        ordered = sorted(qs, key=lambda x: id_pos[x.id])

        serializer = self.get_serializer(ordered, many=True)
        return self.get_paginated_response(serializer.data)


class OptimizedRetrieveModelMixin(mixins.RetrieveModelMixin):
    """
    Optimized retrieve mixin with select_related, prefetch_related, and annotation support.
    """
    select_related_fields = ()
    prefetch_related_fields = ()
    annotation_fields = None

    def retrieve(self, request, *args, **kwargs):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]

        qs = self.get_queryset().filter(**{self.lookup_field: lookup_value})

        if self.select_related_fields:
            qs = qs.select_related(*self.select_related_fields)
        if self.prefetch_related_fields:
            qs = qs.prefetch_related(*self.prefetch_related_fields)
        if self.annotation_fields:
            qs = qs.annotate(**self.annotation_fields)

        instance = qs.get()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

