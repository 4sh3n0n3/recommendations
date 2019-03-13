from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from main.models import User, Choice, Course
from .utils import get_recommendations_list, get_courses_for_selecting


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
    context = {'users': User.objects.all()}

    if request.method == 'GET':
        return render(request, 'select_user.html', context)

    if request.method == 'POST':
        try:
            user = User.objects.get(name=request.POST['name'])
        except ObjectDoesNotExist:
            context['error_mess'] = 'Пользователь не существует!'
            return render(request, 'select_user.html', context)
        template = loader.get_template('select_course.html')
        courses = Course.objects.all()
        context = {
            'username': user.name,
            'courses': courses,
        }
        return HttpResponse(template.render(context, request))


def select_courses(request, username):
    user = User.objects.get(name=username)

    selected_cources_ids = Choice.objects.filter(user=user).values_list('course_id', flat=True)

    context = {
        'username': username,
        'selected_cources_ids': selected_cources_ids,
        'courses': get_courses_for_selecting(selected_cources_ids),
    }

    if request.method == 'POST':
        selected_cources_ids = request.POST.getlist('selected_courses')
        courses = Course.objects.filter(id__in=selected_cources_ids)

        # если не совпадает, значит в списке есть курсы, которых у нас в базе нет => пришли говноданные
        if len(courses) == len(selected_cources_ids):
            Choice.objects.filter(user=user).delete()
            for course in courses:
                Choice.objects.create(user=user, course=course)
                print('Saved: {}'.format(course.name))

        context['mess'] = 'Данные успешно сохранены'

    return render(request, 'select_course.html', context)


def view_table(request):
    return render(request, 'result_table.html', {
        'users': User.objects.all(),
        'courses': Course.objects.all(),
    })


def show_recommendations(request, username):
    template = loader.get_template('recommendations_list.html')
    recommendations = get_recommendations_list(username)

    context = {
        'username': username,
        'recommendations': recommendations,
    }

    if recommendations is None:
        context.update({'error_mess': 'Такого пользователя не существует!'})

    return HttpResponse(template.render(context, request))
