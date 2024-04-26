from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from apps.account import facebook_login_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('apps.account.urls')),
    path('select_related/', include('apps.select_related.urls')),
    path('login/', facebook_login_views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth', include('social_django.urls', namespace='social')),
    path('', facebook_login_views.home, name='home'),
    path("__debug__", include("debug_toolbar.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
