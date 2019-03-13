from django.core.exceptions import ObjectDoesNotExist

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
