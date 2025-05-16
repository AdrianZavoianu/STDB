from django.shortcuts import get_object_or_404, render

from publications.models import \
    UnifiedJournalArticles  # or whatever your unified model is


def home(request):
    articles = UnifiedJournalArticles.objects.all()[6108:6112]
    return render(request, "frontend/home.html", {"articles": articles})

