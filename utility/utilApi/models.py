# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from email.policy import default
from secrets import choice
from django.core.validators import RegexValidator
from django.db import models
from datetime import datetime
from django.conf import settings

# --------------------------------------------------
from utilUtilities.views.utility import Utility
from utilUtilities.models import Country

# =========================================================================================
#                                       CONSTANT
# =========================================================================================
REGEX_PHONE_SIMPLE = r"\d{8,13}"
REGEX_PHONE = RegexValidator(regex=REGEX_PHONE_SIMPLE, message="Phone number invalid. Expected : 10 to 15 digits.")
REGEX_EMAIL = RegexValidator(
    regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", message="Email Id is invalid."
)
# --------------------------------------------------
NULL = (None, "", 0)
SETTINGS_SYSTEM = settings.SYSTEM
SETTINGS_EMAIL = settings.EMAIL
# --------------------------------------------------
IN = "0"
OUT = "1"
DIRECTION = [
    (IN, "Inbound"),
    (OUT, "Outbound"),
]
DEV = "0"
QAS = "1"
PRD = "2"
SYSTEM = [
    (DEV, "Development"),
    (QAS, "Quality"),
    (PRD, "Production"),
]
PENDING = "0"
CREATED = "1"
REJECTED = "2"
STATUS = [
    (PENDING, "Pending"),
    (CREATED, "Created"),
    (REJECTED, "Rejected"),
]


# =========================================================================================
#                                       CODE
# =========================================================================================
class Request(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(choices=SYSTEM, default=SETTINGS_SYSTEM)

    email = models.EmailField(
        unique=True,
        validators=[REGEX_EMAIL],
        max_length=255,
    )
    country = models.ForeignKey(to=Country, null=True, on_delete=models.SET_NULL)
    phone_no = models.CharField(
        unique=True,
        validators=[REGEX_PHONE],
        max_length=15,
    )
    tg_id = models.CharField(
        max_length=127,
        blank=True,
        null=True,
    )
    status = models.IntegerField(
        choices=STATUS,
        default=PENDING,
    )
    reason = models.CharField(max_length=255)

    created_on = models.PositiveBigIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created_on in NULL:  # Only when item created
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
        self.email = self.email.upper()
        return super(Request, self).save()


class Api(models.Model):
    id = models.AutoField(primary_key=True)
    sys = models.IntegerField(choices=SYSTEM, default=SETTINGS_SYSTEM)

    direction = models.ImageField(choice=DIRECTION, default=IN)

    email = models.EmailField(
        unique=True,
        validators=[REGEX_EMAIL],
        max_length=255,
    )
    country = models.ForeignKey(to=Country, null=True, on_delete=models.SET_NULL)
    phone_no = models.CharField(
        unique=True,
        validators=[REGEX_PHONE],
        max_length=15,
        null=True,
        blank=True,
    )
    tg_id = models.CharField(
        max_length=127,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=127)
    key = models.CharField(max_length=255, blank=True, null=True)

    last_update = models.PositiveBigIntegerField(blank=True, null=True)
    created_on = models.PositiveBigIntegerField(blank=True, null=True)

    def __refresh(self):
        self.key = Utility.randomGenerator(length=225)

    def save(self, *args, **kwargs):
        if self.created_on in NULL:  # Only when item created
            self.created_on = Utility.datetimeToEpochMs(datetime.now())
            self.name = self.name.upper()
        if self.direction == OUT:
            self.email = SETTINGS_EMAIL
        self.email = self.email.upper()
        self.__refresh()
        self.last_update = Utility.datetimeToEpochMs(datetime.now())
        return super(Api, self).save()
