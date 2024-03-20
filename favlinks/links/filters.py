import django_filters
from django_filters import DateFilter, CharFilter

from .models import *


class FavLinkFilter(django_filters.FilterSet):
    title = CharFilter(field_name="title", lookup_expr="icontains")
    start_date = DateFilter(field_name="date", lookup_expr="gte")
    end_date = DateFilter(field_name="date", lookup_expr="lte")

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.filters["category"].queryset = self.filters[
                "category"
            ].queryset.filter(user=user)
            self.filters["tags"].queryset = self.filters["tags"].queryset.filter(
                user=user
            )
        else:
            self.filters["category"].queryset = self.filters["category"].queryset.none()
            self.filters["tags"].queryset = self.filters["tags"].queryset.none()

    class Meta:
        model = FavLink
        fields = ["category", "tags"]
