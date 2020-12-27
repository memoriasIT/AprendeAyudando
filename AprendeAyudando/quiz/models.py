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

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        #abstract = True
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

"""class QuizActivity(Quiz):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

class QuizCourse(Quiz):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)"""

#---------------------------Question------------------
class Question(models.Model):
    text = models.CharField(max_length=500)
    question_score = models.IntegerField()
    #image = models.ImageField()

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    def __str__(self):
        return self.text
    """class Meta:
        abstract = True"""
"""class QuestionActivity(Question):
    quiz = models.ForeignKey(QuizActivity, on_delete=models.CASCADE)
class QuestionCourse(Question):
    quiz = models.ForeignKey(QuizCourse, on_delete=models.CASCADE)"""

#----------------------------Answer------------------
class Answer(models.Model):
    text = models.CharField(max_length=500)
    correct = models.BooleanField()

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    """class Meta:
        abstract = True"""

"""class AnswerActivity(Answer):
    question = models.ForeignKey(QuestionActivity, on_delete=models.CASCADE)

class AnswerCourse(Answer):
    question = models.ForeignKey(QuestionCourse, on_delete=models.CASCADE)"""



#-------------------------Qualification--------------
class Qualification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    total_score = models.IntegerField()
    finish = models.BooleanField(default=False)

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
    """class Meta:
        abstract = True"""

"""class QualificationActivity(Qualification):
    quiz = models.ForeignKey(QuizActivity, on_delete=models.CASCADE)
    questions_asked = models.ManyToManyField(
        QuestionActivity,
        through='QuestionAskedActivity',
        through_fields=('qualification_activity', 'question_activity'),
        related_name='questions_asked_qualification'
    )

class QualificationCourse(Qualification):
    quiz = models.ForeignKey(QuizCourse, on_delete=models.CASCADE)
    questions_asked = models.ManyToManyField(
        QuestionCourse,
        through='QuestionAskedCourse',
        through_fields=('qualification_course', 'question_course'),
        related_name='questions_asked_qualification'
    )"""

#------------------Questions Asked-----------------
class QuestionAsked(models.Model):
    qualification = models.ForeignKey(
        Qualification, 
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

"""class QuestionAskedActivity(models.Model):
    qualification_activity = models.ForeignKey(
        QualificationActivity, 
        on_delete=models.CASCADE
    )
    question_activity = models.ForeignKey(
        QuestionActivity,
        on_delete=models.CASCADE
    )

class QuestionAskedCourse(models.Model):
    qualification_course = models.ForeignKey(
        QualificationCourse,
        on_delete=models.CASCADE
    )
    question_course = models.ForeignKey(
        QuestionCourse,
        on_delete=models.CASCADE
    )
    class Meta:
        unique_together = ('qualification_course','question_course')"""

"""class Prue(models.Model):
    texto = models.CharField(max_length=30)
    quiz_activity = models.ForeignKey(
        QuizActivity,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    quiz_course = models.ForeignKey(
        QuizCourse,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    class Meta:
        constraints = [
            models.CheckConstraint(
                check = (
                    models.Q(quiz_activity__isnull = True, quiz_course__isnull = False)
                    |
                    models.Q(quiz_activity__isnull = False, quiz_course__isnull = True)
                ),
                name='prue_2quiz_are_null_or_notnull'
            ),
        ]"""