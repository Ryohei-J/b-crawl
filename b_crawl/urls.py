from django.urls import path
from . import views

add_name = 'b_crawl'

urlpatterns = [
    path('',views.home, name='home'),
    path('result/', views.result, name='result'),
    path('history-all/', views.history_all, name='history_all'),
    path('history-yours/', views.history_yours, name='history_yours'),
]