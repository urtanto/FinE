# pylint: disable=C0114
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import render, redirect

from fine.forms import EditProfile
from fine.froms import RegistrationForm
from fine.models import RegistrationEvents, User, Interests
from django.contrib.auth.hashers import make_password, check_password


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


def registration_page(request: WSGIRequest):
    """
    Страница регистрации
    """
    context = {'pagename': 'Регистрация'}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(username=form.cleaned_data['username'], password=make_password(form.cleaned_data['password2']),
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                        email=form.cleaned_data['email'])
            user.save()
            return redirect('/')
        else:
            pass
    else:
        form = RegistrationForm()
    context['form'] = form

    return render(request, 'registration/register.html', context)


def cheack_for_none(user, model):
    try:
        temp = model.objects.get(user=user)
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
        context['user'] = User.objects.get(id=code)  # все поля из модели для пользователя с id = code
        context['events'] = cheack_for_none(code, RegistrationEvents)  # ивенты, на которые зарегался пользователь
        context['interests'] = cheack_for_none(code, Interests)  # главный интерес пользователя
    except User.DoesNotExist:
        context['events'] = None
        context['interests'] = None
        raise Http404

    return render(request, 'pages/profile/view.html', context)

INTERESTS = {
    0: 'Спорт',
    1: 'Квесты',
    2: 'Видеоигры',
    3: 'Фильмы'
}

@login_required
def edit_page(request):
    """
    Редактирование Профиля
    """
    context = {
        'pagename': 'Profile Editing',
        'interests':  INTERESTS.items(),
        'menu': get_menu_context(),
    }

    cur_user = User.objects.get(username=request.user.username)
    form = EditProfile(instance=cur_user)

    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=cur_user)
        if form.is_valid():
            form.save()

        if request.POST.get('select') is not None:
            Interests.objects.update_or_create(user=request.user,
                                           defaults={'interest': request.POST.get('select')})
            User.Interest

        return redirect('/profile/' + str(request.user.id))
    context['form'] = form

    return render(request, 'pages/profile/edit.html', context)