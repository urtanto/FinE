from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import render, redirect

from fine.forms import EditProfile, InterestsForm, RegistrationForm, CreateEvent, CreateGroup
from fine.models import RegistrationEvents, User, Interests, Friends, UserGroups
from fine.forms import EditProfile, InterestsForm, RegistrationForm, CreateEvent, SearchFriends
from django.contrib.auth.decorators import login_required
from fine.models import RegistrationEvents, User, Interests, Event, Friends
from django.contrib.auth.hashers import make_password, check_password
import json


def get_menu_context():
    """
    Функция для возвращения контекста меню

    :return: контекст меню
    """
    return [
        {'url_name': 'index', 'name': 'Меню'},
        {'url_name': 'index', 'name': 'Главная страница'},
    ]


def index_page(request: WSGIRequest):
    """
    Функция, обрабатывающая запрос.
    """
    context = {
        'pagename': 'FinE',
        'menu': get_menu_context(),
        "events": Event.objects.all()
    }
    return render(request, 'pages/start/index.html', context)


def registration_page(request: WSGIRequest):
    """
    Страница регистрации пользователя.
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
    Страница с созданием ивента.
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
    Cтраница изменения ивента.

    :param event_id: Event ID
    :type event_id: int
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
    Страница с добавлением пользователя на мероприятие.

    :param event_id: Event ID
    :type event_id: int
    """
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return redirect('/')
    request.user.events.add(event)
    return redirect('/')


def friends_for_profile_view_page_algo(request: WSGIRequest, code: int):
    """
    Набор алгоритмов для страницы профиля.

    :param request: Параметр запроса для POST-обработки.
    :type request: :class: 'django.http.HttpRequest'
    :param code: ID пользователя.
    :type event_id: int
    """
    if request.POST.get('button') == 'friend_button':
        Friends.objects.create(from_user=request.user, to_user=User.objects.get(id=code), waiting=True)
    elif request.POST.get('button') == 'del_request':
        Friends.objects.get(from_user=request.user, to_user=User.objects.get(id=code)).delete()
    elif request.POST.get('button') == 'del_friend':
        Friends.objects.get(from_user=request.user, to_user=User.objects.get(id=code)).delete()
        Friends.objects.get(from_user=User.objects.get(id=code), to_user=request.user).delete()
    elif request.POST.get('button') == 'acp_friend':
        Friends.objects.create(to_user=User.objects.get(id=code), from_user=request.user, waiting=False)
        Friends.objects.filter(id=Friends.objects.get(to_user=request.user, from_user=code).id).update(waiting=False)


def profile_view_page(request: WSGIRequest, code: int):
    """
    Страница профиля пользователя.

    :param code: ID пользователя
    :type code: int
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

    if request.user.is_authenticated:
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
        friends_for_profile_view_page_algo(request, code)

        return redirect('/profile/' + str(code))

    return render(request, 'pages/profile/view.html', context)


@login_required
def edit_page(request):
    """
    Страница редактирования основной информации профиля.
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
    """
    Функция для возвращения размера массива 'Интересов' к параметру :size.

    :param arr: Массив интересов.
    :param size: Размер будущего массива.
    :param request: Параметр запроса для POST-обработки.
    """
    if len(arr) > size:
        for i in range(len(arr) - size):
            arr[i].delete()
    elif len(arr) < size:
        for i in range(size - len(arr)):
            arr.create(user=request.user, interest=0)


@login_required
def edit_interests_page(request):
    """
    Страница с редактированием интересов пользователя.
    """
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


def friends_algo(request: WSGIRequest):
    """
    Набор алгоритмов для страницы с дрзьями.
    :param request: Параметр запроса для POST-обработки
    """
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


def get_user(received_object: RegistrationEvents | Friends) -> User:
    if isinstance(received_object, Friends):
        return received_object.from_user
    return received_object.user


@login_required
def event_page(request: WSGIRequest, event_id: int):
    context = {
        'pagename': 'Profile Editing',
        'menu': get_menu_context(),
    }
    try:
        event: Event = list(Event.objects.filter(id=int(event_id)))[0]
        if request.method == 'POST':
            print("*click*")
            data = json.loads(request.body)
            if data["going"]:
                RegistrationEvents.objects.get(event=event, user=request.user).delete()
            else:
                RegistrationEvents.objects.create(event=event, user=request.user)
        friends: list[Friends] = list(Friends.objects.filter(to_user=request.user, waiting=False))
        people: list[RegistrationEvents] = list(RegistrationEvents.objects.filter(event=event_id))
        friends: list[User] = list(map(get_user, friends))
        people: list[User] = list(map(get_user, people))
        event.description = "adada "
        context['event'] = event
        context['friends'] = friends
        context['people'] = people
        context['going'] = True if request.user in people else False
    except IndexError:
        return render(request, 'pages/does_not_found.html', context)
    return render(request, 'pages/main/event.html', context)


def get_friends(id: int):
    """
    Функция, возвращающая список друзей пользователя.
    :param id: ID пользователя
    :return: Список друзей
    """
    return Friends.objects.filter(to_user=User.objects.get(id=id), waiting=False)


