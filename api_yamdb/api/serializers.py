from rest_framework import serializers

from users.models import CHOICES, User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=CHOICES, default='user')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
