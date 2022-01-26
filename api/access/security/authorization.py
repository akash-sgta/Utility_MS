# --------------------------------------------------------------------------
# DOCUMENTATION
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# LIRARY
# --------------------------------------------------------------------------
from rest_framework.permissions import BasePermission

# --------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# CODE
# --------------------------------------------------------------------------
class Authorization(BasePermission):
    def __init__(self):
        super().__init__()
        self.safe_methods = ["GET"]
        self.restricted_methods = ["POST", "PUT", "DELETE"]

    def has_permission(self, request, view):
        user_ref = request.user
        if request.method in self.safe_methods:
            return True
        if request.method in self.restricted_methods:
            return user_ref.is_admin
