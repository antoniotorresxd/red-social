# publications/views.py
import requests
from datetime import datetime
from django.utils import timezone

from django.conf import settings
from django.core.cache import cache

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action

from .models import Publication, Submission
from .serializers import PublicationSerializer, SubmissionSerializer

from rest_framework.parsers import MultiPartParser, FormParser

class PublicationViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = PublicationSerializer
    queryset = Publication.objects.all().order_by('-timestamp')

    @staticmethod
    def handle_message_response(message: str, status_code: int, data=[]):
        return Response({
            'data': data,
            'message': message,
            'status_code': status_code,
        }, status=status_code)

    def get_queryset(self):
        qs = Publication.objects.all()
        tipo = self.request.query_params.get('type')
        community_id = self.request.query_params.get('community_id')
        user_id = self.request.query_params.get('user_id')
        ordering = self.request.query_params.get('ordering')

        if tipo:
            qs = qs.filter(type=tipo)
        if community_id:
            qs = qs.filter(community_id=community_id)
        if user_id:
            qs = qs.filter(user_id=user_id)
        if ordering:
            qs = qs.order_by(ordering)

        return qs

    def list(self, request, *args, **kwargs):
        try:
  
            queryset = self.get_queryset()[:10]
            data = self.serializer_class(queryset, many=True).data

            user_ids = {pub['user_id'] for pub in data}
            if user_ids:
                ids_param = ",".join(map(str, user_ids))
                cache_key = f"users_batch_{ids_param}"

                users = cache.get(cache_key)
                if users is None:

                    auth_header = request.headers.get("Authorization")
                    headers = {}
                    if auth_header:
                        headers["Authorization"] = auth_header

                    resp = requests.get(
                        f"{settings.API_GATEWAY_URL}/microservice-users/",
                        params={"ids": ids_param},
                        headers=headers,
                        timeout=2
                    )
                    resp.raise_for_status()

                    body = resp.json()
                    users_list = body.get("data", body) if isinstance(body, dict) else body
                    users = {u["id"]: u for u in users_list}

                    cache.set(cache_key, users, timeout=300)

                for pub in data:
                    user = users.get(pub["user_id"])
                    pub["user_name"] = user["name"] if user else None

            return self.handle_message_response(
                message="Publicaciones encontradas",
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
            instance = get_object_or_404(Publication, pk=pk)
            serializer = self.serializer_class(instance)
            return self.handle_message_response(
                message="Publicación encontrada",
                status_code=status.HTTP_200_OK,
                data=serializer.data
            )
        except Exception as e:
            return self.handle_message_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request, *args, **kwargs):
        try:
            user_id = request.headers.get('X-User-Id')
            data = request.data.copy()
            if user_id:
                data['user_id'] = user_id

            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.handle_message_response(
                message="Registrado satisfactoriamente",
                status_code=status.HTTP_201_CREATED,
                data=serializer.data
            )
        except Exception as e:
            return self.handle_message_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


    @action(detail=False, methods=['post'], url_path='submit-task')
    def submit_task(self, request):
        try:
            user_id = request.headers.get('X-User-Id')
            task_id = request.data.get('task')

            if not task_id:
                return self.handle_message_response(
                    message="El campo 'task' es obligatorio.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            task = Publication.objects.filter(id=task_id, type='task').first()
            if not task:
                return self.handle_message_response(
                    message="No se encontró la tarea o no es válida.",
                    status_code=status.HTTP_404_NOT_FOUND
                )

            now = timezone.now()
            is_late = task.due_date and now > task.due_date

            submission = Submission.objects.create(
                task=task,
                user_id=user_id,
                file=request.FILES['file'],
                submitted_at=now,
                is_late=is_late,
                reviewed=False
            )

            serializer = SubmissionSerializer(submission)
            return self.handle_message_response(
                message="Tarea enviada correctamente",
                status_code=status.HTTP_201_CREATED,
                data=serializer.data
            )
        except Exception as e:
            return self.handle_message_response(
                message=f"Error al enviar la tarea: {str(e)}",
                status_code=status.HTTP_400_BAD_REQUEST
            )