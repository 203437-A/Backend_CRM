from rest_framework import permissions

class CustomEmployeePermission(permissions.BasePermission):
    """
    Permisos personalizados para que los administradores gestionen cualquier empleado y
    los empleados solo puedan acceder o modificar su propio perfil.
    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        if request.method in ['GET', 'PUT', 'PATCH']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if request.method in ['GET', 'PUT', 'PATCH']:
            return obj == request.user

        return False
