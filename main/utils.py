from math import sqrt

from django.db.models import Count

from main.models import User, Course, Choice

COEFF_MIN_VALUE = 0.5


def djakarta_coef(courses1, courses2):
    # C = A intersection with B
    c = set(courses1).intersection(courses2)

    # |C|/(sqrt (|A|*|B|))
    return len(c) / sqrt(len(courses1) * len(courses2))


def get_recommendations_list(username):
    try:
        aimed_user = User.objects.get(name=username)
    except User.DoesNotExist:
        return None

    all_users = User.objects.exclude(name=username)
    aimed_courses = aimed_user.courses.all()
    courses_dict = {}

    for user in all_users:
        courses = user.courses.all()
        diff = list(set(courses) - set(aimed_courses))

        coeff = djakarta_coef(courses, aimed_courses)
        if coeff >= COEFF_MIN_VALUE:
            for course in diff:
                courses_dict.update({course: courses_dict.get(course, 0) + 1})

    sorted_by_value = sorted(courses_dict.items(), key=lambda kv: kv[1])
    top_5 = reversed(sorted_by_value)[:5]

    top_dict = {}
    for item in top_5:
        top_dict.update({item[0].name: item[1]})
    print(top_dict)
    return top_dict


def get_courses_for_selecting(selected_cources_ids):
    selected_cources = Course.objects.filter(id__in=selected_cources_ids)

    not_selected = Course.objects.exclude(id__in=selected_cources_ids).annotate(selected_count=Count('choices'))
    min_popuplar = not_selected.order_by('selected_count')[:4]
    max_popular = not_selected.exclude(id__in=min_popuplar.values_list('id', flat=True)).order_by('-selected_count')[:4]

    return list(selected_cources) + list(min_popuplar) + list(max_popular)


def calculate_djakarta(username1, username2):
    courses1 = Choice.objects.filter(user__name=username1)
    courses2 = Choice.objects.filter(user__name=username2)
    return djakarta_coef(courses1, courses2)
