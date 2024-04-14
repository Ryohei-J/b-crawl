from django.urls import path
from . import views

add_name = 'b_crawl'

urlpatterns = [
    path('',views.home, name='home'),
    path('result/', views.result, name='result'),
    path('history/', views.history, name='history'),
]