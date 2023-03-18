from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render


def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Меню'},
        {'url_name': 'index', 'name': 'Мои голосования'},
    ]


def index_page(request: WSGIRequest):
    context = {
        'pagename': 'Simple voting',
        'menu': get_menu_context()
    }
    return render(request, 'pages/index.html', context)

