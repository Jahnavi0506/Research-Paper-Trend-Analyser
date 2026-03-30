import time
import requests
import xml.etree.ElementTree as ET
from papers.models import Paper,Author,PaperAuthor
from django.utils.dateparse import parse_datetime

def fetch_arxiv_papers():
    url="http://export.arxiv.org/api/query?search_query=cat:cs.AI&max_results=5"
    headers = {
    "User-Agent": "research-analyzer (yattapujahnavi1801@gmail.com)"
    }
    time.sleep(5)
    response=requests.get(url, headers=headers)
    print(response.status_code)

    print(response.text[:200])

    if response.status_code == 429:
        print("Rate limit hit. Try again later.")
        return
    if response.status_code!=200:
        print("Failed to fetch data from arXiv")
        return
    root=ET.fromstring(response.content)

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title=entry.find("{http://www.w3.org/2005/Atom}title").text
        summary=entry.find("{http://www.w3.org/2005/Atom}summary").text
        published=entry.find("{http://www.w3.org/2005/Atom}published").text
        published_date=parse_datetime(published)

        category=entry.find("{http://arxiv.org/schemas/atom}primary_category").attrib['term']

        paper,created=Paper.objects.get_or_create(
            title=title,
            defaults={
                'summary':summary,
                'published_date':published_date,
                'category':category
            }
        )

        for author in entry.findall("{http://www.w3.org/2005/Atom}author"):

            name=author.find("{http://www.w3.org/2005/Atom}name").text

            author_obj,_=Author.objects.get_or_create(name=name)

            PaperAuthor.objects.get_or_create(
                paper=paper,
                author=author_obj
            )
