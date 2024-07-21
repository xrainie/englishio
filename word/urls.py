from django.urls import path
from . import views

app_name = 'word'

urlpatterns = [
    path('', views.word_detail, name='word_detail'),
    path('list/', views.word_list, name='word_list'),
]
