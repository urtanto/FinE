# pylint: disable=C0114
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from fine.froms import RegistrationForm, CreateEvent
from fine.models import RegistrationEvents, User, Interests, Event
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


def cheack_for_none(user_id, model):
    try:
        temp = model.objects.get(user=user_id)
        return temp
    except model.DoesNotExist:
        return None


@login_required
def event_create_page(request):
    """
    Функция по созданию ивента
    """
    context = {'pagename': 'CreateEvent', 'menu': get_menu_context()}
    if request.method == 'POST':
        form = CreateEvent(request.POST)
        if form.is_valid():
            event = Event(name=form.cleaned_data['name'],
                          type=form.cleaned_data['type'],
                          address=form.cleaned_data['address'],
                          status=form.cleaned_data['status'], start_day=form.cleaned_data['start_day'],
                          finish_day=form.cleaned_data['finish_day'], description=form.cleaned_data['description'],
                          entertainment_type=form.cleaned_data['entertainment_type'],
                          author=request.user)
            event.save()
            return redirect('/')
        else:
            pass
    else:
        form = CreateEvent()
    context['form'] = form
    return render(request, 'pages/event/create.html', context)


@login_required
def event_edit_page(request: WSGIRequest, event_id: int):
    """
    Функция по изменению ивента
    """
    context = {'pagename': 'EditEvent', 'menu': get_menu_context(), 'event_id': event_id}
    event = Event.objects.get(pk=event_id)
    form = CreateEvent(request.POST, instance=event)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, 'pages/event/edit.html', context)


def profile_view_page(request: WSGIRequest, code: int):
    """
    Профиль пользователя
    """
    context = {'pagename': 'Profile',
               'menu': get_menu_context()}
    try:
        context['user'] = User.objects.get(id=code)  # все поля из модели для пользователя с id = code
        context['events'] = cheack_for_none(code, RegistrationEvents)  # ивенты, на которые зарегался пользователь
        context['interests'] = cheack_for_none(code, Interests)  # интересы пользователя
    except User.DoesNotExist:
        context['events'] = None
        context['interests'] = None
        raise Http404

    return render(request, 'pages/profile/view.html', context)
