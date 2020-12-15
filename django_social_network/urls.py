from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from .views import home_view
from profiles.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='profiles/login.html', redirect_authenticated_user=True),
         name='login-view'),
    path('logout/', auth_views.LogoutView.as_view(template_name='profiles/logout.html'), name='logout-view'),
    path('register/', register, name='register-view'),
    path('profile/', include('profiles.urls')),
    path('posts/', include('posts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
