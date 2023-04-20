# pylint: disable=C0114
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import render, redirect

from fine.forms import EditProfile, InterestsForm
from fine.forms import RegistrationForm
from fine.models import RegistrationEvents, User, Interests, Friends
from django.contrib.auth.decorators import login_required
from fine.forms import RegistrationForm, CreateEvent
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

    try:
        friend = Friends.objects.get(from_user=request.user, to_user=User.objects.get(id=code))
        context['waiting_friend'] = friend.waiting

    except Friends.DoesNotExist:
        context['already_friend'] = False

    try:
        Friends.objects.get(from_user=User.objects.get(id=code), to_user=request.user, waiting=True)
        context['have_request'] = True
    except Friends.DoesNotExist:
        context['have_request'] = False


    if request.method == 'POST':
        if request.POST.get('friend_button'):
            Friends.objects.create(from_user=request.user, to_user=User.objects.get(id=code), waiting=True)
        if request.POST.get('del_request'):
            Friends.objects.get(from_user=request.user, to_user=User.objects.get(id=code)).delete()
        if request.POST.get('del_friend'):
            Friends.objects.get(from_user=request.user, to_user=User.objects.get(id=code)).delete()
            Friends.objects.get(from_user=User.objects.get(id=code), to_user=request.user).delete()
        if request.POST.get('acp_friend'):
            Friends.objects.create(to_user=User.objects.get(id=code), from_user=request.user, waiting=False)
            Friends.objects.filter(id=Friends.objects.get(to_user=request.user, from_user=code).id).update(waiting=False)

        return redirect('/profile/' + str(code))


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


def get_user(registration_event: RegistrationEvents) -> User:
    return registration_event.user

@login_required
def event_page(request: WSGIRequest, event_id: int):
    context = {
        'pagename': 'Profile Editing',
        'menu': get_menu_context(),
    }
    try:
        event: Event = list(Event.objects.filter(id=int(event_id)))[0]
        people: list[RegistrationEvents] = list(RegistrationEvents.objects.filter(event=int(event_id)))
        people: list[User] = list(map(get_user, people))
        event.description = "adada " * 1000
        context['event'] = event
        context['friends'] = people * 2
        context['people'] = people * 5
    except IndexError:
        return render(request, 'pages/does_not_found.html', context)
    return render(request, 'pages/main/event.html', context)



@login_required
def friends_page(request):
    """
    Страница с друзьями пользователя
    """
    context = {
        'pagename': 'Friends',
        'menu': get_menu_context(),
        'friends': Friends.objects.filter(to_user=request.user, waiting=False),
        'friends_request_to_user': Friends.objects.filter(to_user=request.user, waiting=True),
        'friends_request_by_user': Friends.objects.filter(from_user=request.user, waiting=True),
    }
    context['friends_size'] = len(context['friends'])
    context['friends_request_to_user_size'] = len(context['friends_request_to_user'])
    context['friends_request_by_user_size'] = len(context['friends_request_by_user'])

    if request.method == 'POST':
        if request.POST.get('cancel_to_request'):
            Friends.objects.get(id=request.POST.get('cancel_to_request')).delete()

        if request.POST.get('accept_from_request'):
            friend = Friends.objects.get(id=request.POST.get('accept_from_request'))
            Friends.objects.create(to_user=friend.from_user, from_user=request.user, waiting=False)
            Friends.objects.filter(id=request.POST.get('accept_from_request')).update(waiting=False)

        if request.POST.get('cancel_from_request'):
            Friends.objects.get(id=request.POST.get('cancel_from_request')).delete()

        if request.POST.get('del_friend'):
            friend = Friends.objects.get(id=request.POST.get('del_friend'))
            Friends.objects.get(to_user=friend.to_user, from_user=friend.from_user).delete()
            Friends.objects.get(to_user=friend.from_user, from_user=friend.to_user).delete()

        return redirect('/friends/')

    return render(request, 'pages/friends/friends.html', context)