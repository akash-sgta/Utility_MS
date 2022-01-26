# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from django.db import models

# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# CODE
# --------------------------------------------------------------------------
class Country(models.Model):
    id = models.AutoField(primary_key=True)
    iso = models.CharField(max_length=3, unique=True, null=True)
    isd = models.CharField(max_length=7, unique=True)  # phone code
    name = models.CharField(max_length=127, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.upper() if self.name not in (None, "") else None
        self.iso = self.iso.upper() if self.iso not in (None, "") else None
        return super(Country, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class State(models.Model):
    id = models.AutoField(primary_key=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=127, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.upper() if self.name not in (None, "") else None
        return super(State, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class City(models.Model):
    id = models.AutoField(primary_key=True)
    state_id = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=127, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.upper() if self.name not in (None, "") else None
        return super(City, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
