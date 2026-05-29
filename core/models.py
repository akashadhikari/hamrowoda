from django.contrib.gis.db import models

class Ward(models.Model):
    objectid    = models.IntegerField(unique=True)
    state_code  = models.IntegerField(db_index=True, null=True)
    dcode       = models.IntegerField(db_index=True, null=True)
    district    = models.CharField(max_length=100, db_index=True)
    gapa_napa   = models.CharField(max_length=100, db_index=True)
    type_gn     = models.CharField(max_length=50)
    gn_code     = models.FloatField(null=True)
    ward_number = models.IntegerField(db_index=True, null=True)
    ddgnww      = models.FloatField(null=True)
    ddgn        = models.IntegerField(null=True)
    center      = models.CharField(max_length=100, null=True, blank=True)
    area_sqkm   = models.FloatField(null=True)
    geometry    = models.GeometryField(srid=4326)

    class Meta:
        indexes = [
            models.Index(fields=["state_code", "district", "gapa_napa", "ward_number"])
        ]

    def __str__(self):
        return f"{self.gapa_napa} - Ward {self.ward_number}"