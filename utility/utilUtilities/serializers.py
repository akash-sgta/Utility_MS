# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from rest_framework import serializers

# -----------------------------------------
from utilUtilities.models import Country, State, City, Mailer

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
        depth = 1


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
        depth = 1


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
        depth = 1


# -----------------------------------------
class Mailer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Mailer
        fields = (
            "id",
            "api",
            "sender",
            "reciever",
            "type",
            "subject",
            "body",
            "status",
            "reason",
            "created_on",
            "last_update",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "api": {"read_only": True},
            "created_on": {"read_only": True},
            "last_update": {"read_only": True},
        }
        depth = 1
