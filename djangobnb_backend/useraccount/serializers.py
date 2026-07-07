from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User



class CustomRegisterSerializer(RegisterSerializer):
    username = None

    name = serializers.CharField(required=False, allow_blank=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["name"] = self.validated_data.get("name", "")
        return data

    def save(self, request):
        user = super().save(request)
        user.name = self.validated_data.get("name", "")
        user.save()
        return user
    
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'name', 'avatar_url'
        )