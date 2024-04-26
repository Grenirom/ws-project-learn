from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from config.tasks import send_confirmation_email_task
from .serializers import UserSerializer, RegistrationSerializer

User = get_user_model()


class UserViewSet(ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    @action(['POST'], detail=False)
    def register(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        print(request.data, 'code from request.data')
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.create_activation_code()

        if user:
            try:
                send_confirmation_email_task.delay(user.email, user.activation_code)
            except Exception as e:
                return Response({'msg': 'Зарегестрирован, но возникли неполадки с email!',
                                 'data': serializer.data}, status=201)
        return Response(serializer.data, status=201)

    @action(['GET'], detail=False, url_path='activate/(?P<uuid>[0-9A-Fa-f-]+)')
    def activate(self, request, uuid):
        print(uuid, '111111111111')
        try:
            user = User.objects.get(activation_code=uuid)
        except Exception as e:
            print(e, '1111111111')
            return Response({'msg': 'Ссылка недействительна, или уже открыта!'}, status=400)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response({'msg': 'Аккаунт успешно активирован!'}, status=200)


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny, )


class RefreshView(TokenRefreshView):
    permission_classes = (AllowAny, )