@login_required
def search_friends(request):
    """
    Страница по поиску людей
    """
    context = {'pagename': 'Search friends', 'menu': get_menu_context(), 'users': User.objects.all(), 'users_size': 0}
    if request.method == 'POST':
        form = SearchFriends(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            friends = Friends.objects.filter(from_user_id=request.user)
            friends_id = [friend.to_user_id for friend in friends]

            users_search = (User.objects.filter(first_name__icontains=search) |
                            User.objects.filter(last_name__icontains=search) |
                            User.objects.filter(username__icontains=search))

            my_user = User.objects.exclude(id=request.user.id)

            users_friends = User.objects.exclude(id__in=friends_id)

            users = users_search & my_user & users_friends
            context['users'] = users
            context['users_size'] = len(users)
        else:
            pass
    else:
        form = SearchFriends()

    if request.POST.get('friend_button'):
        Friends.objects.create(from_user=request.user,
                               to_user=User.objects.get(id=request.POST.get('friend_button')), waiting=True)

    context['form'] = form
    return render(request, 'pages/friends/search_friends.html', context)


def friends_only_page(request):
    """
    Страница только с друзьями пользователя
    """
    context = {
        'pagename': 'Friends',
        'menu': get_menu_context(),
        'friends': Friends.objects.filter(to_user=request.user, waiting=False),
    }
    context['friends_size'] = len(context['friends'])

    if request.method == 'POST':
        if request.POST.get('del_friend'):
            friend = Friends.objects.get(id=request.POST.get('del_friend'))
            Friends.objects.get(to_user=friend.to_user, from_user=friend.from_user).delete()
            Friends.objects.get(to_user=friend.from_user, from_user=friend.to_user).delete()

        return redirect('/friends_only/')

    return render(request, 'pages/friends/friends_only_page.html', context)


@login_required
def friends_page(request):
    """
    Страница с друзьями пользователя
    """
    context = {
        'pagename': 'Friends',
        'menu': get_menu_context(),
        'friends': get_friends(request.user.id),
        'friends_request_to_user': Friends.objects.filter(to_user=request.user, waiting=True),
        'friends_request_by_user': Friends.objects.filter(from_user=request.user, waiting=True),
    }
    context['friends_size'] = len(context['friends'])
    context['friends_request_to_user_size'] = len(context['friends_request_to_user'])
    context['friends_request_by_user_size'] = len(context['friends_request_by_user'])

    if request.method == 'POST':
        friends_algo(request)

        return redirect('/friends/')

    return render(request, 'pages/friends/friends.html', context)


@login_required
def create_group_page(request):
    context = {
        'pagename': 'Create Group',
        'menu': get_menu_context(),
    }

    if request.method == 'POST':
        form = CreateGroup(request.POST)
        if form.is_valid():
            UserGroups.objects.create(title=form.cleaned_data['title'],
                                      description=form.cleaned_data['description'],
                                      founder=request.user)

            return redirect('/')
    else:
        form = CreateGroup()
    context['form'] = form

    return render(request, 'pages/groups/create_group.html', context)


@login_required
def groups_page(request):
    context = {
        'pagename': 'Groups',
        'menu': get_menu_context(),
        'groups': request.user.members.all(),  # группы, где пользователь состоит
        'my_groups': UserGroups.objects.filter(founder=request.user)  # группы, которыми владеет пользователь
    }

    return render(request, 'pages/groups/groups.html', context)


@login_required
def group_page(request, group_id: int):
    context = {
        'pagename': 'Group №' + str(group_id),
        'menu': get_menu_context(),
        'group': UserGroups.objects.get(id=group_id),
        'users': User.objects.filter(members__id=group_id)
    }
    if UserGroups.objects.get(id=group_id).founder.id is not request.user.id and\
            group_id not in request.user.members.all().values_list('id', flat=True):
        return redirect('/')

    return render(request, 'pages/groups/group.html', context)


@login_required
def add_to_group_page(request, group_id: int):
    context = {
        'pagename': 'Adding to Group №' + str(group_id),
        'menu': get_menu_context(),
        'group': UserGroups.objects.get(id=group_id),
        'users': User.objects.exclude(members__id=group_id) & User.objects.exclude(id=request.user.id),
        'group_id': group_id,
    }

    if UserGroups.objects.get(id=group_id).founder.id is not request.user.id:
        redirect('/')

    context['users_size'] = len(context['users'])
    if request.method == 'POST':
        form = SearchFriends(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']

            friends = Friends.objects.filter(from_user_id=request.user)
            friends_id = [friend.to_user_id for friend in friends]
            users_friends_all = User.objects.filter(id__in=friends_id)

            friends_group = User.objects.filter(members__id=group_id)
            friends_group_id = [friend.id for friend in friends_group]
            users_friends = User.objects.exclude(id__in=friends_group_id)

            my_user = User.objects.exclude(id=request.user.id)

            users_to_invite = my_user & users_friends_all & users_friends

            users_search = (User.objects.filter(first_name__icontains=search) |
                            User.objects.filter(last_name__icontains=search) |
                            User.objects.filter(username__icontains=search))

            users = users_search & users_to_invite
            context['users'] = users
            context['users_size'] = len(users)
        else:
            pass
    else:
        form = SearchFriends()
    context['form'] = form

    if request.method == 'POST':
        if request.POST.get('invite'):
            invented = Friends.objects.get(from_user_id=request.POST.get('invite'))
            invented = User.objects.get(id=invented.from_user_id)
            invented.members.add(context['group'])
            return redirect('/group/add_to_group/' + str(context['group_id']))

    return render(request, 'pages/groups/add_to_group.html', context)
