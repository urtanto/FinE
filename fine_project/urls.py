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

from fine_project import settings
from fine import views
from fine.views import get_context

context_for_login = get_context(page_name="Авторизация", active="/login/")
context_for_login["menu"]["right"]["unauthorized"][1] = {'url_name': '/login/', 'name': 'Войти'}
urlpatterns = [
    path('', views.index_page, name='index'),
    path('admin/', admin.site.urls),
    path('profile/<int:code>', views.profile_view_page, name='profile'),
    path('login/',
         auth_views.LoginView.as_view(
             extra_context=context_for_login
         ),
         name='login'),
    path('registration/', views.registration_page, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('menu/', views.menu_page, name='menu'),
    path('menu/event/create/', views.event_create_page, name='event_create'),
    path('menu/event/edit/<int:event_id>', views.event_edit_page, name='event_edit'),
    path('menu/event/commit/<int:event_id>', views.commit_event_page, name='event_commit'),
    path('profile/edit/about', views.edit_page, name='edition_about'),
    path('profile/edit/interests', views.edit_interests_page, name='edition_interests'),
    path('menu/event/<int:event_id>', views.event_page, name='event'),
    path('friends/', views.friends_page, name='friends'),
    path('search_friends/', views.search_friends, name='search_friends'),
    path('friends_only/', views.friends_only_page, name='friends_only'),
    path('groups/create_group/', views.create_group_page, name='create_group'),
    path('groups/', views.groups_page, name='groups'),
    path('groups/group/<int:group_id>', views.group_page, name='group'),
    path('groups/group/add_to_group/<int:group_id>', views.add_to_group_page, name='add_to_group'),
    path('groups/group/remove_from_the_group/<int:group_id>',
         views.remove_from_the_group_page, name='remove_from_the_group'),
    path('theme/change/', views.theme_change),
    path('profile/my_reports/report/<int:report_id>', views.report_page, name='report'),
    path('profile/my_reports/', views.my_reports_page, name='my_reports'),
    path('profile/my_reports/create_report/', views.create_report_page, name='create_report'),
    path('verify_reports/', views.unverifed_reports_page, name='uncheacked_reports'),
    path('verify_reports/report/<int:report_id>', views.verify_report_page, name='verify_report'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
