import json
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from core.models import Ward

class Command(BaseCommand):
    help = "Load wards from GeoJSON"

    def add_arguments(self, parser):
        parser.add_argument("geojson_path", type=str)

    def handle(self, *args, **kwargs):
        path = kwargs["geojson_path"]
        self.stdout.write(f"Loading {path}...")

        with open(path) as f:
            data = json.load(f)

        created = skipped = 0
        for feature in data["features"]:
            p = feature["properties"]
            if Ward.objects.filter(objectid=p["OBJECTID"]).exists():
                skipped += 1
                continue

            Ward.objects.create(
                objectid    = p.get("OBJECTID"),
                state_code  = p.get("STATE_CODE"),
                dcode       = p.get("DCODE"),
                district    = p.get("DISTRICT", ""),
                gapa_napa   = p.get("GaPa_NaPa", ""),
                type_gn     = p.get("Type_GN", ""),
                gn_code     = p.get("GN_CODE"),
                ward_number = p.get("NEW_WARD_N"),
                ddgnww      = p.get("DDGNWW"),
                ddgn        = p.get("DDGN"),
                center      = p.get("CENTER"),
                area_sqkm   = p.get("Area_SQKM"),
                geometry    = GEOSGeometry(json.dumps(feature["geometry"])),
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Done. Created: {created}, Skipped: {skipped}"))