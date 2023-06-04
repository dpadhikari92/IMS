import django_filters
from .models import BOMRawMaterial 

class BOMFilter(django_filters.FilterSet):                            # Stockfilter used to filter based on name
    name = django_filters.CharFilter(lookup_expr='icontains')           # allows filtering without entering the full name
    class Meta:
        model = BOMRawMaterial 
        fields = ['bom']