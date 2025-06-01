from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User as UserModel
from .serializers import (
    EmailAuthTokenSerializer,
    PasswordResetByEmailBirthdaySerializer,
    RegistrationSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = UserModel.objects.none()

    @staticmethod
    def handle_message_response(message, status_code, data=None):
        return Response({
            'data': data or [],
            'message': message,
            'status_code': status_code,
        }, status=status_code)

    def list(self, request):
        try:
            ids = request.query_params.get('ids')
            if not ids:
                return self.handle_message_response(
                    message='',
                    status_code=status.HTTP_200_OK,
                    data=[],
                )

            id_list = [int(pk) for pk in ids.split(',') if pk.isdigit()]
            queryset = UserModel.objects.filter(id__in=id_list)
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.serializer_class(page, many=True)
                return self.handle_message_response(
                    message='Usuarios encontrados',
                    status_code=status.HTTP_200_OK,
                    data=serializer.data,
                )

            serializer = self.serializer_class(queryset, many=True)
            return self.handle_message_response(
                message='Usuarios encontrados',
                status_code=status.HTTP_200_OK,
                data=serializer.data,
            )

        except Exception as e:
            return self.handle_message_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                data=[],
            )

    def retrieve(self, request, pk=None):
        try:
            instance = get_object_or_404(UserModel, id=pk)
            serializer = self.serializer_class(instance)
            return self.handle_message_response(
                message='Usuario no encontrado',
                status_code=status.HTTP_200_OK,
                data=serializer.data,
            )

        except Exception as e:
            return self.handle_message_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                data=[],
            )
            
    @action(detail=False, methods=['get'], url_path='find-by-email')
    def find_by_email(self, request):
        email = request.query_params.get('email', '').strip()

        if not email:
            return self.handle_message_response(
                message="El parámetro 'email' es obligatorio.",
                status_code=status.HTTP_400_BAD_REQUEST,
                data=[]
            )

        try:
            user = get_object_or_404(UserModel, email=email)
            serializer = self.serializer_class(user)
            return self.handle_message_response(
                message="Usuario encontrado",
                status_code=status.HTTP_200_OK,
                data=serializer.data
            )

        except Exception as e:
            return self.handle_message_response(
                message=f"Error al buscar usuario: {str(e)}",
                status_code=status.HTTP_400_BAD_REQUEST,
                data=[]
            )

    @action(
        detail=False,
        methods=['post'],
        url_path='register',
        serializer_class=RegistrationSerializer,
    )
    def register(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            user_data = self.serializer_class(user).data

            return self.handle_message_response(
                message=f"{user} Registrado satisfactoriamente",
                status_code=status.HTTP_201_CREATED,
                data=user_data,
            )

        except Exception as e:
            return self.handle_message_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                data=[],
            )

    def update(self, request, pk=None):
        try:
            instance = get_object_or_404(UserModel, id=pk)
            serializer = self.serializer_class(
                instance,
                data=request.data,
                partial=False,
            )
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()

            return self.handle_message_response(
                message=f"{updated_instance} Actualizado satisfactoriamente",
                status_code=status.HTTP_200_OK,
                data=self.serializer_class(updated_instance).data,
            )

        except Exception as e:
            return self.handle_message_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                data=[],
            )

    @action(
        detail=False,
        methods=['post'],
        url_path='reset-password',
        serializer_class=PasswordResetByEmailBirthdaySerializer,
    )
    def reset_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        birthdate = serializer.validated_data['birthdate']
        new_password = serializer.validated_data['new_password']
        try:
            user = UserModel.objects.get(email=email, birthdate=birthdate)
        except UserModel.DoesNotExist:
            return self.handle_message_response(
                message="Usuario no encontrado",
                status_code=status.HTTP_404_NOT_FOUND,
                data=[]
            )

        user.set_password(new_password)
        user.save()

        return self.handle_message_response(
            message="Contraseña actualizada correctamente.",
            status_code=status.HTTP_200_OK,
            data=[]
        )
    
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        serializer = EmailAuthTokenSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        refresh_str = str(refresh)

        payload = {
            'access': access,
            'refresh': refresh_str,
            'user_name': user.name,
            'user_id': user.id,
            'email': user.email,
        }

        return self.handle_message_response(
            message='Usuario autenticado',
            status_code=status.HTTP_200_OK,
            data=payload,
        )

    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return self.handle_message_response(
                message="Debe enviar el campo 'refresh' con el token.",
                status_code=status.HTTP_400_BAD_REQUEST,
                data=[],
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return self.handle_message_response(
                message='Logout exitoso. Refresh token invalidado.',
                status_code=status.HTTP_200_OK,
                data=[],
            )

        except Exception as e:
            return self.handle_message_response(
                message=f"Error invalidando token: {str(e)}",
                status_code=status.HTTP_400_BAD_REQUEST,
                data=[],
            )

    @action(detail=False, methods=['get'], url_path='validate-token')
    def validate_token(self, request):
        auth = JWTAuthentication()
        user, token = auth.authenticate(request)
        resp = Response(status=status.HTTP_200_OK)
        resp['X-User-ID'] = str(user.id)
        resp['X-User-Email'] = user.email
        resp['X-User-Name'] = user.name
        return resp
