from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

# Create your views here.


def add_user(request):
    template = loader.get_template('add_user.html')

    if request.method == 'GET':
        return HttpResponse(template.render({}, request))

    if request.method == 'POST':
        user = User()
        user.name = request.POST['name']
        try:
            user.save()
        except IntegrityError:
            return HttpResponse(template.render({'error_mess': 'Пользователь уже существует!'}, request))
        template = loader.get_template('select_course.html')
        courses = Course.objects.all()
        context = {
            'username': user.name,
            'courses': courses,
        }
        return HttpResponse(template.render(context, request))


def add_course(request):
    template = loader.get_template('add_course.html')

    if request.method == 'GET':
        return HttpResponse(template.render({}, request))

    if request.method == 'POST':
        course = Course()
        course.name = request.POST['name']
        try:
            course.save()
        except IntegrityError:
            return HttpResponse(template.render({'error_mess': 'Курс уже существует!'}, request))
        return HttpResponse(template.render({'mess': 'Курс успешно сохранен'}, request))


def select_user(request):
    template = loader.get_template('select_user.html')

    if request.method == 'GET':
        return HttpResponse(template.render({}, request))

    if request.method == 'POST':
        try:
            user = User.objects.get(name=request.POST['name'])
        except ObjectDoesNotExist:
            return HttpResponse(template.render({'error_mess': 'Пользователь не существует!'}, request))
        template = loader.get_template('select_course.html')
        courses = Course.objects.all()
        context = {
            'username': user.name,
            'courses': courses,
        }
        return HttpResponse(template.render(context, request))


def select_courses(request, username):
    template = loader.get_template('select_course.html')

    if request.method == 'GET':
        courses = Course.objects.all()
        context = {
            'username': username,
            'courses': courses,
        }
        return HttpResponse(template.render(context, request))

    if request.method == 'POST':
        user = User.objects.get(name=username)
        courses = Course.objects.all()

        for course in courses:
            if request.POST.get(course.name):
                try:
                    Choice.objects.get(user=user, course=course)
                except ObjectDoesNotExist:
                    choice = Choice()
                    choice.user = user
                    choice.course = course
                    choice.save()
                    print('Saved: {}'.format(course.name))
            else:
                try:
                    choice = Choice.objects.get(user=user, course=course)
                except ObjectDoesNotExist:
                    continue
                choice.delete()
                print('Deleted: {}'.format(course.name))

        context = {
            'username': username,
            'courses': courses,
            'mess': 'Данные успешно изменены',
        }
        return HttpResponse(template.render(context, request))


def view_table(request):
    template = loader.get_template('result_table.html')
    users = User.objects.all()
    courses = Course.objects.all()
    context = {
        'users': users,
        'courses': courses,
    }
    return HttpResponse(template.render(context, request))