from rest_framework import serializers
from accounts.models import User, UserRole


class UserRoleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserRole
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    role = UserRoleSerializer(many=True)

    class Meta:
        model = User
        fields = "__all__"
