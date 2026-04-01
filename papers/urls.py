from django.urls import path
from .views import get_papers, get_authors, paper_growth, top_authors
from .views import category_trends

urlpatterns = [
    path('papers/', get_papers),
    path('authors/', get_authors),
    path('trends/categories/', category_trends),
    path('trends/growth/', paper_growth),
    path('trends/authors/', top_authors),
]