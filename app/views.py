from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from django.contrib.auth.models import User
from sqlite3 import IntegrityError
from django.db import transaction
from faker import Faker
import random

import warnings
warnings.filterwarnings('ignore', message="DateTimeField Answer.dt received a naive datetime", category=RuntimeWarning)
# warnings.filterwarnings('default')

fake = Faker()


'''def fill_profile_entity():
    profiles = []
    for i in range(0, 100):
        user_name = fake.user_name()
        profile = {
            'login': user_name + str(i),
            'password': 'psw_' + str(i),
            'nickname': user_name + str(i),
            'email': user_name + str(i) + '@example.com'
        }
        profiles.append(profile)

    for profile_data in profiles:
        p = Profile(
            userId=uuid.uuid4(),
            login=profile_data["login"],
            password=profile_data["password"],
            nickname=profile_data["nickname"],
            email=profile_data["email"]
        )
        p.save()'''


def fill_profile_entity(n):
    for i in range(0, n):
        try:
            u = User.objects.create_user(
                username=fake.user_name() + str(i),
                email=fake.email(),
                password='psw',
                first_name=fake.first_name(),
                last_name=fake.last_name())
            u.save()
            p = Profile.objects.create(user=u)
            p.save()
            print(f'user created {i}')
        except IntegrityError:
            fill_profile_entity(n - i + 1)


def fill_question_entity(n):
    profiles = Profile.objects.all()
    for i in range(n):
        user_profile = random.choice(profiles)
        q = Question(user=user_profile,
                     title=fake.sentence(),
                     content=fake.paragraph(),
                     dt=fake.date_time_this_year())
        q.save()
        print(f'question created {i}')


def create_fake_tags(n=11000):
    with open('tags.txt', 'w') as file:
        for i in range(n):
            tag_name = fake.word()
            file.write(tag_name + '\n')
            print(f'{i} tag created')


def fill_tag_entity(n):
    with open('tags.txt', 'r') as file:
        tags_ = file.readlines()
    for i in range(n):
        random_question = Question.objects.order_by('?').first()
        random_tag = random.choice(tags_).strip()
        t = Tag(question=random_question,
                tag=random_tag)
        t.save()
        if i % 1000 == 0:
            print(f'tag created {i}')


def fill_question_like_entity(n):
    users = Profile.objects.all()
    questions = Question.objects.all()
    for i in range(n):
        u = random.choice(users)
        q = random.choice(questions)
        like = random.choice([-1, 0, 1])
        QuestionLike.objects.create(user=u, question=q, like=like)
        print(f'like at question created {i}')


def fill_answer_like_entity(n):
    users = Profile.objects.all()
    answer_ = Answer.objects.all()
    for i in range(n):
        u = random.choice(users)
        aa = random.choice(answer_)
        like = random.choice([-1, 0, 1])
        AnswerLike.objects.create(user=u, answer=aa, like=like)
        print(f'like at answer created {i}')


def fill_answer_entity(n):
    users = Profile.objects.all()
    for i in range(n):
        random_question = Question.objects.order_by('?').first()
        random_user = random.choice(
            users.exclude(id=random_question.user.id))
        a = Answer(question=random_question,
                   user=random_user,
                   content=fake.paragraph(),
                   dt=fake.date_time_this_year(),
                   is_correct=random.choice([True, False]))
        a.save()
        if i % 1000 == 0:
            print(f'answer created {i}')


def fill_answer_entity_bulk(n):
    users = Profile.objects.all()
    answers = []
    with transaction.atomic():
        for i in range(n):
            random_question = Question.objects.order_by('?').first()
            random_user = random.choice(users.exclude(id=random_question.user.id))
            answer_ = Answer(question=random_question,
                             user=random_user,
                             content=fake.paragraph(),
                             dt=fake.date_time_this_year(),
                             is_correct=random.choice([True, False]))
            answers.append(answer_)
            print(f'answer created {i}')
        Answer.objects.bulk_create(answers)
        print(f'Готово {n} добавлено')


'''fill_profile_entity(12000)'''
'''fill_question_entity(110000)'''
'''fill_answer_entity(1100000-962891)'''
'''fill_answer_entity_bulk(5000)'''
'''create_fake_tags()'''
'''fill_tag_entity(100000)'''
'''fill_question_like_entity(1000000)'''
'''fill_answer_like_entity(1000000)'''


user = {
    'is_active': True,
    'id': 1,
    'name': 'dr_pepper',
    'login': '@dr_pepper',
    'password': 'psw',
    'email': 'dr_pepper@mail.ru',
    'answers_count': 0
}


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
    return render(request, template_name='index.html', context={
        'user': user,
        'pages': pages,
        'page': page_num,
        'popular_tags': popular_tags,
        'questions_with_info': questions_with_info})


def hot(request, page_num=1):
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
    return render(request, template_name='question.html', context={
        'user': user,
        'pages': pages,
        'page': page_num,
        'popular_tags': popular_tags,
        'question_info': question_info,
        'answers_with_info': answers_with_info})


def ask(request):
    popular_tags = Tag.manager.get_top_tags()
    return render(request, template_name='ask.html', context={'user': user, 'popular_tags': popular_tags})


def login(request):
    popular_tags = Tag.manager.get_top_tags()
    return render(request, template_name='login.html', context={'user': user, 'popular_tags': popular_tags})


def registration(request):
    popular_tags = Tag.manager.get_top_tags()
    return render(request, template_name='registration.html', context={'user': user, 'popular_tags': popular_tags})


def tag(request, target_tag, page_num=1):
    questions_db = Question.manager.get_questions_by_tag(target_tag)
    questions_per_page = 2
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
    return render(request, template_name='tag.html', context={
        'target_tag': target_tag,
        'user': user,
        'pages': pages,
        'page': page_num,
        'popular_tags': popular_tags,
        'questions_with_info': questions_with_info})


def settings(request):
    popular_tags = Tag.manager.get_top_tags()
    return render(request, template_name='settings.html', context={'user': user, 'popular_tags': popular_tags})


def error(request):
    return render(request, template_name='error.html', context={'user': user})
