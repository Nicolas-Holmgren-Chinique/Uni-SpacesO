from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Textbook, StudyMaterial, Subject
import requests

def library_home(request):
    subjects = Subject.objects.all()
    recent_uploads = StudyMaterial.objects.order_by('-created_at')[:5]
    featured_books = Textbook.objects.order_by('?')[:4] # Random featured
    
    context = {
        'subjects': subjects,
        'recent_uploads': recent_uploads,
        'featured_books': featured_books,
    }
    return render(request, 'library/home.html', context)

def search_books(request):
    query = request.GET.get('q', '')
    local_results = []
    api_results = []
    
    if query:
        # 1. Search local curated DB
        local_results = Textbook.objects.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query) |
            Q(subject__name__icontains=query)
        )
        
        # 2. Search Open Library API (free, no key needed)
        try:
            # Searching for full text or title
            url = f"https://openlibrary.org/search.json?q={query}&limit=12"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                for doc in data.get('docs', []):
                    # Prioritize items with ebook count or fulltext
                    cover_id = doc.get('cover_i')
                    cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else None
                    
                    # Determine availability
                    has_fulltext = doc.get('has_fulltext', False)
                    ebook_count = doc.get('ebook_count_i', 0)
                    ia_id = doc.get('ia', [None])[0]
                    
                    # Construct Google Shopping/Search link for "cheapest option"
                    isbn = doc.get('isbn', [None])[0]
                    shopping_url = f"https://www.google.com/search?tbm=shop&q=isbn:{isbn}" if isbn else f"https://www.google.com/search?tbm=shop&q={doc.get('title')}"

                    api_results.append({
                        'title': doc.get('title'),
                        'author': ', '.join(doc.get('author_name', [])[:2]),
                        'year': doc.get('first_publish_year'),
                        'key': doc.get('key'), # /works/OL...
                        'cover_url': cover_url,
                        'has_fulltext': has_fulltext,
                        'ebook_count': ebook_count,
                        'ia': ia_id,
                        'shopping_url': shopping_url
                    })
        except Exception as e:
            print(f"Open Library API Error: {e}")

    context = {
        'query': query,
        'local_results': local_results,
        'api_results': api_results,
    }
    return render(request, 'library/search_results.html', context)

@login_required
def upload_material(request):
    # Placeholder for upload logic
    # In a real implementation, use a ModelForm
    return render(request, 'library/upload.html')
