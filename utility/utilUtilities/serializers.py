# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from rest_framework import serializers
from utilUtilities.models import Country, State, City

# --------------------------------------------------------------------------
# CODE
# ---------------------------------------------------------------------------
class Country_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            "id",
            "sys",
            "isd",
            "iso",
            "name",
            "created_on",
            "last_update",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "sys": {"read_only": True},
            "created_on": {"read_only": True},
            "last_update": {"read_only": True},
        }
        depth = 1

    def data(self):
        data = super(Country_Serializer, self).data
        return data


class State_Serializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = (
            "id",
            "sys",
            "country",
            "name",
            "created_on",
            "last_update",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "sys": {"read_only": True},
            "created_on": {"read_only": True},
            "last_update": {"read_only": True},
        }
        depth = 1

    def data(self):
        data = super(State_Serializer, self).data
        return data


class City_Serializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            "id",
            "sys",
            "state",
            "name",
            "created_on",
            "last_update",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "sys": {"read_only": True},
            "created_on": {"read_only": True},
            "last_update": {"read_only": True},
        }
        depth = 1

    def data(self):
        data = super(City_Serializer, self).data
        return data
