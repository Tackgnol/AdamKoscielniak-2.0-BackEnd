
from Models.UserRole import UserRole

def IsUserRoleValid(userRole):
    print(_getUserRoles())
    return userRole in _getUserRoles()

def IsUserAdmin(userRole):
    print(_getAdminRoles())
    print(userRole)
    return userRole in _getAdminRoles()

def _getAdminRoles():
    return [u.Name for u in UserRole.objects if bool(u.IsAdmin)]

def _getUserRoles():
    return [u.Name for u in UserRole.objects if not u.IsAdmin]