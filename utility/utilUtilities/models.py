# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from datetime import datetime
from django.db import models

# -----------------------------------------
from utilUtilities.views.utility.utility import Utility
from utilUtilities.views.utility.constant import Constant
from utilApi.models import Api

# =========================================================================================
#                                       CONSTANT
# =========================================================================================


# =========================================================================================
#                                       CODE
# =========================================================================================


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(
        choices=Constant.SYSTEM_CHOICE, default=Constant.SETTINGS_SYSTEM
    )

    iso = models.CharField(max_length=3, unique=True, null=True, blank=True)
    isd = models.IntegerField(unique=True)
    name = models.CharField(max_length=127, unique=True)

    created_on = models.PositiveBigIntegerField(blank=True, null=True)
    last_update = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created_on in Constant.NULL:
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
        self.name = self.name.upper()
        self.iso = self.iso.upper()
        self.last_update = Utility.datetimeToEpochMs(datetime.now())
        return super(Country, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-{self.name}"


class State(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(
        choices=Constant.SYSTEM_CHOICE, default=Constant.SETTINGS_SYSTEM
    )

    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=127, unique=True)

    created_on = models.PositiveBigIntegerField(blank=True, null=True)
    last_update = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created_on in Constant.NULL:
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
        self.name = self.name.upper()
        self.last_update = Utility.datetimeToEpochMs(datetime.now())
        return super(State, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-{self.name}"


class City(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(
        choices=Constant.SYSTEM_CHOICE, default=Constant.SETTINGS_SYSTEM
    )

    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=127, unique=True)

    created_on = models.PositiveBigIntegerField(blank=True, null=True)
    last_update = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created_on in Constant.NULL:
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
        self.name = self.name.upper() if self.name not in (None, "") else None
        self.last_update = Utility.datetimeToEpochMs(datetime.now())
        return super(City, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-{self.name}"


# -----------------------------------------
class Mailer(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(
        choices=Constant.SYSTEM_CHOICE, default=Constant.SETTINGS_SYSTEM
    )

    api = models.ForeignKey(
        to=Api, on_delete=models.SET_NULL, null=True, blank=True
    )

    sender = models.EmailField()
    receiver = models.TextField()
    cc = models.TextField()
    bcc = models.TextField()

    type = models.IntegerField(
        choices=Constant.EMAIL_TYPE_CHOICE, default=Constant.RAW
    )
    subject = models.CharField(max_length=63)
    body = models.TextField()
    attachment = models.TextField()

    status = models.IntegerField(
        choices=Constant.PENDING, default=Constant.STATUS
    )
    reason = models.TextField(null=True, blank=True)

    created_on = models.PositiveBigIntegerField(blank=True, null=True)
    last_update = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created_on in Constant.NULL:
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
        self.subject = self.subject.upper()
        return super(City, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-{self.subject[:16]}"


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(
        choices=Constant.SYSTEM_CHOICE, default=Constant.SETTINGS_SYSTEM
    )

    api = models.ForeignKey(
        to=Api, on_delete=models.SET_NULL, null=True, blank=True
    )

    receiver = models.TextField()

    subject = models.CharField(max_length=63)
    body = models.TextField()
    attachment = models.TextField()

    status = models.IntegerField(
        choices=Constant.PENDING, default=Constant.STATUS
    )
    reason = models.TextField(null=True, blank=True)

    created_on = models.PositiveBigIntegerField(blank=True, null=True)
    last_update = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created_on in Constant.NULL:
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
        self.subject = self.subject.upper()
        return super(City, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-{self.subject[:16]}"


# -----------------------------------------

# -----------------------------------------
