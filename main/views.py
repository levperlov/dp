from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect

from main.forms import LoginForm, AddNewsForm, GetNewsForm, YaCalcForm
from main.models import News
import math   # needed for yacalc page


def get_base_context(request, pagename):
    return {
        'pagename': pagename,
        'loginform': LoginForm(),
        'user': request.user,
    }


def index_page(request):
    context = get_base_context(request, 'DangerHome')
    return render(request, 'pages/index.html', context)


@login_required(login_url='/login/')
def add_news_page(request):
    context = get_base_context(request, 'Добавление новой новости')
    user = request.user
    if request.POST:
        form = AddNewsForm(request.POST)
        if form.is_valid():
            news = News(
                author=user,
                name=form.data['name'],
                content=form.data['content'],
                is_public='is_public' in form.data and form.data['is_public'] == 'on',
                added_date=datetime.now()
            )
            news.save()
            messages.add_message(request, messages.SUCCESS, "Новость успешно добавлена")
            return redirect('feed')
        else:
            messages.add_message(request, messages.ERROR, "Ошибка добавления новости")
    else:
        form = AddNewsForm(request.POST)
    context['form'] = form
    return render(request, 'pages/add.html', context)

# SELECT * FROM 'main_news' where (is_public='1' and name like '%{0}%')
# SELECT * FROM 'main_news' where (is_public='1' and name like '%'%')
@login_required(login_url='/login/')
def search_page(request):
    context = get_base_context(request, 'Поиск новостей')
    if request.GET:
        form = GetNewsForm(request.GET)
        if form.is_valid():
            News.objects.filter(name__contains=form.data['name'], is_public=True)
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM 'main_news' where (is_public='1' and name like '%{0}%')".format(form.data['name'])
            )
            result = [  # Переупаковываем из tuple в list
                [field for field in item] for item in cursor.fetchall()
            ]
            for item in result:
                item[-1] = User.objects.get(id=item[-1])              # Добавляем объекты юзеров вместо author_id
            context['result'] = result
        else:
            messages.add_message(request, messages.ERROR, "Ошибка поиска новостей")
    else:
        form = GetNewsForm()
    context['form'] = form
    return render(request, 'pages/search.html', context)


def feed_page(request):
    context = get_base_context(request, 'Просмотр новостей')
    context['public_news'] = News.objects.filter(is_public=True)
    if request.user.is_authenticated:
        context['my_news'] = News.objects.filter(author=request.user)
        context['public_news'] = context['public_news'].exclude(author=request.user)
    return render(request, 'pages/feed.html', context)


def yacalc_page(request):
    context = get_base_context(request, 'Вычисление сложных математических выражений')
    if request.GET:
        form = YaCalcForm(request.GET)
        if form.is_valid():
            context['result'] = eval(form.data['expression'])
        else:
            messages.add_message(request, messages.ERROR, "Ошибка формата выражения")
    else:
        form = YaCalcForm()
    context['form'] = form
    return render(request, 'pages/yacalc.html', context)


def login_page(request):
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = loginform.data['username']
            password = loginform.data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "Авторизация успешна")
            else:
                messages.add_message(request, messages.ERROR, "Неправильный логин или пароль")
        else:
            messages.add_message(request, messages.ERROR, "Некорректные данные в форме авторизации")
    return redirect('index')


def logout_page(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Вы успешно вышли из аккаунта")
    return redirect('index')
