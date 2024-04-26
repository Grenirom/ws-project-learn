from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register('', views.UserViewSet)

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('refresh/', views.RefreshView.as_view()),
    path('', include(router.urls)),
]

