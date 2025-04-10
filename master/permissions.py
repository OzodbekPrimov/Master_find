from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """FAqat xodimlar nmahsulotni tahrirlash yoki o'chirish huquqiga ega. Qolganlar esa faqat o'qishga"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff


class IsOwnerReadOnly(permissions.BasePermission):
    """BU ruxsat faqat obekt egasi va so'rov egasi bitta bo'lsa tahrirlash yoki
    o'chirishga ruxsat beradi aks holda faqat o'qishga"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.owner == request.user