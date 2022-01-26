# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from rest_framework import serializers
from access.models import Identity

# --------------------------------------------------------------------------
# CODE
# ---------------------------------------------------------------------------
class Identity_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Identity
        fields = ("id", "name", "email", "key", "created_on", "is_active", "is_admin")
        extra_kwargs = {
            "id": {"read_only": True},
            "name": {"read_only": True},
            "key": {"read_only": True},
            "created_on": {"read_only": True},
            "is_admin": {"read_only": True},
        }
