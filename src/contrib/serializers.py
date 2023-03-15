from contrib.models import Company
from contrib.models import User
from django.db.models import QuerySet
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class UserField(PrimaryKeyRelatedField):
    def to_representation(self, value: User):
        user = User.objects.get(pk=value.pk)
        serializer = UserSerializer(user)
        return serializer.data

    def get_queryset(self) -> QuerySet | list[User]:
        return User.objects.all()


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
