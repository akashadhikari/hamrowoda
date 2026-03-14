from django.urls import path
from .views import home, state_view, district_view, gapa_view, ward_view

urlpatterns = [
    path('', home, name='home'),

    # New hierarchy
    path('<int:state_number>/', state_view, name='state'),
    path('<int:state_number>/<str:district>/', district_view, name='district'),
    path('<int:state_number>/<str:district>/<str:gapa>/', gapa_view, name='gapa'),
    path('<int:state_number>/<str:district>/<str:gapa>/<int:ward_number>/', ward_view, name='ward'),
]