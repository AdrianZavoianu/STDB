from django.contrib import admin

from .models import DocumentType, JournalPublication

# Register your models here.

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code")

@admin.register(JournalPublication)
class JournalPublicationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "doc_type","code")
    search_fields = ("name",)