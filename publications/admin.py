from django.contrib import admin

from .models import (ASCEJournalStructuralEngineering, DocumentType,
                     JournalPublication)

# Register your models here.

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code")

@admin.register(JournalPublication)
class JournalPublicationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "doc_type","code")
    search_fields = ("name",)
@admin.register(ASCEJournalStructuralEngineering)
class ASCEJournalStructuralEngineering(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year","filename","file_exists")
    search_fields = ("title", "authors", "abstract")
    list_filter = ("volume", "issue", "year")