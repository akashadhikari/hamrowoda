import matplotlib
matplotlib.use('Agg')

from django.shortcuts import render
from django.http import Http404
import geopandas as gpd
import os
import matplotlib.pyplot as plt
import io

# Load GeoJSON
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
geojson_path = os.path.join(BASE_DIR, 'core', 'static', 'core', 'Ward_plus_Limpiyadhura.geojson')
gdf = gpd.read_file(geojson_path)

# Case insensitive helpers
gdf['STATE_CODE_lower'] = gdf['STATE_CODE'].astype(str).str.lower()
gdf['DISTRICT_lower'] = gdf['DISTRICT'].str.lower()
gdf['GaPa_lower'] = gdf['GaPa_NaPa'].str.lower()


# ---------------------------------
# SVG MAP GENERATOR
# ---------------------------------

def create_svg(main_gdf, demarcation_gdf=None, demarcation_color="blue"):

    fig, ax = plt.subplots(figsize=(6,6))

    # Main polygon
    main_gdf.plot(ax=ax, color="white", edgecolor="black", linewidth=1)

    # Inner boundaries
    if demarcation_gdf is not None:
        demarcation_gdf.boundary.plot(ax=ax, edgecolor=demarcation_color, linewidth=1)

    ax.set_aspect('equal')
    ax.axis("off")

    fig.tight_layout()

    buffer = io.StringIO()
    fig.savefig(buffer, format="svg")
    plt.close(fig)

    return buffer.getvalue()


# ---------------------------------
# HOME → NEPAL MAP WITH STATES
# ---------------------------------

def home(request):

    states = gdf.dissolve(by='STATE_CODE')

    svg_map = create_svg(gdf, states)

    return render(request, "core/map_view.html", {
        "title": "Nepal",
        "map": svg_map
    })


# ---------------------------------
# STATE VIEW
# ---------------------------------

def state_view(request, state_number):

    state_lower = str(state_number).lower()

    gdf_state = gdf[gdf['STATE_CODE_lower'] == state_lower]

    if gdf_state.empty:
        raise Http404("State not found")

    districts = gdf_state.dissolve(by='DISTRICT')

    svg_map = create_svg(gdf_state, districts)

    title = f"State {gdf_state['STATE_CODE'].iloc[0]}"

    return render(request, "core/map_view.html", {
        "title": title,
        "map": svg_map
    })


# ---------------------------------
# DISTRICT VIEW
# ---------------------------------

def district_view(request, state_number, district):

    state_lower = str(state_number).lower()
    district_lower = district.lower()

    gdf_state = gdf[gdf['STATE_CODE_lower'] == state_lower]

    if gdf_state.empty:
        raise Http404("State not found")

    gdf_district = gdf_state[gdf_state['DISTRICT_lower'] == district_lower]

    if gdf_district.empty:
        raise Http404("District not found")

    gapas = gdf_district.dissolve(by='GaPa_NaPa')

    svg_map = create_svg(gdf_district, gapas)

    title = f"State {state_number}, District {gdf_district['DISTRICT'].iloc[0]}"

    return render(request, "core/map_view.html", {
        "title": title,
        "map": svg_map
    })


# ---------------------------------
# GAPA / NAPA VIEW
# ---------------------------------

def gapa_view(request, state_number, district, gapa):

    state_lower = str(state_number).lower()
    district_lower = district.lower()
    gapa_lower = gapa.lower()

    gdf_state = gdf[gdf['STATE_CODE_lower'] == state_lower]

    if gdf_state.empty:
        raise Http404("State not found")

    gdf_district = gdf_state[gdf_state['DISTRICT_lower'] == district_lower]

    if gdf_district.empty:
        raise Http404("District not found")

    gdf_gapa = gdf_district[gdf_district['GaPa_lower'] == gapa_lower]

    if gdf_gapa.empty:
        raise Http404("GaPa/Napa not found")

    wards = gdf_gapa.dissolve(by='NEW_WARD_N')

    svg_map = create_svg(gdf_gapa, wards)

    title = f"State {state_number}, District {gdf_gapa['DISTRICT'].iloc[0]}, {gdf_gapa['GaPa_NaPa'].iloc[0]}"

    return render(request, "core/map_view.html", {
        "title": title,
        "map": svg_map
    })


# ---------------------------------
# WARD VIEW
# ---------------------------------

def ward_view(request, state_number, district, gapa, ward_number):

    state_lower = str(state_number).lower()
    district_lower = district.lower()
    gapa_lower = gapa.lower()

    gdf_state = gdf[gdf['STATE_CODE_lower'] == state_lower]

    if gdf_state.empty:
        raise Http404("State not found")

    gdf_district = gdf_state[gdf_state['DISTRICT_lower'] == district_lower]

    if gdf_district.empty:
        raise Http404("District not found")

    gdf_gapa = gdf_district[gdf_district['GaPa_lower'] == gapa_lower]

    if gdf_gapa.empty:
        raise Http404("GaPa/Napa not found")

    gdf_ward = gdf_gapa[gdf_gapa['NEW_WARD_N'] == ward_number]

    if gdf_ward.empty:
        raise Http404("Ward not found")

    svg_map = create_svg(gdf_ward)

    title = f"State {state_number}, District {gdf_ward['DISTRICT'].iloc[0]}, {gdf_ward['GaPa_NaPa'].iloc[0]}, Ward {ward_number}"

    return render(request, "core/map_view.html", {
        "title": title,
        "map": svg_map
    })