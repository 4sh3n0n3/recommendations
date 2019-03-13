from django.db.utils import IntegrityError
from django.shortcuts import render, redirect

from main.models import User, Choice, Course
from .utils import get_recommendations_list, get_courses_for_selecting, calculate_djakarta


def add_user(request):
    if request.method == 'POST':
        try:
            user = User.objects.create(name=request.POST['name'])
        except IntegrityError:
            return render(request, 'add_user.html', {'error_mess': 'Пользователь уже существует!'})
        return redirect('main:select_courses', user.name)
    return render(request, 'add_user.html')


def add_course(request):
    if request.method == 'POST':
        try:
            Course.objects.create(name=request.POST['name'])
        except IntegrityError:
            return render(request, 'add_course.html', {'error_mess': 'Курс уже существует!'})
        return render(request, 'add_course.html', {'mess': 'Курс успешно сохранен'})
    return render(request, 'add_course.html')


def select_user(request):
    context = {'users': User.objects.all()}

    if request.method == 'GET':
        return render(request, 'select_user.html', context)

    if request.method == 'POST':
        try:
            user = User.objects.get(name=request.POST['name'])
        except User.DoesNotExist:
            context['error_mess'] = 'Пользователь не существует!'
            return render(request, 'select_user.html', context)
        return redirect('main:select_courses', user.name)


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


def show_recommendations(request, username=None):
    if username is None:
        context = {'users': User.objects.all()}
    else:
        recommendations = get_recommendations_list(username)

        context = {
            'username': username,
            'recommendations': recommendations,
        }

        if recommendations is None:
            context.update({'error_mess': 'Такого пользователя не существует!'})

    return render(request, 'recommendations_list.html', context)


def matrix(request, username1=None):
    context = {'username1': username1}

    if username1 is not None:
        res = []
        user1_courses = Choice.objects.filter(user__name=username1).values_list('course__name', flat=True)
        for user in User.objects.exclude(name=username1):
            res.append({
                'username1': username1,
                'username2': user.name,
                'user1_courses': user1_courses,
                'user2_courses': Choice.objects.filter(user__name=user.name).values_list('course__name', flat=True),
                'coef': round(calculate_djakarta(username1, user.name), 4)
            })
        context['result'] = res
    else:
        context['users'] = User.objects.all()

    return render(request, 'matrix.html', context)
