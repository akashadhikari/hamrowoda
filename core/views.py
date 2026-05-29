from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Ward
from .serializers import WardGeoSerializer


def map_view(request, state=None, district=None, gapa=None, ward=None):
    context = {
        "state": state,
        "district": district,
        "gapa": gapa,
        "ward": ward,
    }
    return render(request, "core/map_view.html", context)


class WardGeoJSONView(ListAPIView):
    serializer_class = WardGeoSerializer

    def get_queryset(self):
        qs = Ward.objects.all()
        state    = self.request.query_params.get("state")
        district = self.request.query_params.get("district")
        gapa     = self.request.query_params.get("gapa")
        ward     = self.request.query_params.get("ward")

        if state:
            qs = qs.filter(state_code=state)
        if district:
            qs = qs.filter(district__iexact=district)
        if gapa:
            qs = qs.filter(gapa_napa__iexact=gapa)
        if ward:
            qs = qs.filter(ward_number=ward)

        return qs