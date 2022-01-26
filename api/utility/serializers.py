# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from rest_framework import serializers
from utility.models import Country, State, City

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
        )
        extra_kwargs = {
            "id": {"read_only": True},
        }


class State_Serializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = (
            "id",
            "country_id",
            "name",
        )
        extra_kwargs = {
            "id": {"read_only": True},
        }


class City_Serializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            "id",
            "state_id",
            "name",
        )
        extra_kwargs = {
            "id": {"read_only": True},
        }
