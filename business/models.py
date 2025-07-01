from django.db import models
from accounts.models import User
from django.utils import timezone
from django.template.loader import render_to_string
import os
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
from io import BytesIO


COUNTY_CHOICES = [
    ('001', 'Mombasa'),
    ('002', 'Kwale'),
    ('003', 'Kilifi'),
    ('004', 'Tana River'),
    ('005', 'Lamu'),
    ('006', 'Taita Taveta'),
    ('007', 'Garissa'),
    ('008', 'Wajir'),
    ('009', 'Mandera'),
    ('010', 'Marsabit'),
    ('011', 'Isiolo'),
    ('012', 'Meru'),
    ('013', 'Tharaka Nithi'),
    ('014', 'Embu'),
    ('015', 'Kitui'),
    ('016', 'Machakos'),
    ('017', 'Makueni'),
    ('018', 'Nyandarua'),
    ('019', 'Nyeri'),
    ('020', 'Kirinyaga'),
    ('021', 'Murang\'a'),
    ('022', 'Kiambu'),
    ('023', 'Turkana'),
    ('024', 'West Pokot'),
    ('025', 'Samburu'),
    ('026', 'Trans Nzoia'),
    ('027', 'Uasin Gishu'),
    ('028', 'Elgeyo Marakwet'),
    ('029', 'Nandi'),
    ('030', 'Baringo'),
    ('031', 'Laikipia'),
    ('032', 'Nakuru'),
    ('033', 'Narok'),
    ('034', 'Kajiado'),
    ('035', 'Kericho'),
    ('036', 'Bomet'),
    ('037', 'Kakamega'),
    ('038', 'Vihiga'),
    ('039', 'Bungoma'),
    ('040', 'Busia'),
    ('041', 'Siaya'),
    ('042', 'Kisumu'),
    ('043', 'Homa Bay'),
    ('044', 'Migori'),
    ('045', 'Kisii'),
    ('046', 'Nyamira'),
    ('047', 'Nairobi')
]

BUSINESS_TYPES = [
    ('sole', 'Sole Proprietorship'),
    ('partnership', 'Partnership'),
    ('company', 'Limited Company'),
    ('cooperative', 'Cooperative Society'),
    ('ngo', 'Non-Governmental Organization'),
    ('other', 'Other')
]

class Business(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPES)
    registration_number = models.CharField(max_length=50, blank=True)
    kra_pin = models.CharField(max_length=20, blank=True)
    county = models.CharField(max_length=3, choices=COUNTY_CHOICES)
    physical_address = models.TextField()
    date_established = models.DateField()
    id_front = models.ImageField(upload_to='ids/front/')
    id_back = models.ImageField(upload_to='ids/back/')
    registration_certificate = models.FileField(upload_to='certificates/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.registration_number and self.is_approved:
            year = timezone.now().year
            count = Business.objects.filter(
                county=self.county,
                business_type=self.business_type,
                created_at__year=year
            ).count() + 1
            seq = str(count).zfill(5)
            self.registration_number = f"CBR/{self.county}/{self.business_type.upper()}/{seq}/{year}"
        super().save(*args, **kwargs)
        if self.is_approved and not self.registration_certificate:
            self.generate_certificate()

    def generate_certificate(self):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        width, height = A4
        y = height - 100

        # Add logo
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
        if os.path.exists(logo_path):
            p.drawImage(logo_path, 240, y, width=120, height=80, preserveAspectRatio=True)
            y -= 100

        # Header
        p.setFont("Helvetica-Bold", 16)
        p.drawCentredString(width / 2, y, "STATE DEPARTMENT OF BUSINESS AND INVESTMENT")
        y -= 30
        p.setFont("Helvetica-Bold", 14)
        p.drawCentredString(width / 2, y, "Certificate of Business Registration")
        y -= 50

        # Business info
        p.setFont("Helvetica", 12)
        info = [
            f"Business Name: {self.name}",
            f"Registration Number: {self.registration_number}",
            f"Business Type: {self.get_business_type_display()}",
            f"KRA PIN: {self.kra_pin}",
            f"County: {self.get_county_display()}",
            f"Physical Address: {self.physical_address}",
            f"Date Established: {self.date_established}",
            f"Date Approved: {self.created_at.date()}",
        ]
        for line in info:
            p.drawString(80, y, line)
            y -= 20

        p.showPage()
        p.save()

        # Save PDF to model
        filename = f"{self.registration_number.replace('/', '_')}.pdf"
        self.registration_certificate.save(filename, ContentFile(buffer.getvalue()), save=False)
        buffer.close()

    def __str__(self):
        return f"{self.name} ({self.get_business_type_display()})"


class PartnershipDetail(models.Model):
    business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name='partnership_detail')
    partners = models.JSONField(help_text="List of partners with names, IDs, PINs, contacts")

class CompanyDetail(models.Model):
    business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name='company_detail')
    directors = models.JSONField(help_text="List of directors")
    shareholders = models.JSONField(help_text="List of shareholders with shares info")
    share_capital = models.DecimalField(max_digits=12, decimal_places=2)
