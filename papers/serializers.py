from rest_framework import serializers
from .models import Paper,Author,PaperAuthor

class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model=Paper
        fields='__all__'
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields='__all__'
class PaperAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=PaperAuthor
        fields='__all__'
        