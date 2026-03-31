from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Paper,Author,PaperAuthor
from .serializers import PaperSerializer,AuthorSerializer,PaperAuthorSerializer

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

