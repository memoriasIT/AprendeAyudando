from django.db import models
from activity.models import Activity
from courses.models import Course
from django.contrib.auth import get_user_model

#----------------------------Quiz--------------------
class Quiz(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True, null=True)
    maximum_date = models.DateTimeField(verbose_name="Maximum Date", null=True)
    repeatable = models.BooleanField()
    show_qualification = models.BooleanField(default=False)

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        constraints = [
            models.CheckConstraint(
                check = (
                    models.Q(activity__isnull = True, course__isnull = False)
                    |
                    models.Q(activity__isnull = False, course__isnull = True)
                ),
                name='Quiz_activityAndCourse_are_null_or_notnull'
            ),
        ]

#---------------------------Question------------------
class Question(models.Model):
    text = models.CharField(max_length=500)
    question_score = models.IntegerField()
    #image = models.ImageField()

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    def __str__(self):
        return self.text

#----------------------------Answer------------------
class Answer(models.Model):
    text = models.CharField(max_length=500)
    correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

#-------------------------Qualification--------------
class Qualification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)
    finish = models.BooleanField(default=False)
    total_correct_questions = models.IntegerField(default=0)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    questions_asked = models.ManyToManyField(
        Question,
        through='QuestionAsked',
        through_fields=('qualification', 'question'),
        related_name='questions_asked_qualification'
    )
    def __str__(self):
        return self.user.username
        #return str(self.id)

#------------------------Questions Asked-----------------
class QuestionAsked(models.Model):
    qualification = models.ForeignKey(
        Qualification, 
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )