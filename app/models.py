from django.contrib.auth.models import User
from django.db import models
import uuid
from datetime import datetime
from django.utils import timezone
from django.db.models import Count
from django.db.models import Sum


class QuestionManager(models.Manager):
    def get_questions(self, count=100):
        return self.order_by('-dt')[:count]

    def get_questions_hot(self, count=100):
        question_info = []
        questions = self.order_by('-dt')[:count]
        for question in questions:
            likes = QuestionLike.manager.get_likes_at_question_count(question)
            question_info.append(
                {
                    "question": question,
                    "likes": likes
                }
            )
        sorted_question_info = sorted(question_info, key=lambda x: x["likes"], reverse=True)
        sorted_questions = []
        for info in sorted_question_info:
            sorted_questions.append(info["question"])
        return sorted_questions


    def get_tags_at_question(self, question):
        tags = Tag.manager.get_tags_at_question(question)
        return tags

    def get_questions_by_tag(self, tag):
        return Question.objects.filter(tag__tag=tag).order_by('-dt')[:50]


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    content = models.TextField(default='')
    dt = models.DateTimeField(default=timezone.now)
    objects = models.Manager()
    manager = QuestionManager()

    def __str__(self):
        return f"{self.user.username} : {self.title}"


class AnswerManager(models.Manager):

    def get_answers_at_question(self, question):
        return self.filter(question=question).order_by('-is_correct')

    def get_answers_at_question_count(self, question):
        return len(self.filter(question=question))


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(default='')
    dt = models.DateTimeField(default=timezone.now)
    is_correct = models.BooleanField(default=False)
    objects = models.Manager()
    manager = AnswerManager()

    def __str__(self):
        return f"{self.user.username} -> {self.question.user.username} : {self.question.title}"


class AnswerLikeManager(models.Manager):

    def get_likes_at_answer_count(self, answer):
        return self.filter(answer=answer).aggregate(likes_sum=Sum('like'))['likes_sum'] or 0


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    objects = models.Manager()
    manager = AnswerLikeManager()

    def __str__(self):
        return f"{self.user.user.username} : like"


class QuestionLikeManager(models.Manager):

    def get_likes_at_question_count(self, question):
        return self.filter(question=question).aggregate(likes_sum=Sum('like'))['likes_sum'] or 0


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    objects = models.Manager()
    manager = QuestionLikeManager()

    def __str__(self):
        return f"{self.user.user.username} : like"


class TagManager(models.Manager):

    def get_tags_at_question(self, question):
        return self.filter(question=question)

    def get_top_tags(self):
        top_tags = self.values('tag').annotate(tag_count=Count('tag')).order_by('-tag_count')[:9]
        return top_tags


class Tag(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    tag = models.CharField(max_length=128)
    objects = models.Manager()
    manager = TagManager()

    def __str__(self):
        return f"{self.tag}"


class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.BinaryField(null=True, blank=True)




