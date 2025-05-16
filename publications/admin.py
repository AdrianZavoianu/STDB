from django.contrib import admin

from .models import (
    ACIStructuralJournal, AISCJournalStructuralEngineering,
    ASCEJournalCompositesConstruction,
    ASCEJournalPerformanceConstructedFacilities,
    ASCEJournalStructuralDesignConstructionPractice,
    ASCEJournalStructuralEngineering, BookCategoryLevel1, BookCategoryLevel2,
    BookCategoryLevel3, BookPublication, CASPCanadianJournalCivilEngineering,
    CodeCategoryLevel1, CodeCategoryLevel2, CodePublication,
    ConferenceProceeding, Country, DocumentType, ElsevierComputersStructures,
    ElsevierConstructionBuildingMaterials, ElsevierEngineeringStructures,
    ElsevierFiniteElementsAnalysisDesign, ElsevierJournalBuildingEngineering,
    ElsevierJournalConstructionalSteelResearch, ElsevierStructuralSafety,
    GuidelineCategoryLevel1, GuidelineCategoryLevel2, GuidelineCategoryLevel3,
    GuidelinePublication, IABSEJournalSeismologyEarthquakeEngineering,
    InderScienceInternationalJournalEarthquakeImpactEngineering,
    InderScienceInternationalJournalMasonryResearchInnovation,
    InderScienceInternationalJournalMaterialsStructuralIntegrity,
    InderScienceInternationalJournalStructuraEngineering, JournalPublication,
    JSEEJournalSeismologyEarthquakeEngineering,
    NZSEEBulletinEarthquakeEngineering, PCEEProceedings, ReportCategoryLevel1,
    ReportCategoryLevel2, ReportCategoryLevel3, ReportPublication,
    SageAdvancesStructuralEngineering, SageEarthquakeSpectra,
    SpringerBulletinEarthquakeEngineering, SpringerComputationalMechanics,
    SpringerEarthquakeEngineeringEngineeringVibrations,
    SpringerEuropeanJournalWoodProducts,
    SpringerInternationalJournalSteelStructures, SpringerMaterialsStructures,
    SpringerStructuralMultidisciplinaryOptimization, StandardCategoryLevel1,
    StandardCategoryLevel2, StandardCategoryLevel3, StandardPublication,
    TaFrEngineeringStructuresandTechnologies,
    TaFrJournalAsianArchitectureBuildingEngineering,
    TaylorFrancisJournalEarthquakeEngineering,
    TaylorFrancisMechanicsStructuresMaterials,
    TechnoAdvancesConcreteConstruction, TechnoComputersConcrete,
    TechnoEarthquakesStructures, TechnoSmartStructuresSystems,
    TechnoSteelCompositeStructures, TechnoStructuralEngineeringMechanics,
    TechnoWindStructures, UnifiedConferenceArticles, UnifiedJournalArticles,
    WCEEProceedings, WileyEarthquakeEngineeringStructuralDynamics,
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

@admin.register(InderScienceInternationalJournalMaterialsStructuralIntegrity)
class InderScienceInternationalJournalMaterialsStructuralIntegrityAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")


@admin.register(InderScienceInternationalJournalStructuraEngineering)
class InderScienceInternationalJournalStructuraEngineeringAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")

@admin.register(InderScienceInternationalJournalEarthquakeImpactEngineering)
class InderScienceInternationalJournalEarthquakeImpactEngineeringAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")

@admin.register(InderScienceInternationalJournalMasonryResearchInnovation)
class InderScienceInternationalJournalMasonryResearchInnovationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")

@admin.register(TechnoSteelCompositeStructures)
class TechnoSteelCompositeStructuresAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")

@admin.register(TechnoStructuralEngineeringMechanics)
class TechnoStructuralEngineeringMechanicsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")

@admin.register(TechnoAdvancesConcreteConstruction)
class TechnoAdvancesConcreteConstructionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")

@admin.register(TechnoComputersConcrete)
class TechnoComputersConcreteAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")

@admin.register(TechnoEarthquakesStructures)
class TechnoEarthquakesStructuresAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")

@admin.register(TechnoSmartStructuresSystems)
class TechnoSmartStructuresSystemsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")

@admin.register(TechnoWindStructures)
class TechnoWindStructuresAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")


@admin.register(NZSEEBulletinEarthquakeEngineering)
class NZSEEBulletinEarthquakeEngineeringAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")

@admin.register(CASPCanadianJournalCivilEngineering)
class CASPCanadianJournalCivilEngineeringAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "volume", "issue", "article_index", "year", "filename", "file_exists")
    list_filter = ("volume", "issue", "year", "file_exists")
    search_fields = ("title", "volume")

@admin.register(UnifiedJournalArticles)
class UnifiedJournalArticlesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "authors", "journal_name", "volume", "issue", "article_index", "year", "filename", "file_exists")
    search_fields = ("title", "authors", "volume")

@admin.register(ConferenceProceeding)
class ConferenceProceedingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "doc_type", "code")

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "numeric")

@admin.register(WCEEProceedings)
class WCEEProceedingsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "edition", "country", "article_index", "year", "filename", "file_exists")
    list_filter = ("edition", "country")

@admin.register(PCEEProceedings)
class PCEEProceedingsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "edition", "country", "article_index", "year", "filename", "file_exists")
    list_filter = ("edition", "country")

@admin.register(UnifiedConferenceArticles)
class UnifiedConferenceArticlesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "authors", "conference_name", "edition", "country", "article_index", "year", "filename", "file_exists")
    search_fields = ("title", "authors", "edition")

@admin.register(BookPublication)
class BookPublicationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "authors","filename", "file_exists")

@admin.register(BookCategoryLevel1)
class BookCategoryLevel1Admin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(BookCategoryLevel2)
class BookCategoryLevel2Admin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(BookCategoryLevel3)
class BookCategoryLevel3Admin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(GuidelinePublication)
class GuidelinePublicationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "authors","filename", "file_exists")

@admin.register(GuidelineCategoryLevel1)
class GuidelineCategoryLevel1Admin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(GuidelineCategoryLevel2)
class GuidelineCategoryLevel2Admin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(GuidelineCategoryLevel3)
class GuidelineCategoryLevel3Admin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(ReportPublication)
class ReportPublicationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "authors","filename", "file_exists")

@admin.register(ReportCategoryLevel1)
class ReportCategoryLevel1Admin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(ReportCategoryLevel2)
class ReportCategoryLevel2Admin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(ReportCategoryLevel3)
class ReportCategoryLevel3Admin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(StandardPublication)
class StandardPublicationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "authors","filename", "file_exists")

@admin.register(StandardCategoryLevel1)
class StandardCategoryLevel1Admin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(StandardCategoryLevel2)
class StandardCategoryLevel2Admin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(StandardCategoryLevel3)
class StandardCategoryLevel3Admin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(CodePublication)
class CodePublicationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "authors","filename", "file_exists")

@admin.register(CodeCategoryLevel1)
class StandardCategoryLevel1Admin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(CodeCategoryLevel2)
class StandardCategoryLevel2Admin(admin.ModelAdmin):
    list_display = ("id", "name")