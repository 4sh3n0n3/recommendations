from .models import *


COEFF_MIN_VALUE = 0.5


def get_recommendations_list(aimed_user):
    all_users = User.objects.all().exclude(name=aimed_user.name)
    courses_dict = {}

    for user in all_users:
        intersection = list(user.courses.get_queryset().intersection(aimed_user.courses.get_queryset()))
        union = list(user.courses.get_queryset().union(aimed_user.courses.get_queryset()))
        diff = list(set(user.courses.get_queryset()) - set(aimed_user.courses.get_queryset()))

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
    return top_5
