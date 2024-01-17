from app.models import Question, Answer, Tag, QuestionLike, AnswerLike
from django.contrib.auth.models import User
from sqlite3 import IntegrityError
from django.db import transaction
from faker import Faker
import random
import warnings


warnings.filterwarnings('ignore', message="DateTimeField Answer.dt received a naive datetime", category=RuntimeWarning)
# warnings.filterwarnings('default')

fake = Faker()

print("db_fill")

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
            print(f'user created {u.username}')
        except IntegrityError:
            print(f'User with username {u.username} already exists')
        except Exception as e:
            print(f'An error occurred while creating user: {e}')


'''def fill_profile_entity(n):
    for i in range(0, n):
        try:
            u = User.objects.create_user(
                username=fake.user_name() + str(i),
                email=fake.email(),
                password='psw',
                first_name=fake.first_name(),
                last_name=fake.last_name())
            u.save()
            p = User.objects.create_user(u)
            p.save()
            print(f'user created {i}')
        except IntegrityError:
            fill_profile_entity(n - i + 1)'''


def fill_question_entity(n):
    profiles = User.objects.all()
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
    users = User.objects.all()
    questions = Question.objects.all()
    for i in range(n):
        u = random.choice(users)
        q = random.choice(questions)
        like = random.choice([-1, 0, 1])
        QuestionLike.objects.create(user=u, question=q, like=like)
        print(f'like at question created {i}')


def fill_answer_like_entity(n):
    users = User.objects.all()
    answer_ = Answer.objects.all()
    for i in range(n):
        u = random.choice(users)
        aa = random.choice(answer_)
        like = random.choice([-1, 0, 1])
        AnswerLike.objects.create(user=u, answer=aa, like=like)
        print(f'like at answer created {i}')


def fill_answer_entity(n):
    users = User.objects.all()
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
    users = User.objects.all()
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

fill_profile_entity(120)
fill_question_entity(1100)
fill_answer_entity(10000)
fill_answer_entity_bulk(10)
create_fake_tags()
fill_tag_entity(1000)
fill_question_like_entity(10000)
fill_answer_like_entity(10000)