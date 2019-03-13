from django.urls import path
from .views import add_user, add_course, select_user, select_courses, view_table, show_recommendations, matrix

app_name = 'main'
urlpatterns = [
    path('create_user/', add_user, name='new_user'),
    path('create_course/', add_course, name='new_course'),
    path('select_user/', select_user, name='select_user'),
    path('select_courses/<str:username>/', select_courses, name='select_courses'),
    path('table/', view_table, name='view_table'),
    path('recomm/<str:username>/', show_recommendations, name='show_recommendations'),
    path('matrix/', matrix, name='matrix'),
    path('matrix/<str:username1>/', matrix, name='matrix1'),
    path('matrix/<str:username1>/<str:username2>/', matrix, name='matrix2'),
]
