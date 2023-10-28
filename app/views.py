from django.shortcuts import render
from django.core.paginator import Paginator


title_1 = 'Lorem ipsum dolor sit amet'
title_2 = 'Nullam ac dapibus lectus'
title_3 = 'Vestibulum a ultrices tellus'
content_1 = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce odio nisl, dapibus non diam quis, semper hendrerit justo. Integer convallis mauris lectus, sit amet imperdiet velit mollis a. Aliquam erat volutpat. Sed non massa egestas, molestie sem condimentum, volutpat purus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum eu magna purus. Vivamus et augue turpis. Donec mattis ipsum sed congue viverra. Ut enim eros, tempus in commodo ac, tincidunt vitae orci. Fusce faucibus facilisis est, id venenatis libero porta aliquam. Sed et eros orci. In semper odio lacus, vitae tristique libero lobortis non. Suspendisse potenti.'
content_2 = 'Nullam ac dapibus lectus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; In tincidunt neque egestas magna fermentum volutpat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris fermentum odio et accumsan rhoncus. Cras et iaculis orci. Integer nec massa placerat, volutpat purus non, pulvinar elit. Sed gravida massa malesuada ultrices tristique.'
content_3 = 'Vestibulum a ultrices tellus, vitae condimentum ipsum. Vivamus commodo nibh eget tincidunt faucibus. Proin porta commodo nisl, rutrum vulputate libero consequat et. Aliquam vitae gravida justo, sed posuere eros. Donec ac aliquam elit. Etiam maximus et lorem eget mollis. Sed non urna libero. Sed tincidunt viverra lorem et dictum. Sed et sapien urna. Aliquam consectetur lectus ut augue tincidunt scelerisque. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Vivamus lorem quam, elementum et neque in, tincidunt porttitor nibh. Nam scelerisque tempus orci, nec semper ipsum consequat sagittis.'
titles = [title_1, title_2, title_3, title_1, title_2, title_3, title_1, title_2, title_3, title_1, title_2, title_3]
contents = [content_1, content_2, content_3, content_1, content_2, content_3, content_1, content_2, content_3, content_1, content_2, content_3]

QUESTIONS = [
    {
        'id': i,
        'title': titles[i],
        'content': contents[i]
    } for i in range(10)
]


def paginate(objects, page, per_page=4):
    paginator = Paginator(QUESTIONS, per_page=per_page)
    return paginator.page(page).object_list


def index(request):
    page = request.GET.get('page', 1)
    return render(request, template_name='index.html', context={'questions': paginate(QUESTIONS, page)})


def question(request, question_id):
    question_ = QUESTIONS[question_id]
    return render(request, template_name='question.html', context={'question': question_})
