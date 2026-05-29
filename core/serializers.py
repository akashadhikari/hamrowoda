from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Ward

class WardGeoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Ward
        geo_field = "geometry"
        fields = [
            "id", "state_code", "dcode", "district",
            "gapa_napa", "type_gn", "ward_number",
            "center", "area_sqkm"
        ]