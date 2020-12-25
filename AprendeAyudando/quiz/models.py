from django.db import models
from activity.models import Activity
from courses.models import Course
from django.contrib.auth import get_user_model

#---------------------------Quiz--------------------
class Quiz(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True, null=True)
    repeatable = models.BooleanField()
    show_qualification = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    class Meta:
        abstract = True

class QuizActivity(Quiz):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

class QuizCourse(Quiz):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

#---------------------------Question------------------
class Question(models.Model):
    text = models.CharField(max_length=500)
    question_score = models.IntegerField()
    #image = models.ImageField()
    class Meta:
        abstract = True
class QuestionActivity(Question):
    quiz = models.ForeignKey(QuizActivity, on_delete=models.CASCADE)
class QuestionCourse(Question):
    quiz = models.ForeignKey(QuizCourse, on_delete=models.CASCADE)

#----------------------------Answer------------------
class Answer(models.Model):
    text = models.CharField(max_length=500)
    correct = models.BooleanField()
    class Meta:
        abstract = True

class AnswerActivity(Answer):
    question = models.ForeignKey(QuestionActivity, on_delete=models.CASCADE)

class AnswerCourse(Course):
    question = models.ForeignKey(QuestionCourse, on_delete=models.CASCADE)



#-------------------------Qualification--------------
class Qualification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    total_score = models.FloatField()
    correct_answers = models.IntegerField()

    class Meta:
        abstract = True

class QualificationActivity(Qualification):
    quiz = models.ForeignKey(QuestionActivity, on_delete=models.CASCADE)

class QualificationCourse(Qualification):
    quiz = models.ForeignKey(QuestionCourse, on_delete=models.CASCADE)
