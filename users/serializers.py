from rest_framework import serializers
from users.models import User


class APIRegistarionSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
