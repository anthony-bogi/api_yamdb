from rest_framework import permissions


class IsAdminOrSuperuserPermission(permissions.BasePermission):
    """Разрешение доступа только для Администратора и Суперпользователя."""
    message = 'Админ зона! У Вас нет разрешения для дальнейшей работы!'

    def has_permission(self, request, view):
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        return False



class IsModeratorPermission(permissions.BasePermission):
    """Доступ разрешен только для Модератора."""
    message = 'Зона Модератора! У Вас нет разрешения для дальнейшей работы!'

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'moderator':
            return True
        return False
