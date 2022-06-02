# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from datetime import datetime
from django.db import models
from django.conf import settings

from utilUtilities.views.utility import Utility

# =========================================================================================
#                                       CONSTANT
# =========================================================================================
DEV = "0"
QAS = "1"
PRD = "2"
SYSTEM = [
    (DEV, "Development"),
    (QAS, "Quality"),
    (PRD, "Production"),
]
SETTINGS_SYSTEM = settings.SYSTEM
# -----------------------------------------
NULL = (None, "", 0)
# -----------------------------------------


# =========================================================================================
#                                       CODE
# =========================================================================================


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(choices=SYSTEM, default=SETTINGS_SYSTEM)

    iso = models.CharField(max_length=3, unique=True, null=True, blank=True)
    isd = models.IntegerField(unique=True)
    name = models.CharField(max_length=127, unique=True)

    created_on = models.PositiveBigIntegerField(blank=True, null=True)
    last_update = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created_on in NULL:
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
        self.name = self.name.upper()
        self.iso = self.iso.upper()
        self.last_update = Utility.datetimeToEpochMs(datetime.now())
        return super(Country, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-{self.name}"


class State(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(choices=SYSTEM, default=SETTINGS_SYSTEM)

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=127, unique=True)

    created_on = models.PositiveBigIntegerField(blank=True, null=True)
    last_update = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created_on in NULL:
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
        self.name = self.name.upper()
        self.last_update = Utility.datetimeToEpochMs(datetime.now())
        return super(State, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-{self.name}"


class City(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(choices=SYSTEM, default=SETTINGS_SYSTEM)

    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=127, unique=True)

    created_on = models.PositiveBigIntegerField(blank=True, null=True)
    last_update = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created_on in NULL:
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
        self.name = self.name.upper() if self.name not in (None, "") else None
        self.last_update = Utility.datetimeToEpochMs(datetime.now())
        return super(City, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-{self.name}"


# -----------------------------------------

# -----------------------------------------

# -----------------------------------------
