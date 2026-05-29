from django.urls import path
from .views import map_view, WardGeoJSONView

urlpatterns = [
    path("", map_view, name="map_home"),
    path("<int:state>/", map_view, name="map_state"),
    path("<int:state>/<str:district>/", map_view, name="map_district"),
    path("<int:state>/<str:district>/<str:gapa>/", map_view, name="map_gapa"),
    path("<int:state>/<str:district>/<str:gapa>/<int:ward>/", map_view, name="map_ward"),
    path("api/wards/", WardGeoJSONView.as_view(), name="ward_geojson"),
]