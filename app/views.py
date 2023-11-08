from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage


title_1 = 'Lorem ipsum dolor sit amet'
title_2 = 'Nullam ac dapibus lectus'
title_3 = 'Vestibulum a ultrices tellus'
content_1 = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce odio nisl, dapibus non diam quis, semper hendrerit justo. Integer convallis mauris lectus, sit amet imperdiet velit mollis a. Aliquam erat volutpat. Sed non massa egestas, molestie sem condimentum, volutpat purus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum eu magna purus. Vivamus et augue turpis. Donec mattis ipsum sed congue viverra. Ut enim eros, tempus in commodo ac, tincidunt vitae orci. Fusce faucibus facilisis est, id venenatis libero porta aliquam. Sed et eros orci. In semper odio lacus, vitae tristique libero lobortis non. Suspendisse potenti.'
content_2 = 'Nullam ac dapibus lectus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; In tincidunt neque egestas magna fermentum volutpat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris fermentum odio et accumsan rhoncus. Cras et iaculis orci. Integer nec massa placerat, volutpat purus non, pulvinar elit. Sed gravida massa malesuada ultrices tristique.'
content_3 = 'Vestibulum a ultrices tellus, vitae condimentum ipsum. Vivamus commodo nibh eget tincidunt faucibus. Proin porta commodo nisl, rutrum vulputate libero consequat et. Aliquam vitae gravida justo, sed posuere eros. Donec ac aliquam elit. Etiam maximus et lorem eget mollis. Sed non urna libero. Sed tincidunt viverra lorem et dictum. Sed et sapien urna. Aliquam consectetur lectus ut augue tincidunt scelerisque. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Vivamus lorem quam, elementum et neque in, tincidunt porttitor nibh. Nam scelerisque tempus orci, nec semper ipsum consequat sagittis.'
titles = [title_1 + ' 0', title_2 + ' 1', title_3 + ' 2', title_1 + ' 3', title_2 + ' 4', title_3 + ' 5', title_1 + ' 6', title_2 + ' 7', title_3 + ' 8', title_1 + ' 9', title_2 + ' 10', title_3 + ' 11']
contents = [content_1, content_2, content_3, content_1, content_2, content_3, content_1, content_2, content_3, content_1, content_2, content_3]
tag_1 = 'Perl'
tag_2 = 'Python'
tag_3 = 'TechnoPark'
tag_4 = 'MySQL'
tag_5 = 'django'
tag_6 = 'Mail.ru'
tag_7 = 'Voloshin'
tag_8 = 'Firefox'
tag_9 = 'C++'
tag_10 = 'Swift'
tags = [tag_1, tag_2, tag_3, tag_4, tag_5, tag_6, tag_7, tag_8, tag_9, tag_10]
question_tags = [
    [tag_1, tag_2, tag_3],
    [tag_4, tag_5],
    [tag_1, tag_3, tag_4, tag_7, tag_9],
    [tag_7, tag_8, tag_9],
    [tag_2, tag_3, tag_4],
    [tag_1, tag_10, tag_6],
    [tag_3, tag_4, tag_5],
    [tag_1, tag_5, tag_6],
    [tag_6, tag_7, tag_9],
    [tag_6, tag_7, tag_8],
    [tag_1, tag_9],
    [tag_2, tag_3, tag_6, tag_7, tag_8]]

QUESTIONS = [
    {
        'id': i,
        'title': titles[i],
        'content': contents[i],
        'tags':  question_tags[i]
    } for i in range(10)
]
ANSWERS = []

import random
for question in QUESTIONS:
    for i in range(1, random.randrange(2, 11)):
        answer = {
            'question_id': question['id'],
            'id': i,
            'title': 'Answer at ' + titles[i],
            'content': 'This is answer to that question. The question_id is ' + str(question['id']) + '. ' + contents[i],
        }
        ANSWERS.append(answer)


user = {
    'is_active': True,
    'id': 1,
    'name': 'dr_pepper',
    'login': '@dr_pepper',
    'password': 'psw',
    'email': 'dr_pepper@mail.ru',
    'answers_count': 0
}


def paginate(objects, page, per_page=4):
    paginator = Paginator(objects, per_page=per_page)
    return paginator.page(page).object_list, paginator.num_pages


def index(request, page_num=1):
    page = request.GET.get('page', page_num)
    try:
        pagination = paginate(QUESTIONS, page)
    except EmptyPage:
        return error(request)
    questions = pagination[0]
    for question_ in questions:
        answers_ = [ans for ans in ANSWERS if question_['id'] is ans['question_id']]
        question_['answers_count'] = len(answers_)
    pages = list(range(1, pagination[1] + 1))
    return render(request, template_name='index.html', context={
        'user': user,
        'pages': pages,
        'page': page_num,
        'popular_tags': tags,
        'questions': questions})


def question(request, question_id, page_num=1):
    page = request.GET.get('page', page_num)
    question_ = QUESTIONS[question_id]
    answers_ = [answer for answer in ANSWERS if question_id is answer['question_id']]
    answer_per_page = 2
    try:
        pagination = paginate(answers_, page, answer_per_page)
    except EmptyPage:
        return error(request)
    answers = pagination[0]
    pages = list(range(1, pagination[1] + 1))
    return render(request, template_name='question.html', context={
        'user': user,
        'pages': pages,
        'page': page,
        'popular_tags': tags,
        'question': question_,
        'answers': answers})


def ask(request):
    return render(request, template_name='ask.html', context={'user': user, 'popular_tags': tags})


def login(request):
    return render(request, template_name='login.html', context={'user': user, 'popular_tags': tags})


def registration(request):
    return render(request, template_name='registration.html', context={'user': user, 'popular_tags': tags})


def tag(request, target_tag, page_num=1):
    page = request.GET.get('page', page_num)
    filtered_questions = [question for question in QUESTIONS if target_tag in question['tags']]
    question_per_page = 2
    try:
        pagination = paginate(filtered_questions, page, question_per_page)
    except EmptyPage:
        return error(request)
    questions = pagination[0]
    pages = list(range(1, pagination[1] + 1))
    return render(request, template_name='tag.html', context={
        'user': user,
        'pages': pages,
        'page': page_num,
        'popular_tags': tags,
        'questions': questions,
        'target_tag': target_tag})


def settings(request):
    return render(request, template_name='settings.html', context={'user': user, 'popular_tags': tags})


def error(request):
    return render(request, template_name='error.html', context={'user': user})
