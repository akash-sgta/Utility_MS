# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from rest_framework import serializers

# -----------------------------------------
from utilities.models import (
    Country,
    State,
    City,
    Notification,
    Mailer,
    Telegram,
    UrlShort,
)

# --------------------------------------------------------------------------
# CODE
# ---------------------------------------------------------------------------
class Country_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            "id",
            "isd",
            "iso",
            "name",
            "created_on",
            "last_update",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "created_on": {"read_only": True},
            "last_update": {"read_only": True},
        }
        depth = 0


class State_Serializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = (
            "id",
            "country",
            "name",
            "created_on",
            "last_update",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "created_on": {"read_only": True},
            "last_update": {"read_only": True},
        }
        depth = 0


class City_Serializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            "id",
            "state",
            "name",
            "created_on",
            "last_update",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "created_on": {"read_only": True},
            "last_update": {"read_only": True},
        }
        depth = 0


# -----------------------------------------
class Notification_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "id",
            "api",
            "subject",
            "body",
            "attachment",
            "type",
            "created_on",
            "last_update",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "api": {"read_only": True},
            "created_on": {"read_only": True},
            "last_update": {"read_only": True},
        }
        depth = 0


class Mailer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Mailer
        fields = (
            "id",
            "notification",
            "receiver",
            "cc",
            "bcc",
            "status",
            "reason",
            "created_on",
            "last_update",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "created_on": {"read_only": True},
            "last_update": {"read_only": True},
        }
        depth = 0


class Telegram_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Telegram
        fields = (
            "id",
            "api",
            "notificaiton",
            "receiver",
            "status",
            "reason",
            "created_on",
            "last_update",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "created_on": {"read_only": True},
            "last_update": {"read_only": True},
        }
        depth = 0


# -----------------------------------------
class UrlShort_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UrlShort
        fields = (
            "id",
            "key",
            "model",
            "type",
            "query",
            "created_on",
            "last_update",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "created_on": {"read_only": True},
            "last_update": {"read_only": True},
        }
        depth = 0
