from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import CommunitySerializer
from .models import Community as Communitymodel


class CommunityViewSet(viewsets.GenericViewSet):
    serializer_class = CommunitySerializer
    queryset = Communitymodel.objects.none()
        
    @staticmethod
    def handle_message_response(message: str, status_code: int, data = []):
        return Response({
            'data': data,
            'message': message,
            'status_code': status_code,
        }, status=status_code)
    
    def list(self, request):
        try:
            raw = request.META.get('HTTP_X_USER_ID')
            if not raw:
                return self.handle_message_response(
                    message="No se encontró X-User-ID en la petición",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    data=[]
                )
            user_id = int(raw)

            tipo = request.query_params.get('type')
            name = request.query_params.get('name', '').strip()
            join = request.query_params.get('join', False)

            qs = Communitymodel.objects.all()

            if tipo:
                qs = qs.filter(type=tipo)

            if name:
                qs = qs.filter(name__icontains=name)

            if not join:
                qs = qs.filter(list_users__contains=[user_id])

            qs = qs.order_by('-id')[:10]
            data = CommunitySerializer(qs, many=True).data

            return self.handle_message_response(
                message="Comunidades Filtradas",
                status_code=status.HTTP_200_OK,
                data=data
            )

        except Exception as e:
            return self.handle_message_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        try:
            instance = get_object_or_404(Communitymodel, id=pk)
            serializer = self.serializer_class(instance)

            return self.handle_message_response(
                f"Comunidad encontrada",
                status.HTTP_200_OK,
                serializer.data
            )
        except Exception as e:
            return self.handle_message_response(
                str(e), status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'], url_path='create')
    def register(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            user_id = request.headers['X-User-Id']

            if serializer.is_valid():
                type_ = serializer.validated_data.get('type')

                if type_ == 'group':
                    code = Communitymodel.generate_code()
                    instance = serializer.save(code=code)
                else:
                    instance = serializer.save()
                
                instance.join_community(user_id)
                instance_data = self.serializer_class(instance).data

                return self.handle_message_response(
                    message=f"{instance} Registrado satisfactoriamente",
                    status_code=status.HTTP_201_CREATED,
                    data=instance_data,
                )

            return self.handle_message_response(
                message=str(serializer.errors),
                status_code=status.HTTP_400_BAD_REQUEST,
                data=[]
            )

        except Exception as e:
            return self.handle_message_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                data=[]
            )

    @action(detail=False, methods=['post'], url_path='join')
    def join(self, request):
        raw_user = request.headers.get('X-User-Id')
        if not raw_user:
            return self.handle_message_response(
                message="X-User-Id header missing",
                status_code=status.HTTP_401_UNAUTHORIZED,
                data=[]
            )
        try:
            user_id = int(raw_user)
        except ValueError:
            return self.handle_message_response(
                message="X-User-Id must be an integer",
                status_code=status.HTTP_400_BAD_REQUEST,
                data=[]
            )

        type_ = request.data.get('type')
        if type_ not in {'group', 'forum'}:
            return self.handle_message_response(
                message="Invalid 'type'; must be 'group' or 'forum'",
                status_code=status.HTTP_400_BAD_REQUEST,
                data=[]
            )

        filters = {'type': type_}
        if type_ == 'group':
            code = request.data.get('code')
            if not code:
                return self.handle_message_response(
                    message="Missing 'code' for joining a group",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    data=[]
                )
            filters['code'] = code

        else:
            comm_id   = request.data.get('id')
            comm_name = request.data.get('name')
            if comm_id:
                filters['pk'] = comm_id
            elif comm_name:
                filters['name'] = comm_name
            else:
                return self.handle_message_response(
                    message="Provide 'id' or 'name' to join a forum",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    data=[]
                )

        try:
            community = Communitymodel.objects.get(**filters)
        except Communitymodel.DoesNotExist:
            return self.handle_message_response(
                message="Community not found",
                status_code=status.HTTP_404_NOT_FOUND,
                data=[]
            )
        
        community.join_community(user_id)

        data = self.serializer_class(community).data
        return self.handle_message_response(
            message=f"Joined '{community.name}' successfully",
            status_code=status.HTTP_200_OK,
            data=data
        )

    def destroy(self, request, pk=None):
        """
        Elimina una comunidad solo si el usuario autenticado es el admin de la comunidad.
        """
        try:
            community = get_object_or_404(Communitymodel, id=pk)
            raw_user = request.headers.get('X-User-Id')
            if not raw_user:
                return self.handle_message_response(
                    message="X-User-Id header missing",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    data=[]
                )
            try:
                user_id = int(raw_user)
            except ValueError:
                return self.handle_message_response(
                    message="X-User-Id must be an integer",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    data=[]
                )

            if community.admin_id != user_id:
                return self.handle_message_response(
                    message="Solo el administrador puede eliminar la comunidad.",
                    status_code=status.HTTP_403_FORBIDDEN,
                    data=[]
                )

            community.delete()

            return self.handle_message_response(
                message="Comunidad eliminada correctamente.",
                status_code=status.HTTP_200_OK,
                data=[]
            )

        except Exception as e:
            return self.handle_message_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                data=[]
            )
        
    @action(detail=True, methods=['post'], url_path='exit')
    def exit_community(self, request, pk=None):
        """
        Permite que un usuario (no admin) salga de la comunidad.
        El admin NO puede salirse si es el único admin.
        """
        try:
            community = get_object_or_404(Communitymodel, id=pk)
            raw_user = request.headers.get('X-User-Id')
            if not raw_user:
                return self.handle_message_response(
                    message="X-User-Id header missing",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    data=[]
                )
            try:
                user_id = int(raw_user)
            except ValueError:
                return self.handle_message_response(
                    message="X-User-Id must be an integer",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    data=[]
                )

            if user_id == community.admin_id:
                return self.handle_message_response(
                    message="El administrador no puede salir. Solo puede eliminar la comunidad.",
                    status_code=status.HTTP_403_FORBIDDEN,
                    data=[]
                )

            community.exit_community(user_id)

            return self.handle_message_response(
                message="Has salido de la comunidad.",
                status_code=status.HTTP_200_OK,
                data=[]
            )
        except Exception as e:
            return self.handle_message_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                data=[]
            )