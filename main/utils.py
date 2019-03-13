from math import sqrt

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from .models import *

COEFF_MIN_VALUE = 0.5


def get_recommendations_list(username):
    try:
        aimed_user = User.objects.get(name=username)
    except ObjectDoesNotExist:
        return None
    all_users = User.objects.all().exclude(name=username)
    aimed_courses = aimed_user.courses.get_queryset()
    courses_dict = {}

    for user in all_users:
        courses = user.courses.get_queryset()
        intersection = list(courses.intersection(aimed_courses))
        union = list(courses.union(aimed_courses))
        diff = list(set(courses) - set(aimed_courses))

        coeff = len(intersection) / len(union)
        if coeff >= COEFF_MIN_VALUE:
            for course in diff:
                val = courses_dict.get(course)
                if val is None:
                    val = 0
                courses_dict.update({course: val + 1})

    sorted_by_value = sorted(courses_dict.items(), key=lambda kv: kv[1])
    top_5 = []
    counter = 0
    for item in reversed(sorted_by_value):
        counter += 1
        top_5.append(item)
        if counter == 5:
            break

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
    courses1 = Choice.objects.filter(user__name=username1).values_list('course__id', flat=True)
    courses2 = Choice.objects.filter(user__name=username2).values_list('course__id', flat=True)

    # C = A intersection with B
    c = set(courses1).intersection(courses2)

    # |C|/(sqrt (|A|*|B|))
    return len(c) / sqrt(len(courses1) * len(courses2))
