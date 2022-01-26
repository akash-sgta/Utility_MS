# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from django.db import models
from datetime import datetime
from utility.extra.pool import datetime2epochms, randomGenerator

# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------
from api.settings import REFRESH_TOKEN_LIMIT, ACCESS_TOKEN_LIMIT
from utility.extra.constant import ERROR_RT_TIMEOUT, ERROR_AT_TIMEOUT, ERROR_PD_REQUIRED


# --------------------------------------------------------------------------
# CODE
# --------------------------------------------------------------------------
class Identity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=127, unique=True)
    email = models.EmailField(blank=True, null=True)
    key = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.PositiveBigIntegerField(blank=True, null=True)  # ms from epoch
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.created_on = self.created_on if self.created_on not in (None, "") else None
        self.key = self.key if self.key not in (None, "") else None
        if self.created_on == None:  # fill once at creation of entity
            self.created_on = datetime2epochms(datetime.now())
            self.name = self.name.upper()
            self.key = randomGenerator(noSybmol=True)
        self.email = self.email.upper()

        return super(Identity, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name[:10]}"
