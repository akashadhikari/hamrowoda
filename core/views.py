from django.shortcuts import render

def map_view(request, state=None, district=None, gapa=None, ward=None):

    context = {
        "state": state,
        "district": district,
        "gapa": gapa,
        "ward": ward
    }

    return render(request, "core/map_view.html", context)