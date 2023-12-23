from django.contrib import auth
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect

from app.models import Question, Answer, Tag, QuestionLike, AnswerLike
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.contrib.auth.models import User
from sqlite3 import IntegrityError
from django.db import transaction
from faker import Faker
import random
from app.forms import LoginForm, RegistrationForm, AskForm, AnswerForm


def paginate(objects_list, request, page_num, per_page=5):
    page = request.GET.get('page', page_num)
    paginator = Paginator(objects_list, per_page=per_page)
    try:
        pagination_obj = paginator.page(page).object_list
        pagination_pages_count = paginator.num_pages
    except EmptyPage:
        return error(request)
    except PageNotAnInteger:
        return error(request)
    return pagination_obj, pagination_pages_count


def index(request, page_num=1):
    questions_db = Question.manager.get_questions()
    pagination = paginate(questions_db, request, page_num)
    questions = pagination[0]
    questions_with_info = []
    for q in questions:
        question_info = {
            'question': q,
            'answers_count': Answer.manager.get_answers_at_question_count(q),
            'likes_count': QuestionLike.manager.get_likes_at_question_count(q),
            'tags': Tag.manager.get_tags_at_question(q)
        }
        questions_with_info.append(question_info)
    pages = list(range(1, pagination[1] + 1))
    popular_tags = Tag.manager.get_top_tags()
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    return render(request, template_name='index.html', context={
        'user': user,
        'pages': pages,
        'page': page_num,
        'popular_tags': popular_tags,
        'questions_with_info': questions_with_info})


def hot(request, page_num=1):
    questions_db = Question.manager.get_questions_hot()
    pagination = paginate(questions_db, request, page_num)
    questions = pagination[0]
    questions_with_info = []
    for q in questions:
        question_info = {
            'question': q,
            'answers_count': Answer.manager.get_answers_at_question_count(q),
            'likes_count': QuestionLike.manager.get_likes_at_question_count(q),
            'tags': Tag.manager.get_tags_at_question(q)
        }
        questions_with_info.append(question_info)
    pages = list(range(1, pagination[1] + 1))
    popular_tags = Tag.manager.get_top_tags()
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    return render(request, template_name='hot.html', context={
        'user': user,
        'pages': pages,
        'page': page_num,
        'popular_tags': popular_tags,
        'questions_with_info': questions_with_info})


def question(request, question_id, page_num=1):
    try:
        question_ = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return error(request)
    answers_with_info = []
    answers_db = Answer.manager.get_answers_at_question(question_)
    answer_per_page = 2
    pagination = paginate(answers_db, request, page_num, answer_per_page)
    answers = pagination[0]
    pages = list(range(1, pagination[1] + 1))
    question_info = {
        'question': question_,
        'answers_count': Answer.manager.get_answers_at_question_count(question_),
        'likes_count': QuestionLike.manager.get_likes_at_question_count(question_),
        'tags': Tag.manager.get_tags_at_question(question_)
    }
    for aa in answers:
        answer_info = {
            'answer': aa,
            'likes_count': AnswerLike.manager.get_likes_at_answer_count(aa)
        }
        answers_with_info.append(answer_info)
    popular_tags = Tag.manager.get_top_tags()
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    if request.method == 'GET':
        answer_form = AnswerForm()
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            # здесь будем сохранять
            return redirect(reverse('index'))

    context = {
        'user': user,
        'pages': pages,
        'page': page_num,
        'popular_tags': popular_tags,
        'question_info': question_info,
        'answers_with_info': answers_with_info,
        'answer_form': answer_form}
    print(context)
    return render(request, template_name='question.html', context=context)


def ask(request):
    popular_tags = Tag.manager.get_top_tags()
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'GET':
            ask_form = AskForm()
        if request.method == 'POST':
            print(request.POST)
            ask_form = AskForm(request.POST)
            if ask_form.is_valid():
                ask_form.save_ask(user)
                return redirect(reverse('index'))
    else:
        ask_form = AskForm()
        user = None
    return render(request, template_name='ask.html', context={
        'user': user,
        'popular_tags': popular_tags,
        'form': ask_form})


@csrf_protect
def log_in(request):
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, 'Не правильный пароль или такого пользователя не существует')
    popular_tags = Tag.manager.get_top_tags()
    return render(request, template_name='login.html',
                  context={'user': None,
                           'popular_tags': popular_tags,
                           'form': login_form})


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


@csrf_protect
def registration(request):
    if request.method == 'GET':
        registration_form = RegistrationForm()
    if request.method == 'POST':
        print(request.POST)
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save()
            if user:
                user = authenticate(username=registration_form.cleaned_data['username'],
                                    password=registration_form.cleaned_data['password'])
                login(request, user)
                return redirect(reverse('index'))
    popular_tags = Tag.manager.get_top_tags()
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    return render(request, template_name='registration.html',
                  context={'user': user,
                           'popular_tags': popular_tags,
                           'form': registration_form})


def tag(request, target_tag, page_num=1):
    questions_db = Question.manager.get_questions_by_tag(target_tag)
    questions_per_page = 3
    pagination = paginate(questions_db, request, page_num, questions_per_page)
    questions = pagination[0]
    questions_with_info = []
    for q in questions:
        question_info = {
            'question': q,
            'answers_count': Answer.manager.get_answers_at_question_count(q),
            'likes_count': QuestionLike.manager.get_likes_at_question_count(q),
            'tags': Tag.manager.get_tags_at_question(q)
        }
        questions_with_info.append(question_info)
    pages = list(range(1, pagination[1] + 1))
    popular_tags = Tag.manager.get_top_tags()
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    return render(request, template_name='tag.html', context={
        'target_tag': target_tag,
        'user': user,
        'pages': pages,
        'page': page_num,
        'popular_tags': popular_tags,
        'questions_with_info': questions_with_info})


def settings(request):
    popular_tags = Tag.manager.get_top_tags()
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    return render(request, template_name='settings.html', context={'user': user, 'popular_tags': popular_tags})


def error(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    return render(request, template_name='error.html', context={'user': user})
