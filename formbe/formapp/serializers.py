from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company, Posts, Usercompany, Userposts
from rest_framework_simplejwt.tokens import RefreshToken


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'


class UsercompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Usercompany
        fields = '__all__'
        
class UserpostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userposts
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin']

    def get_name(self, obj):
        name = obj.first_name

        if name == "":
            name = obj.email

        return name

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get__id(self, obj):
        return obj.id


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
