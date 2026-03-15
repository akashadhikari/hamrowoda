from django.urls import path
from .views import map_view

urlpatterns = [

    path("", map_view),

    path("<int:state>/", map_view),

    path("<int:state>/<str:district>/", map_view),

    path("<int:state>/<str:district>/<str:gapa>/", map_view),

    path("<int:state>/<str:district>/<str:gapa>/<int:ward>/", map_view),
]