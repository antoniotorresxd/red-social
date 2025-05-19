from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_superuser']

class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            if not user:
                raise serializers.ValidationError(
                    "Credenciales inválidas.",
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                'Debe incluir \"email\" y \"password\".',
                code='authorization'
            )
        attrs['user'] = user
        return attrs

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'name', 'birthdate', 'password', 'password2', 'id_student']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "Las contraseñas no coinciden."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)


class PasswordResetByEmailBirthdaySerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    birthdate = serializers.DateField(write_only=True)
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
