from django.urls import path
from .views import get_papers, get_authors

urlpatterns = [
    path('papers/', get_papers),
    path('authors/', get_authors),
]