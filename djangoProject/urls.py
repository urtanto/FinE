"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from djangoProject import settings
from fine import views
from fine.views import get_menu_context

urlpatterns = [
    path('', views.index_page, name='index'),
    path('admin/', admin.site.urls),
    path('profile/<int:code>', views.profile_view_page, name='profile'),
    path('login/',
         auth_views.LoginView.as_view(
             extra_context={
                 'menu': get_menu_context(),
                 'pagename': 'Авторизация'
             }
         ),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('event/create/', views.event_create_page, name='create'),
    path('event/edit/<int:event_id>', views.event_edit_page, name='event_edit'),
    path('registration/', views.registration_page, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
