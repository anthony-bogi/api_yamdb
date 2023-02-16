from rest_framework import permissions


class IsAdminOrSuperuserPermission(permissions.BasePermission):
    """Разрешение доступа только для администратора и Суперпользователя."""
    message = 'У Вас нет разрешения для дальнейшей работы!'

    def has_permission(self, request, view):
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        return False
