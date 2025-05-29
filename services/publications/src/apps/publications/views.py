# publications/views.py
import requests
from django.utils import timezone

from django.conf import settings
from django.core.cache import cache

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action

from .models import Publication, Submission, Comment
from .serializers import CommentSerializer, PublicationSerializer, SubmissionSerializer

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

    def _inject_user_names(self, items: list, key='user_id') -> list:
        user_ids = {item[key] for item in items if item.get(key)}
        if not user_ids:
            return items

        users = {}
        ids_missing = []

        for uid in user_ids:
            cached = cache.get(f"user_{uid}")
            if cached:
                users[uid] = cached
            else:
                ids_missing.append(uid)

        if ids_missing:
            ids_param = ",".join(map(str, ids_missing))
            headers = {}
            auth_header = self.request.headers.get("Authorization")
            if auth_header:
                headers["Authorization"] = auth_header

            try:
                resp = requests.get(
                    f"{settings.API_GATEWAY_URL}/microservice-users/",
                    params={"ids": ids_param},
                    headers=headers,
                    timeout=2
                )
                resp.raise_for_status()
                body = resp.json()
                users_list = body.get("data", body) if isinstance(body, dict) else body

                for u in users_list:
                    uid = u["id"]
                    users[uid] = u
                    cache.set(f"user_{uid}", u, timeout=300)

            except Exception:
                pass 

        for item in items:
            user = users.get(item.get(key))
            item["user_name"] = user.get("name") if user else None

        return items

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

            data = self._inject_user_names(data)

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

    @action(detail=True, methods=['post'], url_path='add-comment')
    def add_comment(self, request, pk=None):
        try:
            user_id = request.headers.get('X-User-Id')
            content = request.data.get('content')

            if not content:
                return self.handle_message_response(
                    message="El comentario no puede estar vacío.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            post = get_object_or_404(Publication, pk=pk)

            comment = Comment.objects.create(
                post=post,
                user_id=user_id,
                content=content,
                timestamp=timezone.now()
            )

            serializer = CommentSerializer(comment)
            return self.handle_message_response(
                message="Comentario agregado correctamente",
                status_code=status.HTTP_201_CREATED,
                data=serializer.data
            )
        except Exception as e:
            return self.handle_message_response(
                message=f"Error al agregar comentario: {str(e)}",
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'], url_path='comments')
    def list_comments(self, request, pk=None):
        try:
            post = get_object_or_404(Publication, pk=pk)
            comments = Comment.objects.filter(post=post).order_by('timestamp')[:5]
            serialized = CommentSerializer(comments, many=True).data
            enriched = self._inject_user_names(serialized)
            return self.handle_message_response(
                message="Comentarios listados correctamente",
                status_code=status.HTTP_200_OK,
                data=enriched
            )
        except Exception as e:
            return self.handle_message_response(
                message=f"Error al listar comentarios: {str(e)}",
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'], url_path='submissions')
    def list_submissions(self, request, pk=None):
        try:
            task = get_object_or_404(Publication, pk=pk, type='task')
            submissions = Submission.objects.filter(task=task)
            serialized = SubmissionSerializer(submissions, many=True).data

            enriched = self._inject_user_names(serialized)
            return self.handle_message_response(
                message="Entregas listadas correctamente",
                status_code=status.HTTP_200_OK,
                data=enriched
            )
        except Exception as e:
            return self.handle_message_response(
                message=f"Error al listar entregas: {str(e)}",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
    @action(detail=True, methods=['post'], url_path=r'submissions/(?P<submission_id>[^/.]+)/grader')
    def grade_submission(self, request, pk=None, submission_id=None):
        try:

            task = get_object_or_404(Publication, pk=pk, type='task')

            submission = get_object_or_404(Submission, pk=submission_id, task=task)

            grade = request.data.get('grade')
            if grade is None:
                return self.handle_message_response(
                    message="El campo 'grade' es obligatorio.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            try:
                grade = int(grade)
            except ValueError:
                raise ValueError("La calificación debe ser un número entero.")
            if not (0 <= grade <= 10):
                raise ValueError("La calificación debe estar entre 0 y 10.")

            submission.grade = grade
            submission.reviewed = True

            submission.save()

            serializer = SubmissionSerializer(submission)
            return self.handle_message_response(
                message="Calificación registrada correctamente",
                status_code=status.HTTP_200_OK,
                data=serializer.data
            )
        except ValueError as ve:
            return self.handle_message_response(
                message=str(ve),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return self.handle_message_response(
                message=f"Error al calificar la tarea: {str(e)}",
                status_code=status.HTTP_400_BAD_REQUEST
            )