from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Paper,Author,PaperAuthor
from .serializers import PaperSerializer,AuthorSerializer,PaperAuthorSerializer
from django.db.models import Count

# Create your views here.
@api_view(['GET'])
def get_papers(request):
    papers=Paper.objects.all()
    categeory=request.GET.get('categeory')
    if categeory:
        papers=papers.filter(category=categeory)
    
    year=request.GET.get('year')
    if year:
        papers=papers.filter(published_date__year=year) 

    search=request.GET.get('search')
    if search:
        papers=papers.filter(title__icontains=search) | papers.filter(summary__icontains=search)
    
    serializer=PaperSerializer(papers,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_authors(request):
    authors=Author.objects.all()
    serializer=AuthorSerializer(authors,many=True)
    return Response(serializer.data)    

@api_view(['GET'])
def category_trends(request):
    data=(
        Paper.objects
        .values('category')           #group by category
        .annotate(count=Count('id')) #count papers in each category
        .order_by('-count')          #order by count desc

    )
    return Response(data)

@api_view(['GET'])
def paper_growth(request):
    data=(
        Paper.objects
        .values('published_date__year') #group by year
        .annotate(count=Count('id'))     #count papers each year
        .order_by('published_date__year') #order by year asc

    )
    return Response(data)

from django.db.models import Count

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