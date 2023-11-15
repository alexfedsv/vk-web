import django.contrib.admin
from django.contrib import admin

# Register your models here.
from app.models import Profile, Question, Tag, Answer, AnswerLike, QuestionLike, Avatar


admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(AnswerLike)
admin.site.register(QuestionLike)
admin.site.register(Avatar)

