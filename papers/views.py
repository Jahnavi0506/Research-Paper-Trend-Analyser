from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Q
from collections import Counter
import re

from .models import Paper, Author
from .serializers import PaperSerializer, AuthorSerializer


# 🔹 GET PAPERS (FILTER + SEARCH + SORT)
@api_view(['GET'])
def get_papers(request):
    papers = Paper.objects.all()

    # FILTER BY CATEGORY
    category = request.GET.get('category')
    if category:
        papers = papers.filter(category=category)

    # FILTER BY YEAR
    year = request.GET.get('year')
    if year:
        papers = papers.filter(published_date__year=year)

    # SEARCH (title + summary)
    search = request.GET.get('search')
    if search:
        papers = papers.filter(
            Q(title__icontains=search) |
            Q(summary__icontains=search)
        )

    # SORTING
    sort = request.GET.get('sort')
    if sort == 'latest':
        papers = papers.order_by('-published_date')
    elif sort == 'oldest':
        papers = papers.order_by('published_date')

    serializer = PaperSerializer(papers, many=True)
    return Response(serializer.data)


# 🔹 GET AUTHORS
@api_view(['GET'])
def get_authors(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)


# 🔹 CATEGORY TRENDS
@api_view(['GET'])
def category_trends(request):
    data = (
        Paper.objects
        .values('category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    return Response(data)


# 🔹 PAPER GROWTH
@api_view(['GET'])
def paper_growth(request):
    data = (
        Paper.objects
        .values('published_date__year')
        .annotate(count=Count('id'))
        .order_by('published_date__year')
    )
    return Response(data)


# 🔹 TOP AUTHORS
@api_view(['GET'])
def top_authors(request):
    data = (
        Author.objects
        .annotate(paper_count=Count('paperauthor'))
        .order_by('-paper_count')
    )

    return Response([
        {"author": a.name, "papers": a.paper_count}
        for a in data
    ])


# 🔹 TRENDING KEYWORDS
@api_view(['GET'])
def trending_keywords(request):
    papers = Paper.objects.all()

    words = []

    for paper in papers:
        title_words = re.findall(r'\w+', paper.title.lower())
        words.extend(title_words)

    common = Counter(words).most_common(10)

    return Response([
        {"keyword": k, "count": v}
        for k, v in common
    ])