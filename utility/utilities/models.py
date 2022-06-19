# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from datetime import datetime
from lib2to3.pgen2.token import COMMA
from django.db import models
from django.dispatch import receiver

# -----------------------------------------
from utilities.views.utility.utility import Utility
from utilities.views.utility.constant import Constant
from api.models import Api

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
class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(
        choices=Constant.SYSTEM_CHOICE, default=Constant.SETTINGS_SYSTEM
    )

    api = models.ForeignKey(to=Api, on_delete=models.SET_NULL, null=True)

    subject = models.CharField(max_length=63)
    body = models.TextField(blank=True, null=True)
    attachment = models.TextField(blank=True, null=True)
    type = models.IntegerField(
        choices=Constant.EMAIL_TYPE_CHOICE, default=Constant.RAW
    )

    created_on = models.PositiveBigIntegerField(blank=True, null=True)
    last_update = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created_on in Constant.NULL:
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
        self.subject = self.subject.upper()
        if self.body in Constant.NULL:
            self.body = None
        if self.attachment in Constant.NULL:
            self.attachment = None
        self.last_update = Utility.datetimeToEpochMs(datetime.now())
        return super(Mailer, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-{self.subject[:16]}"


class Mailer(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(
        choices=Constant.SYSTEM_CHOICE, default=Constant.SETTINGS_SYSTEM
    )
    notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, null=False
    )

    receiver = models.TextField()
    cc = models.TextField(null=True, blank=True)
    bcc = models.TextField(null=True, blank=True)

    status = models.IntegerField(
        choices=Constant.STATUS_CHOICE, default=Constant.PENDING
    )
    reason = models.TextField(null=True, blank=True)

    created_on = models.PositiveBigIntegerField(blank=True, null=True)
    last_update = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created_on in Constant.NULL:
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
        self.receiver = Constant.COMA.join(
            Utility.emailListGen(self.receiver)
        )
        self.cc = Constant.COMA.join(Utility.emailListGen(self.cc))
        self.bcc = Constant.COMA.join(Utility.emailListGen(self.bcc))
        self.last_update = Utility.datetimeToEpochMs(datetime.now())
        return super(Mailer, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-{self.notification.subject[:16]}"


class Telegram(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(
        choices=Constant.SYSTEM_CHOICE, default=Constant.SETTINGS_SYSTEM
    )
    notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, null=False
    )

    receiver = models.TextField(null=False, blank=False)

    status = models.IntegerField(
        choices=Constant.STATUS_CHOICE, default=Constant.PENDING
    )
    reason = models.TextField(null=True, blank=True)

    created_on = models.PositiveBigIntegerField(blank=True, null=True)
    last_update = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created_on in Constant.NULL:
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
        self.receiver = Constant.COMA.join(Utility.tgUserListGen(self.cc))
        self.last_update = Utility.datetimeToEpochMs(datetime.now())
        return super(Notification, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-{self.notification.subject[:16]}"


# -----------------------------------------
class UrlShort(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(
        choices=Constant.SYSTEM_CHOICE, default=Constant.SETTINGS_SYSTEM
    )

    key = models.CharField(max_length=31, unique=True)
    model = models.IntegerField(
        choices=Constant.MODEL_MODEL_CHOICE, default=Constant.REQUEST
    )
    type = models.IntegerField(
        choices=Constant.MODEL_TYPE_CHOICE, default=Constant.ID
    )
    query = models.CharField(max_length=127)

    created_on = models.PositiveBigIntegerField(blank=True, null=True)
    last_update = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created_on in Constant.NULL:
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
            self.key = Utility.randomGenerator(length=15, no_symbol=True)
        self.last_update = Utility.datetimeToEpochMs(datetime.now())
        return super(UrlShort, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-{self.key}"


# -----------------------------------------
class Log(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(
        choices=Constant.SYSTEM_CHOICE, default=Constant.SETTINGS_SYSTEM
    )

    body = models.TextField()

    created_on = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created_on in Constant.NULL:
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
        return super(Log, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-{Utility.datetimeToStr(Utility.epochMsToDatetime(self.created_on))}"
