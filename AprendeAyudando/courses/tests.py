import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Course


# Tests para los cursos
# run with python manage.py test courses
# class CourseModelTests(TestCase):

# // TODO create tests for the different models
    # def course_was_published_recently_with_future_question(self):
    #     """
    #     was_published_recently() returns False for questions whose pub_date
    #     is in the future.
    #     """
    #     time = timezone.now() + datetime.timedelta(days=30)
    #     future_course = Course(pub_date=time)
    #     self.assertIs(future_course.was_published_recently(), False)