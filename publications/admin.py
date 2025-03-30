from django.contrib import admin

from .models import (ASCEJournalCompositesConstruction,
                     ASCEJournalPerformanceConstructedFacilities,
                     ASCEJournalStructuralDesignConstructionPractice,
                     ASCEJournalStructuralEngineering, DocumentType,
                     ElsevierComputersStructures,
                     ElsevierEngineeringStructures,
                     ElsevierFiniteElementsAnalysisDesign,
                     ElsevierJournalConstructionalSteelResearch,
                     ElsevierStructuralSafety, JournalPublication,
                     SpringerBulletinEarthquakeEngineering,
                     SpringerComputationalMechanics,
                     SpringerEarthquakeEngineeringEngineeringVibrations,
                     SpringerInternationalJournalSteelStructures,
                     SpringerMaterialsStructures,
                     SpringerStructuralMultidisciplinaryOptimization)


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code")

@admin.register(JournalPublication)
class JournalPublicationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "doc_type", "code")

@admin.register(ASCEJournalStructuralEngineering)
class ASCEJournalStructuralEngineeringAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(ASCEJournalStructuralDesignConstructionPractice)
class ASCEJournalStructuralDesignConstructionPracticeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(ASCEJournalCompositesConstruction)
class ASCEJournalCompositesConstructionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(ASCEJournalPerformanceConstructedFacilities)
class ASCEJournalPerformanceConstructedFacilitiesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(ElsevierJournalConstructionalSteelResearch)
class ElsevierJournalConstructionalSteelResearchAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(ElsevierComputersStructures)
class ElsevierComputersStructuresAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(ElsevierEngineeringStructures)
class ElsevierEngineeringStructuresAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(ElsevierFiniteElementsAnalysisDesign)
class ElsevierFiniteElementsAnalysisDesignAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(ElsevierStructuralSafety)
class ElsevierStructuralSafetyAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(SpringerEarthquakeEngineeringEngineeringVibrations)
class SpringerEarthquakeEngineeringEngineeringVibrationsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(SpringerInternationalJournalSteelStructures)
class SpringerInternationalJournalSteelStructuresAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(SpringerBulletinEarthquakeEngineering)
class SpringerBulletinEarthquakeEngineeringAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(SpringerStructuralMultidisciplinaryOptimization)
class SpringerStructuralMultidisciplinaryOptimizationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(SpringerMaterialsStructures)
class SpringerMaterialsStructuresAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(SpringerComputationalMechanics)
class SpringerComputationalMechanicsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

