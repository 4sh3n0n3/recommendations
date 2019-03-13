from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=30, unique=True)
    courses = models.ManyToManyField(through='Choice', to='Course', related_name='users')

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Choice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='choices')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='choices')
