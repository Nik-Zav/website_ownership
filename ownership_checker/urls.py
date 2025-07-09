from django.urls import path
from . import views

app_name = 'ownership_checker'

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', views.analyze_website, name='analyze'),
    path('results/', views.results_view, name='results'),
]