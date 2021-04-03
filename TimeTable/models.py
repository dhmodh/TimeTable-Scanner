import datetime as dt
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserCreationModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Short Name', max_length=10, default='None')

    def __str__(self):
        return self.name

class ScanTimeTableModel(models.Model):

    SEMESTER_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
    )

    DIVISION_CHOICES = (
        ('H', 'H'),
        ('I', 'I'),
    )

    division = models.CharField(verbose_name="Timetable Division", max_length=1, choices=DIVISION_CHOICES, default='1')
    semester = models.CharField(verbose_name="Timetable Semester", max_length=1, choices=SEMESTER_CHOICES, default='1')
    year = models.IntegerField(verbose_name="Timetable Year", default=(dt.date.today().year))
    image = models.ImageField(verbose_name="Timetable Image", default="image/White_thumb.png", upload_to='TimeTable/image/')

    def __str__(self):
        return self.division+'-'+self.semester+'-'+str(self.year)

class SubjectFaculty(models.Model):

    BATCH_CHOICES = (
        ('All', 'All'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    faculty = models.CharField(verbose_name="Faculty Name", max_length=5, default='None')
    batch = models.CharField(verbose_name="Batch Number", max_length=5, choices=BATCH_CHOICES, default='All')
    subject = models.CharField(verbose_name="Subject Name", max_length=10, default='None')
    timetable = models.ForeignKey(ScanTimeTableModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.faculty+' '+self.subject+' '+self.batch

class DeveloperModel(models.Model):
    name = models.CharField(verbose_name="Developer Name", max_length=100, default="Developer")
    designation = models.CharField(verbose_name="Developer Designation", max_length=50, default="Developer")
    description = models.TextField(verbose_name="Developer Description", default="Description not given")
    image = models.ImageField(verbose_name="Developer Name", default="image/White_thumb.png")

    def __str__(self):
        return self.name
