from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
        read_only_fields = ['id', 'role']

    def validate_role(self, value):
        # ADMIN rolini tanlashni cheklash
        if value == 'ADMIN':
            raise serializers.ValidationError(
                "ADMIN rolini tanlash mumkin emas. Bu rol faqat admin panel orqali beriladi.")
        return value


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def validate_role(self, value):
        if value not in ['USER', 'MASTER']:
            raise serializers.ValidationError("Role faqat USER yoki USTA bo'lishi mumkin.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user
