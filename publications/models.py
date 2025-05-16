import os

from django.conf import settings
from django.db import models

# Create your models here.

class DocumentType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Document Type"
        verbose_name_plural = "Document Types"

    def __str__(self):
        return self.name

    def code(self):
        """Returns the ID padded to 2 digits, for use in filenames."""
        return f"{self.id:02}"

class JournalPublication(models.Model):
    name = models.CharField(max_length=255, unique=True)
    doc_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Journal Publication"
        verbose_name_plural = "Journal Publications"

    def __str__(self):
        return self.name

    def code(self):
        """Returns a padded code based on ID for filenames."""
        return f"{self.id:03}"

class BaseJournalArticle(models.Model):
    journal = models.ForeignKey("JournalPublication", on_delete=models.PROTECT)
    title = models.TextField()
    authors = models.TextField()
    abstract = models.TextField(blank=True, null=True)
    year = models.IntegerField()
    doi = models.CharField(max_length=255, unique=True, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    volume = models.IntegerField()
    issue = models.IntegerField(default=0)  # Optional for journals without issues
    article_index = models.IntegerField()

    file_exists = models.BooleanField(default=False)

    FILE_SOURCE_CHOICES = [
        ('S', 'Downloaded'),
        ('O', 'Open Access'),
        ('U', 'Unpaywall'),
        ('L', 'Local/Proprietary'),
    ]
    file_source = models.CharField(
        max_length=1,
        choices=FILE_SOURCE_CHOICES,
        default='S',
        help_text="Source of the PDF file"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def filename(self):
        return f"STDB-{self.publication_code()}-{self.year}-{self.file_source}.pdf"

class ASCEJournalStructuralEngineering(BaseJournalArticle):

    class Meta:
        verbose_name = "ASCE Journal of Structural Engineering Article"
        verbose_name_plural = "ASCE Journal of Structural Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class ASCEJournalStructuralDesignConstructionPractice(BaseJournalArticle):

    class Meta:
        verbose_name = "ASCE Journal of Structural Design and Construction Practice"
        verbose_name_plural = "ASCE Journal of Structural Design and Construction Practice Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class ASCEJournalPerformanceConstructedFacilities(BaseJournalArticle):

    class Meta:
        verbose_name = "ASCE Journal of Performance of Constructed Facilities"
        verbose_name_plural = "ASCE Journal of Performance of Constructed Facilities Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class ASCEJournalCompositesConstruction(BaseJournalArticle):

    class Meta:
        verbose_name = "ASCE Journal of Composites for Construction"
        verbose_name_plural = "ASCE Journal of Composites for Construction Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class ElsevierJournalConstructionalSteelResearch(BaseJournalArticle):
    class Meta:
        verbose_name = "Elsevier Journal of Constructional Steel Research"
        verbose_name_plural = verbose_name + " Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class ElsevierComputersStructures(BaseJournalArticle):
    class Meta:
        verbose_name = "Elsevier Computers and Structures"
        verbose_name_plural = verbose_name + " Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class ElsevierEngineeringStructures(BaseJournalArticle):
    class Meta:
        verbose_name = "Elsevier Engineering Structures"
        verbose_name_plural = verbose_name + " Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class ElsevierFiniteElementsAnalysisDesign(BaseJournalArticle):
    class Meta:
        verbose_name = "Elsevier Finite Elements in Analysis and Design"
        verbose_name_plural = verbose_name + " Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class ElsevierStructuralSafety(BaseJournalArticle):
    class Meta:
        verbose_name = "Elsevier Structural Safety"
        verbose_name_plural = verbose_name + " Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class SpringerEarthquakeEngineeringEngineeringVibrations(BaseJournalArticle):
    class Meta:
        verbose_name = "Springer Earthquake Engineering and Engineering Vibrations"
        verbose_name_plural ="Springer Earthquake Engineering and Engineering Vibrations Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class SpringerInternationalJournalSteelStructures(BaseJournalArticle):
    class Meta:
        verbose_name = "Springer International Journal of Steel Structures"
        verbose_name_plural ="Springer International Journal of Steel Structures Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class SpringerBulletinEarthquakeEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "Springer Bulletin of Earthquake Engineering"
        verbose_name_plural ="Springer Bulletin of Earthquake Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class SpringerStructuralMultidisciplinaryOptimization(BaseJournalArticle):
    class Meta:
        verbose_name = "Springer Structural and Multidisciplinary Optimization"
        verbose_name_plural ="Springer Structural and Multidisciplinary Optimization Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class SpringerMaterialsStructures(BaseJournalArticle):
    class Meta:
        verbose_name = "Springer Materials and Structures"
        verbose_name_plural ="Springer Materials and Structures Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class SpringerComputationalMechanics(BaseJournalArticle):
    class Meta:
        verbose_name = "Springer Computational Mechanics"
        verbose_name_plural ="Springer Computational Mechanics Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class TaylorFrancisJournalEarthquakeEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "Taylor & Francis Journal of Earthquake Engineering"
        verbose_name_plural ="Taylor & Francis Journal of Earthquake Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class TaylorFrancisMechanicsStructuresMaterials(BaseJournalArticle):
    class Meta:
        verbose_name = "Taylor & Francis Mechanics of Structures and Materials"
        verbose_name_plural ="Taylor & Francis Mechanics of Structures and Materials Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class IABSEJournalSeismologyEarthquakeEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "IABSE Journal of Seismology and Earthquake Engineering"
        verbose_name_plural ="IABSE Journal of Seismology and Earthquake Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class WileyStructuralDesignTallSpecialBuildings(BaseJournalArticle):
    class Meta:
        verbose_name = "Wiley The Structural Design of Tall and Special Buildings"
        verbose_name_plural ="Wiley The Structural Design of Tall and Special Buildings Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class WileyEarthquakeEngineeringStructuralDynamics(BaseJournalArticle):
    class Meta:
        verbose_name = "Wiley Earthquake Engineering & Structural Dynamics"
        verbose_name_plural ="Wiley Earthquake Engineering & Structural Dynamics Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class WileyStructuralControlHealthMonitoring(BaseJournalArticle):
    class Meta:
        verbose_name = "Wiley Structural Control and Health Monitoring"
        verbose_name_plural ="Wiley Structural Control and Health Monitoring Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class WileyInternationalJournalNumericalMethodsEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "Wiley International Journal for Numerical Methods in Engineering"
        verbose_name_plural ="Wiley International Journal for Numerical Methods in Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class WSCInternationalJournalStructuralStabilityDynamics(BaseJournalArticle):
    class Meta:
        verbose_name = "WSC International Journal of Structural Stability and Dynamics"
        verbose_name_plural ="WSC International Journal of Structural Stability and Dynamics Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class SageEarthquakeSpectra(BaseJournalArticle):
    class Meta:
        verbose_name = "Sage Earthquake Spectra"
        verbose_name_plural ="Sage Earthquake Spectra Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class SageAdvancesStructuralEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "Sage Advances in Structural Engineering"
        verbose_name_plural ="Sage Advances in Structural Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class JSEEJournalSeismologyEarthquakeEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "JSEE Journal of Seismology and Earthquake Engineering"
        verbose_name_plural ="JSEE Journal of Seismology and Earthquake Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class AISCJournalStructuralEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "AISC Journal of Structural Engineering"
        verbose_name_plural ="AISC Journal of Structural Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class ACIStructuralJournal(BaseJournalArticle):

    class Meta:
        verbose_name = "ACI Structural Journal"
        verbose_name_plural ="ACI Structural Journal Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"



class TaFrEngineeringStructuresandTechnologies(BaseJournalArticle):
    class Meta:
        verbose_name = "Taylor & Francis Engineering Structures and Technologies"
        verbose_name_plural ="Taylor & Francis Engineering Structures and Technologies Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"


class TaFrJournalAsianArchitectureBuildingEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "JAABE Journal of Asian Architecture and Building Engineering"
        verbose_name_plural ="JAABE Journal of Asian Architecture and Building Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"


class SpringerEuropeanJournalWoodProducts(BaseJournalArticle):
    class Meta:
        verbose_name = "Springer European Journal of Wood and Wood Products"
        verbose_name_plural ="Springer European Journal of Wood and Wood Products Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"


class ElsevierConstructionBuildingMaterials(BaseJournalArticle):
    class Meta:
        verbose_name = "Elsevier Construction and Building Materials"
        verbose_name_plural = "Elsevier Construction and Building Materials Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"


class ElsevierJournalBuildingEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "Elsevier Journal of Building Engineering"
        verbose_name_plural = "Elsevier Journal of Building Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"


class JAABEJournalAsianArchitectureuildingEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "JAABE Journal of Asian Architecture and Building Engineering"
        verbose_name_plural = "JAABE Journal of Asian Architecture and Building Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class InderScienceInternationalJournalMaterialsStructuralIntegrity(BaseJournalArticle):
    class Meta:
        verbose_name = "InderScience International Journal of Materials and Structural Integrity"
        verbose_name_plural = "InderScience International Journal of Materials and Structural Integrity Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class InderScienceInternationalJournalStructuraEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "InderScience International Journal of Structural Engineering"
        verbose_name_plural = "InderScience International Journal of Structural Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class InderScienceInternationalJournalEarthquakeImpactEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "InderScience International Journal of Earthquake Impact Engineering"
        verbose_name_plural = "InderScience International Journal of Earthquake Impact Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class InderScienceInternationalJournalMasonryResearchInnovation(BaseJournalArticle):
    class Meta:
        verbose_name = "InderScience International Journal of Masonry Research and Innovation"
        verbose_name_plural = "InderScience International Journal of Masonry Research and Innovation Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class TechnoSteelCompositeStructures(BaseJournalArticle):
    class Meta:
        verbose_name = "Techno Steel and Composite Structures"
        verbose_name_plural = "Techno Steel and Composite Structures Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class TechnoStructuralEngineeringMechanics(BaseJournalArticle):
    class Meta:
        verbose_name = "Techno Structural Engineering Mechanics"
        verbose_name_plural = "Techno Structural Engineering Mechanics Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class TechnoAdvancesConcreteConstruction(BaseJournalArticle):
    class Meta:
        verbose_name = "Techno Advances in Concrete Construction"
        verbose_name_plural = "Techno Advances in Concrete Construction Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class TechnoComputersConcrete(BaseJournalArticle):
    class Meta:
        verbose_name = "Techno Computers and Concrete"
        verbose_name_plural = "Techno Computers and Concrete Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class  TechnoEarthquakesStructures(BaseJournalArticle):
    class Meta:
        verbose_name = "Techno Earthquakes and Structures"
        verbose_name_plural = "Techno Earthquakes and Structures Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class TechnoSmartStructuresSystems(BaseJournalArticle): 
    class Meta:
        verbose_name = "Techno Smart Structures and Systems"
        verbose_name_plural = "Techno Smart Structures and Systems Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class TechnoWindStructures(BaseJournalArticle):
    class Meta:
        verbose_name = "Techno Wind and Structures"
        verbose_name_plural = "Techno Wind and Structures Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class CASPCanadianJournalCivilEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "CASP Canadian Journal of Civil Engineering"
        verbose_name_plural = "CASP Canadian Journal of Civil Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"

class NZSEEBulletinEarthquakeEngineering(BaseJournalArticle):
    class Meta:
        verbose_name = "NZSEE Bulletin of Earthquake Engineering"
        verbose_name_plural = "NZSEE Bulletin of Earthquake Engineering Articles"
        unique_together = ("journal", "volume", "issue", "article_index")

    def publication_code(self):
        doc_type_code = self.journal.doc_type.code()
        journal_code = self.journal.code()
        return f"{doc_type_code}{journal_code}{self.volume:03}{self.issue or 0:02}{self.article_index:03}"


class UnifiedJournalArticles(models.Model):
    journal_name = models.CharField(max_length=255)
    title = models.TextField()
    authors = models.TextField()
    abstract = models.TextField(blank=True, null=True)
    year = models.IntegerField()
    doi = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    volume = models.IntegerField()
    issue = models.IntegerField(default=0)
    article_index = models.IntegerField()
    file_exists = models.BooleanField(default=False)
    publication_code = models.CharField(max_length=50)

    class Meta:
        unique_together = ("journal_name", "volume", "issue", "article_index")
        verbose_name = "0.Unified Journal Article"
        verbose_name = "0.Unified Journal Articles"

    def filename(self):
        return f"STDB-{self.publication_code}-{self.year}.pdf"
    
    def file_url(self):
        if self.file_exists:
            return os.path.join(settings.MEDIA_URL, 'publications', self.filename())
        return None



class Country(models.Model):
    name = models.CharField(max_length=128)
    alpha2 = models.CharField(max_length=2, unique=True)
    alpha3 = models.CharField(max_length=3, unique=True)
    numeric = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return f"{self.name} ({self.alpha3})"


class ConferenceProceeding(models.Model):
    name = models.CharField(max_length=255, unique=True)
    doc_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Conference Proceding"
        verbose_name_plural = "Conference Proceedings"

    def __str__(self):
        return self.name

    def code(self):
        """Returns a padded code based on ID for filenames."""
        return f"{self.id:03}"

class BaseConferenceArticle(models.Model):
    conference = models.ForeignKey("ConferenceProceeding", on_delete=models.PROTECT)
    title = models.TextField()
    authors = models.TextField()
    abstract = models.TextField(blank=True, null=True)
    year = models.IntegerField()
    edition = models.IntegerField()
    url = models.URLField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    article_index = models.IntegerField()

    file_exists = models.BooleanField(default=False)

    FILE_SOURCE_CHOICES = [
        ('S', 'Downloaded'),
        ('O', 'Open Access'),
        ('U', 'Unpaywall'),
        ('L', 'Local/Proprietary'),
    ]
    file_source = models.CharField(
        max_length=1,
        choices=FILE_SOURCE_CHOICES,
        default='S',
        help_text="Source of the PDF file"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def filename(self):
        return f"STDB-{self.publication_code()}-{self.year}-{self.file_source}.pdf"

class WCEEProceedings(BaseConferenceArticle):

    class Meta:
        verbose_name = "World Conference on Earthquake Engineering Article"
        verbose_name_plural = "World Conference on Earthquake Engineering Articles"
        unique_together = ("conference", "edition","country","article_index")

    def publication_code(self):
        doc_type_code = self.conference.doc_type.code()
        conference_code = self.conference.code()
        country_code = self.country.numeric
        return f"{doc_type_code}{conference_code}{self.edition:03}{country_code}{self.article_index:04}"


class PCEEProceedings(BaseConferenceArticle):

    class Meta:
        verbose_name = "Pacific Conference on Earthquake Engineering Article"
        verbose_name_plural = "Pacific Conference on Earthquake Engineering Articles"
        unique_together = ("conference", "edition","country","article_index")

    def publication_code(self):
        doc_type_code = self.conference.doc_type.code()
        conference_code = self.conference.code()
        country_code = self.country.numeric
        return f"{doc_type_code}{conference_code}{self.edition:03}{country_code}{self.article_index:04}"


class UnifiedConferenceArticles(models.Model):
    conference_name = models.CharField(max_length=255)
    title = models.TextField()
    authors = models.TextField()
    abstract = models.TextField(blank=True, null=True)
    year = models.IntegerField()
    edition = models.IntegerField()
    url = models.URLField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    article_index = models.IntegerField()

    file_exists = models.BooleanField(default=False)

    FILE_SOURCE_CHOICES = [
        ('S', 'Downloaded'),
        ('O', 'Open Access'),
        ('U', 'Unpaywall'),
        ('L', 'Local/Proprietary'),
    ]
    file_source = models.CharField(
        max_length=1,
        choices=FILE_SOURCE_CHOICES,
        default='S',
        help_text="Source of the PDF file"
    )

    filename = models.CharField(max_length=255)

    class Meta:
        verbose_name = "0.Unified Conference Article"
        verbose_name_plural = "0.Unified Conference Articles"
        unique_together = ("conference_name", "edition", "country", "article_index")

    def __str__(self):
        return self.title


class BookCategoryLevel1(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BookCategoryLevel2(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(BookCategoryLevel1, on_delete=models.CASCADE, related_name="subcategories")

    class Meta:
        unique_together = ("name", "parent")

    def __str__(self):
        return f"{self.parent} / {self.name}"

class BookCategoryLevel3(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(BookCategoryLevel2, on_delete=models.CASCADE, related_name="subsubcategories")

    class Meta:
        unique_together = ("name", "parent")

    def __str__(self):
        return f"{self.parent} / {self.name}"

class BookPublication(models.Model):
    doc_type = models.ForeignKey("DocumentType", on_delete=models.PROTECT)

    category_lvl1 = models.ForeignKey(BookCategoryLevel1, on_delete=models.PROTECT)
    category_lvl2 = models.ForeignKey(BookCategoryLevel2, on_delete=models.PROTECT)
    category_lvl3 = models.ForeignKey(BookCategoryLevel3, on_delete=models.PROTECT)
    title = models.TextField()
    authors = models.TextField()
    content_summary = models.TextField(blank=True, null=True)
    year = models.IntegerField()
    publisher = models.CharField(max_length=255, blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    url = models.URLField(blank=True, null=True)

    book_index = models.IntegerField()

    FILE_SOURCE_CHOICES = [
        ('S', 'Downloaded'),
        ('O', 'Open Access'),
        ('U', 'Unpaywall'),
        ('L', 'Local/Proprietary'),
    ]
    file_source = models.CharField(
        max_length=1,
        choices=FILE_SOURCE_CHOICES,
        default='S',
        help_text="Source of the PDF file"
    )

    file_exists = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Book Entry"
        verbose_name_plural = "Book Entries"
        unique_together = (
            "category_lvl1", "category_lvl2", "category_lvl3", "book_index"
        )

    def __str__(self):
        return self.title

    def publication_code(self):
        doc_type_code = self.doc_type.code()
        lvl1 = self.category_lvl1.id
        lvl2 = self.category_lvl2.id
        lvl3 = self.category_lvl3.id
        return f"{doc_type_code}{lvl1:03}{lvl2:03}{lvl3:03}{self.book_index:04}"

    def filename(self):
        return f"STDB-{self.publication_code()}-{self.year}-{self.file_source}.pdf"


class GuidelineCategoryLevel1(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class GuidelineCategoryLevel2(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(GuidelineCategoryLevel1, on_delete=models.CASCADE, related_name="subcategories")

    class Meta:
        unique_together = ("name", "parent")

    def __str__(self):
        return f"{self.parent} / {self.name}"

class GuidelineCategoryLevel3(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(GuidelineCategoryLevel2, on_delete=models.CASCADE, related_name="subsubcategories")

    class Meta:
        unique_together = ("name", "parent")

    def __str__(self):
        return f"{self.parent} / {self.name}"

class GuidelinePublication(models.Model):
    doc_type = models.ForeignKey("DocumentType", on_delete=models.PROTECT)

    category_lvl1 = models.ForeignKey(GuidelineCategoryLevel1, on_delete=models.PROTECT)
    category_lvl2 = models.ForeignKey(GuidelineCategoryLevel2, on_delete=models.PROTECT)
    category_lvl3 = models.ForeignKey(GuidelineCategoryLevel3, on_delete=models.PROTECT)
    title = models.TextField()
    authors = models.TextField()
    content_summary = models.TextField(blank=True, null=True)
    year = models.IntegerField()
    publisher = models.CharField(max_length=255, blank=True)


    guideline_index = models.IntegerField()

    FILE_SOURCE_CHOICES = [
        ('S', 'Downloaded'),
        ('O', 'Open Access'),
        ('U', 'Unpaywall'),
        ('L', 'Local/Proprietary'),
    ]
    file_source = models.CharField(
        max_length=1,
        choices=FILE_SOURCE_CHOICES,
        default='S',
        help_text="Source of the PDF file"
    )

    file_exists = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Guideline Entry"
        verbose_name_plural = "Guideline Entries"
        unique_together = (
            "category_lvl1", "category_lvl2", "category_lvl3", "guideline_index"
        )

    def __str__(self):
        return self.title

    def publication_code(self):
        doc_type_code = self.doc_type.code()
        lvl1 = self.category_lvl1.id
        lvl2 = self.category_lvl2.id
        lvl3 = self.category_lvl3.id
        return f"{doc_type_code}{lvl1:03}{lvl2:03}{lvl3:03}{self.guideline_index:04}"

    def filename(self):
        return f"STDB-{self.publication_code()}-{self.year}-{self.file_source}.pdf"



class ReportCategoryLevel1(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ReportCategoryLevel2(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(ReportCategoryLevel1, on_delete=models.CASCADE, related_name="subcategories")

    class Meta:
        unique_together = ("name", "parent")

    def __str__(self):
        return f"{self.parent} / {self.name}"

class ReportCategoryLevel3(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(ReportCategoryLevel2, on_delete=models.CASCADE, related_name="subsubcategories")

    class Meta:
        unique_together = ("name", "parent")

    def __str__(self):
        return f"{self.parent} / {self.name}"

class ReportPublication(models.Model):
    doc_type = models.ForeignKey("DocumentType", on_delete=models.PROTECT)

    category_lvl1 = models.ForeignKey(ReportCategoryLevel1, on_delete=models.PROTECT)
    category_lvl2 = models.ForeignKey(ReportCategoryLevel2, on_delete=models.PROTECT)
    category_lvl3 = models.ForeignKey(ReportCategoryLevel3, on_delete=models.PROTECT)
    title = models.TextField()
    authors = models.TextField()
    content_summary = models.TextField(blank=True, null=True)
    year = models.IntegerField()
    publisher = models.CharField(max_length=255, blank=True)


    report_index = models.IntegerField()

    FILE_SOURCE_CHOICES = [
        ('S', 'Downloaded'),
        ('O', 'Open Access'),
        ('U', 'Unpaywall'),
        ('L', 'Local/Proprietary'),
    ]
    file_source = models.CharField(
        max_length=1,
        choices=FILE_SOURCE_CHOICES,
        default='S',
        help_text="Source of the PDF file"
    )

    file_exists = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Report Entry"
        verbose_name_plural = "Report Entries"
        unique_together = (
            "category_lvl1", "category_lvl2", "category_lvl3", "report_index"
        )

    def __str__(self):
        return self.title

    def publication_code(self):
        doc_type_code = self.doc_type.code()
        lvl1 = self.category_lvl1.id
        lvl2 = self.category_lvl2.id
        lvl3 = self.category_lvl3.id
        return f"{doc_type_code}{lvl1:03}{lvl2:03}{lvl3:03}{self.report_index:04}"

    def filename(self):
        return f"STDB-{self.publication_code()}-{self.year}-{self.file_source}.pdf"



class StandardCategoryLevel1(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class StandardCategoryLevel2(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(StandardCategoryLevel1, on_delete=models.CASCADE, related_name="subcategories")

    class Meta:
        unique_together = ("name", "parent")

    def __str__(self):
        return f"{self.parent} / {self.name}"

class StandardCategoryLevel3(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(StandardCategoryLevel2, on_delete=models.CASCADE, related_name="subsubcategories")

    class Meta:
        unique_together = ("name", "parent")

    def __str__(self):
        return f"{self.parent} / {self.name}"

class StandardPublication(models.Model):
    doc_type = models.ForeignKey("DocumentType", on_delete=models.PROTECT)

    category_lvl1 = models.ForeignKey(StandardCategoryLevel1, on_delete=models.PROTECT)
    category_lvl2 = models.ForeignKey(StandardCategoryLevel2, on_delete=models.PROTECT)
    category_lvl3 = models.ForeignKey(StandardCategoryLevel3, on_delete=models.PROTECT)
    title = models.TextField()
    authors = models.TextField()
    content_summary = models.TextField(blank=True, null=True)
    year = models.IntegerField()
    publisher = models.CharField(max_length=255, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT,default=171)

    FILE_SOURCE_CHOICES = [
        ('S', 'Downloaded'),
        ('O', 'Open Access'),
        ('U', 'Unpaywall'),
        ('L', 'Local/Proprietary'),
    ]
    file_source = models.CharField(
        max_length=1,
        choices=FILE_SOURCE_CHOICES,
        default='S',
        help_text="Source of the PDF file"
    )

    file_exists = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Standard Entry"
        verbose_name_plural = "Standard Entries"
        unique_together = (
            "category_lvl1", "category_lvl2", "category_lvl3", "country"
        )

    def __str__(self):
        return self.title

    def publication_code(self):
        doc_type_code = self.doc_type.code()
        lvl1 = self.category_lvl1.id
        lvl2 = self.category_lvl2.id
        lvl3 = self.category_lvl3.id
        country_code = self.country.numeric
        return f"{doc_type_code}{lvl1:03}{lvl2:03}{lvl3:03}0{country_code}"

    def filename(self):
        return f"STDB-{self.publication_code()}-{self.year}-{self.file_source}.pdf"


class CodeCategoryLevel1(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CodeCategoryLevel2(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(CodeCategoryLevel1, on_delete=models.CASCADE, related_name="subcategories")

    class Meta:
        unique_together = ("name", "parent")

    def __str__(self):
        return f"{self.parent} / {self.name}"

class CodePublication(models.Model):
    doc_type = models.ForeignKey("DocumentType", on_delete=models.PROTECT)

    category_lvl1 = models.ForeignKey(CodeCategoryLevel1, on_delete=models.PROTECT)
    category_lvl2 = models.ForeignKey(CodeCategoryLevel2, on_delete=models.PROTECT)

    title = models.TextField()
    authors = models.TextField()
    content_summary = models.TextField(blank=True, null=True)
    year = models.IntegerField()
    publisher = models.CharField(max_length=255, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT,default=171)
    code_index = models.IntegerField()

    FILE_SOURCE_CHOICES = [
        ('S', 'Downloaded'),
        ('O', 'Open Access'),
        ('U', 'Unpaywall'),
        ('L', 'Local/Proprietary'),
    ]
    file_source = models.CharField(
        max_length=1,
        choices=FILE_SOURCE_CHOICES,
        default='S',
        help_text="Source of the PDF file"
    )

    file_exists = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Code Entry"
        verbose_name_plural = "Code Entries"
        unique_together = (
            "category_lvl1", "category_lvl2",  "code_index"
        )

    def __str__(self):
        return self.title

    def publication_code(self):
        doc_type_code = self.doc_type.code()
        lvl1 = self.category_lvl1.id
        lvl2 = self.category_lvl2.id
        country_code = self.country.numeric
        return f"{doc_type_code}{lvl1:03}{lvl2:03}{country_code}{self.code_index:04}"

    def filename(self):
        return f"STDB-{self.publication_code()}-{self.year}-{self.file_source}.pdf"










