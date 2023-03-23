# pylint: disable=C0114
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import render

from fine.models import RegistrationEvents, User, Interests


def get_menu_context():
    """
    Функция для возвращения контекста меню

    :return: контекст меню
    """
    return [
        {'url_name': 'index', 'name': 'Меню'},
        {'url_name': 'index', 'name': 'Мои голосования'},
    ]


def index_page(request: WSGIRequest):
    """
    Функция обрабатывающая запрос /
    """
    context = {
        'pagename': 'Simple voting',
        'menu': get_menu_context()
    }
    return render(request, 'pages/start/index.html', context)


def cheack_for_none(user_id, model):
    """
    Надо

    :param user_id:
    :param model:
    :return:
    """
    try:
        temp = model.objects.get(user=user_id)
        return temp
    except model.DoesNotExist:
        return None


def profile_view_page(request: WSGIRequest, code: int):
    """
    Профиль пользователя
    """
    context = {'pagename': 'Profile',
               'menu': get_menu_context()}
    try:
        context['user'] = User.objects.get(user_id=code)  # все поля из модели для пользователя с id = code
        context['events'] = cheack_for_none(code, RegistrationEvents)  # ивенты, на которые зарегался пользователь
        context['interests'] = cheack_for_none(code, Interests)  # интересы пользователя
    except User.DoesNotExist:
        context['events'] = None
        context['interests'] = None
        raise Http404

    return render(request, 'pages/profile/view.html', context)
