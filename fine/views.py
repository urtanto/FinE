# pylint: disable=C0114
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import render, redirect

from fine.forms import EditProfile, InterestsForm, RegistrationForm, CreateEvent
from django.contrib.auth.decorators import login_required
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


INTERESTS = {
    0: 'Спорт',
    1: 'Квесты',
    2: 'Видеоигры',
    3: 'Фильмы'
}


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
                          start_day=form.cleaned_data['start_day'],
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
    form = CreateEvent(instance=event)
    if request.method == 'POST':
        form = CreateEvent(request.POST, instance=event)
        if form.is_valid():
            form.save()
    context['form'] = form
    return render(request, 'pages/event/edit.html', context)


@login_required
def commit_event_page(request, event_id):
    """
    Добавляет пользователя в мероприятие
    """
    context = {'pagename': 'Commit Event', 'menu': get_menu_context(), 'event_id': event_id}
    event = Event.objects.get(pk=event_id)
    request.user.events.add(event)
    return render(request, 'pages/start/index.html', context)


def profile_view_page(request: WSGIRequest, code: int):
    """
    Профиль пользователя
    """
    context = {'pagename': 'Profile',
               'menu': get_menu_context(),
               'cur_user': request.user}
    try:
        context['user'] = User.objects.get(id=code)  # все поля из модели для пользователя с id = code
        context['events'] = RegistrationEvents.objects.filter(user=code)  # ивенты, на которые зарегался пользователь

        context['interests'] = []  # интересы пользователя
        Interests.objects.filter(user=code).values_list('interest', flat=True)
        for i in Interests.objects.filter(user=code).values_list('interest', flat=True):
            context['interests'].append(INTERESTS[i])


    except User.DoesNotExist:
        context['events'] = None
        context['interests'] = None
        raise Http404

    return render(request, 'pages/profile/view.html', context)


@login_required
def edit_page(request):
    """
    Редактирование Профиля
    """
    context = {
        'pagename': 'Profile Editing',
        'menu': get_menu_context(),
        'user': request.user
    }

    cur_user = User.objects.get(username=request.user.username)
    form = EditProfile(instance=cur_user)

    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=cur_user)
        if form.is_valid():
            form.save()
        return redirect('/profile/' + str(request.user.id))
    context['form'] = form

    return render(request, 'pages/profile/edit_about.html', context)


def to_fit(arr, size, request):
    if len(arr) > size:
        for i in range(len(arr) - size):
            arr[i].delete()
    elif len(arr) < size:
        for i in range(size - len(arr)):
            arr.create(user=request.user, interest=0)


@login_required
def edit_interests_page(request):
    context = {
        'pagename': 'Profile Editing',
        'menu': get_menu_context(),
    }
    if request.method == 'POST':
        form = InterestsForm(request.POST)
        if form.is_valid():
            interests = form.cleaned_data.get('Interests')
            context['interests'] = interests

            cur_interests = User.objects.get(id=request.user.id).interests_set.all()
            to_fit(cur_interests, len(interests), request)

            counter = 0
            for i in cur_interests.values_list('id', flat=True):
                Interests.objects.filter(id=i).update(interest=int(interests[counter]))
                counter += 1
            context['cur_interests'] = cur_interests

            return redirect('/profile/' + str(request.user.id))
    else:
        form = InterestsForm
    context['form'] = form

    return render(request, 'pages/profile/edit_interests.html', context)
