from django.db import models

# Create your models here.
class Paper(models.Model):
    title=models.CharField(max_length=500)
    summary=models.TextField()
    published_date=models.DateField()
    category=models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Author(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class PaperAuthor(models.Model):
    paper=models.ForeignKey(Paper,on_delete=models.CASCADE)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author.name} - {self.paper.title}"
