# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from django.db import models
from datetime import datetime

# --------------------------------------------------
from utilities.util.constant import Constant
from utilities.util.utility import Utility


# =========================================================================================
#                                       CONSTANT
# =========================================================================================


# =========================================================================================
#                                       CODE
# =========================================================================================
class Request(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(
        choices=Constant.SYSTEM_CHOICE, default=Constant.SETTINGS_SYSTEM
    )

    email = models.EmailField()
    isd = models.CharField(
        validators=[Constant.REGEX_INTEGER],
        null=True,
        blank=True,
        max_length=7,
    )
    phone_no = models.CharField(
        validators=[Constant.REGEX_INTEGER],
        null=True,
        blank=True,
        max_length=15,
    )
    tg_id = models.CharField(
        validators=[Constant.REGEX_INTEGER],
        null=True,
        blank=True,
        max_length=63,
    )

    status = models.IntegerField(
        choices=Constant.STATUS_CHOICE, default=Constant.PENDING
    )
    reason = models.TextField(null=True, blank=True)

    created_on = models.PositiveBigIntegerField(blank=True, null=True)
    last_update = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created_on in Constant.NULL:  # Only when item created
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
        self.email = self.email.upper()
        if self.isd in Constant.NULL:
            self.isd = None
        if self.phone_no in Constant.NULL:
            self.phone_no = None
        if self.tg_id in Constant.NULL:
            self.tg_id = None
        self.last_update = Utility.datetimeToEpochMs(datetime.now())
        return super(Request, self).save()

    def __str__(self) -> str:
        return f"{self.id}-{self.email}"


class Api(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(
        choices=Constant.SYSTEM_CHOICE, default=Constant.SETTINGS_SYSTEM
    )

    direction = models.IntegerField(
        choices=Constant.DIRECTION_CHOICE, default=Constant.IN
    )

    email = models.EmailField()
    isd = models.CharField(
        validators=[Constant.REGEX_INTEGER],
        null=True,
        blank=True,
        max_length=7,
    )
    phone_no = models.CharField(
        validators=[Constant.REGEX_INTEGER],
        null=True,
        blank=True,
        max_length=15,
    )
    tg_id = models.CharField(
        validators=[Constant.REGEX_INTEGER],
        null=True,
        blank=True,
        max_length=63,
    )

    name = models.CharField(max_length=127, unique=True)
    key = models.CharField(max_length=255, blank=True, null=True)

    last_update = models.PositiveBigIntegerField(blank=True, null=True)
    created_on = models.PositiveBigIntegerField(blank=True, null=True)

    def __refresh(self):
        self.key = Utility.randomGenerator(length=225, no_symbol=True)

    def save(self, *args, **kwargs):
        if self.created_on in Constant.NULL:  # Only when item created
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
            self.name = self.name.upper()
        if self.direction == Constant.OUT:
            self.email = Constant.SETTINGS_EMAIL_EMAIL
        if self.isd in Constant.NULL:
            self.isd = None
        if self.phone_no in Constant.NULL:
            self.phone_no = None
        if self.tg_id in Constant.NULL:
            self.tg_id = None
        self.email = self.email.upper()
        self.__refresh()
        self.last_update = Utility.datetimeToEpochMs(datetime.now())
        return super(Api, self).save()

    def __str__(self) -> str:
        return f"{self.id}-{self.name}"
