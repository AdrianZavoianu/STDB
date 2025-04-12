from django.contrib import admin

from .models import (ACIStructuralJournal, AISCJournalStructuralEngineering,
                     ASCEJournalCompositesConstruction,
                     ASCEJournalPerformanceConstructedFacilities,
                     ASCEJournalStructuralDesignConstructionPractice,
                     ASCEJournalStructuralEngineering, DocumentType,
                     ElsevierComputersStructures,
                     ElsevierConstructionBuildingMaterials,
                     ElsevierEngineeringStructures,
                     ElsevierFiniteElementsAnalysisDesign,
                     ElsevierJournalBuildingEngineering,
                     ElsevierJournalConstructionalSteelResearch,
                     ElsevierStructuralSafety,
                     IABSEJournalSeismologyEarthquakeEngineering,
                     JournalPublication,
                     JSEEJournalSeismologyEarthquakeEngineering,
                     SageAdvancesStructuralEngineering, SageEarthquakeSpectra,
                     SpringerBulletinEarthquakeEngineering,
                     SpringerComputationalMechanics,
                     SpringerEarthquakeEngineeringEngineeringVibrations,
                     SpringerEuropeanJournalWoodProducts,
                     SpringerInternationalJournalSteelStructures,
                     SpringerMaterialsStructures,
                     SpringerStructuralMultidisciplinaryOptimization,
                     TaFrEngineeringStructuresandTechnologies,
                     TaFrJournalAsianArchitectureBuildingEngineering,
                     TaylorFrancisJournalEarthquakeEngineering,
                     TaylorFrancisMechanicsStructuresMaterials,
                     UnifiedArticles,
                     WileyEarthquakeEngineeringStructuralDynamics,
                     WileyInternationalJournalNumericalMethodsEngineering,
                     WileyStructuralControlHealthMonitoring,
                     WileyStructuralDesignTallSpecialBuildings,
                     WSCInternationalJournalStructuralStabilityDynamics)


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
    list_filter = ("volume", "issue", "year", "file_exists")

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

@admin.register(TaylorFrancisJournalEarthquakeEngineering)
class TaylorFrancisJournalEarthquakeEngineeringAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(TaylorFrancisMechanicsStructuresMaterials)
class TaylorFrancisMechanicsStructuresMaterialsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(IABSEJournalSeismologyEarthquakeEngineering)
class IABSEJournalSeismologyEarthquakeEngineeringAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(WileyStructuralDesignTallSpecialBuildings)
class WileyStructuralDesignTallSpecialBuildingsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(WileyEarthquakeEngineeringStructuralDynamics)
class WileyEarthquakeEngineeringStructuralDynamicsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(WileyStructuralControlHealthMonitoring)
class WileyStructuralControlHealthMonitoringAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(WileyInternationalJournalNumericalMethodsEngineering)
class WileyInternationalJournalNumericalMethodsEngineeringAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(WSCInternationalJournalStructuralStabilityDynamics)
class WSCInternationalJournalStructuralStabilityDynamicsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(SageEarthquakeSpectra)
class SageEarthquakeSpectraAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(SageAdvancesStructuralEngineering)
class SageAdvancesStructuralEngineeringAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")

@admin.register(JSEEJournalSeismologyEarthquakeEngineering)
class JSEEJournalSeismologyEarthquakeEngineeringAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")

@admin.register(AISCJournalStructuralEngineering)
class AISCJournalStructuralEngineeringAdmin(admin.ModelAdmin):
    list_display = ("id", "title","authors", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")

@admin.register(ACIStructuralJournal)
class ACIStructuralJournalAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")

@admin.register(UnifiedArticles)
class UnifiedArticlesAdmin(admin.ModelAdmin):
    list_display = ("id", "title","authors","journal_name", "volume", "issue", "article_index", "year", "filename", "file_exists")
    search_fields = ("title","authors", "volume")


@admin.register(TaFrEngineeringStructuresandTechnologies)
class TaFrEngineeringStructuresandTechnologiesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")


@admin.register(TaFrJournalAsianArchitectureBuildingEngineering)
class TaFrJournalAsianArchitectureBuildingEngineeringAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")

@admin.register(SpringerEuropeanJournalWoodProducts)
class SpringerEuropeanJournalWoodProductsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")

@admin.register(ElsevierConstructionBuildingMaterials)
class ElsevierConstructionBuildingMaterialsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")

@admin.register(ElsevierJournalBuildingEngineering)
class ElsevierJournalBuildingEngineeringAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")