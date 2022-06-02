# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from rest_framework import serializers

from utilApi.models import Api, Request


# =========================================================================================
#                                       CONSTANT
# =========================================================================================

# =========================================================================================
#                                       CODE
# =========================================================================================
class Request_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = (
            "id",
            "sys",
            "email",
            "country",
            "phone_no",
            "tg_id",
            "status",
            "reason",
            "created_on",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "sys": {"read_only": True},
            "country": {"read_only": True},
            "created_on": {"read_only": True},
        }
        depth = 1


class Api_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Api
        fields = (
            "id",
            "sys",
            "direction",
            "email",
            "country",
            "phone_no",
            "tg_id",
            "name",
            "key",
            "created_on",
            "last_update",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "sys": {"read_only": True},
            "country": {"read_only": True},
            "key": {"read_only": True},
            "created_on": {"read_only": True},
            "last_update": {"read_only": True},
        }
        depth = 1
