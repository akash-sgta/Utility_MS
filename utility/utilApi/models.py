# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from django.db import models
from datetime import datetime

# --------------------------------------------------
from utilUtilities.views.utility import Utility, Constant


# =========================================================================================
#                                       CONSTANT
# =========================================================================================


# =========================================================================================
#                                       CODE
# =========================================================================================
class Request(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(
        choices=Constant.SYSTEM, default=Constant.SETTINGS_SYSTEM
    )

    email = models.EmailField(unique=True)
    isd = models.CharField(null=True, blank=True, max_length=7)
    phone_no = models.CharField(unique=True, max_length=15)
    tg_id = models.CharField(max_length=127, blank=True, null=True)
    status = models.IntegerField(
        choices=Constant.STATUS, default=Constant.PENDING
    )
    reason = models.TextField(null=True, blank=True)

    created_on = models.PositiveBigIntegerField(blank=True, null=True)
    last_update = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created_on in Constant.NULL:  # Only when item created
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
        self.email = self.email.upper()
        self.last_update = Utility.datetimeToEpochMs(datetime.now())
        return super(Request, self).save()


class Api(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(
        choices=Constant.SYSTEM, default=Constant.SETTINGS_SYSTEM
    )

    direction = models.ImageField(
        choice=Constant.DIRECTION, default=Constant.IN
    )

    email = models.EmailField(unique=True)
    isd = models.CharField(null=True, blank=True, max_length=7)
    phone_no = models.IntegerField(unique=True, max_length=15)
    tg_id = models.CharField(max_length=127, blank=True, null=True)
    name = models.CharField(max_length=127)
    key = models.CharField(max_length=255, blank=True, null=True)

    last_update = models.PositiveBigIntegerField(blank=True, null=True)
    created_on = models.PositiveBigIntegerField(blank=True, null=True)

    def __refresh(self):
        self.key = Utility.randomGenerator(length=225)

    def save(self, *args, **kwargs):
        if self.created_on in Constant.NULL:  # Only when item created
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
            self.name = self.name.upper()
        if self.direction == Constant.OUT:
            self.email = Constant.SETTINGS_EMAIL
        self.email = self.email.upper()
        self.__refresh()
        self.last_update = Utility.datetimeToEpochMs(datetime.now())
        return super(Api, self).save()
