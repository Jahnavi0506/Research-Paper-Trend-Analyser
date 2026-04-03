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
class PaperSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()

    class Meta:
        model = Paper
        fields = '__all__'

    def get_authors(self, obj):
        return [pa.author.name for pa in obj.paperauthor_set.all()]
        