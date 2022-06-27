# =========================================================================================
#                                       DOCUMENTATION
# =========================================================================================
"""
Naming Convention
Authoriser_<ViewName>_as<Entity>
"""

# =========================================================================================
#                                       LIBRARY
# =========================================================================================
from rest_framework.permissions import BasePermission
from requests import get

# ------------------------------------------
from utilities.util.constant import Constant


# =========================================================================================
#                                       CONSTANT
# =========================================================================================
CREATE = "POST"
READ = "GET"
UPDATE = "PUT"
DELETE = "DELETE"
ADMIN = "ADMIN"
USER = "USER"
# --------------------------------------------------

# =========================================================================================
#                                       CODE
# =========================================================================================
class Authoriser(BasePermission):
    def __init__(self) -> None:
        self.safe_methods = []
        self.restricted_methods = []
        self.no_access = []
        self.methods = [CREATE, READ, UPDATE, DELETE]
        self.access = [ADMIN, USER]
        super().__init__()

    def outbound_call(self) -> bool:
        # TODO: Place actual request call to check access from IAM_MS
        return True

    def has_access(self, method: str, access: str) -> bool:
        try:
            if method is None or access is None:
                raise Exception("Invalid Formal Arguments")
            if method.upper() not in self.methods:
                raise Exception("Invalid Method name")
            if access.upper * () not in self.access:
                raise Exception("Invalid Access name")
            self.outbound_call()
        except Exception as e:
            print(f"ERROR : {str(e)}")
            return False
        else:
            return True


class Authoriser_asUser(Authoriser):
    def __init__(self):
        super(Authoriser_asUser, self).__init__()
        self.safe_methods = []
        self.restricted_methods = [
            READ,
            CREATE,
            UPDATE,
            DELETE,
        ]
        self.no_access = []

    def has_permission(self, request, view):
        try:
            if request.method in self.safe_methods:
                pass
            elif request.method in self.no_access:
                raise Exception("NO ACCESS")
            elif request.method in self.restricted_methods:
                if self.has_access(method=request.method, access=USER):
                    pass
                else:
                    raise Exception("ACCESS DENIED")
            else:
                raise Exception("INVALID METHOD")
        except Exception as e:
            print(f"ERROR : {str(e)}")
            return False
        else:
            return True


class Authoriser_asAdmin(Authoriser):
    def __init__(self):
        super(Authoriser_asAdmin, self).__init__()
        self.safe_methods = []
        self.restricted_methods = [
            READ,
            CREATE,
            UPDATE,
            DELETE,
        ]
        self.no_access = []

    def has_permission(self, request, view):
        try:
            if request.method in self.safe_methods:
                pass
            elif request.method in self.no_access:
                raise Exception("NO ACCESS")
            elif request.method in self.restricted_methods:
                if self.has_access(method=request.method, access=ADMIN):
                    pass
                else:
                    raise Exception("ACCESS DENIED")
            else:
                raise Exception("INVALID METHOD")
        except Exception as e:
            print(f"ERROR : {str(e)}")
            return False
        else:
            return True
