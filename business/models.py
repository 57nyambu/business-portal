from django.db import models
from accounts.models import User
from django.utils import timezone

import os
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from io import BytesIO
import os
from django.conf import settings
from django.core.files.base import ContentFile

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

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

class Business(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPES)
    registration_number = models.CharField(max_length=50, blank=True)
    kra_pin = models.CharField(max_length=20, blank=True)
    county = models.CharField(max_length=3, choices=COUNTY_CHOICES)
    physical_address = models.CharField(max_length=50, blank=True)
    date_established = models.DateField()
    id_front = models.ImageField(upload_to='ids/front/', blank=True, null=True)
    id_back = models.ImageField(upload_to='ids/back/', blank=True, null=True)
    registration_certificate = models.FileField(upload_to='certificates/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        if not self.registration_number and self.status == 'approved':
            year = timezone.now().year
            count = Business.objects.filter(
                county=self.county,
                business_type=self.business_type,
                created_at__year=year
            ).count() + 1
            seq = str(count).zfill(5)
            self.registration_number = f"CBR/{self.county}/{self.business_type.upper()}/{seq}/{year}"
        super().save(*args, **kwargs)
        if self.status == 'approved' and not self.registration_certificate:
            self.generate_certificate()

    def generate_certificate(self):
        """Generate a professional certificate with enhanced design"""
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        
        width, height = A4
        
        # Define official colors
        primary_blue = HexColor("#182d49")
        secondary_blue = HexColor('#2d4a6b') 
        official_red = HexColor('#c53030')
        gold_accent = HexColor('#d69e2e')
        light_gray = HexColor("#c7c7c7")
        text_gray = HexColor("#262e3d")
        
        # Create official header with gradient background
        header_height = 180
        p.setFillColor(primary_blue)
        p.rect(0, height - header_height, width, header_height, fill=1, stroke=0)
        
        # Add red gradient accent
        p.setFillColor(official_red)
        p.rect(0, height - header_height, width, 20, fill=1, stroke=0)
        
        # Add texture pattern to header
        p.setStrokeColor(HexColor('#ffffff'))
        p.setLineWidth(0.5)
        for i in range(0, int(width), 30):
            p.line(i, height - header_height, i, height)
        
        # Start positioning from header
        y_position = height - 50
        
        # Coat of Arms - properly sized and positioned
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'Coat_of_arms.png')
        if os.path.exists(logo_path):
            # Create elegant circular frame for coat of arms
            logo_size = 100
            logo_x = width / 2 - logo_size / 2
            logo_y = y_position - logo_size
            
            # Outer decorative ring
            p.setFillColor(gold_accent)
            p.circle(logo_x + logo_size/2, logo_y + logo_size/2, logo_size/2 + 8, fill=1, stroke=0)
            
            # White background circle
            p.setFillColor(HexColor('#ffffff'))
            p.circle(logo_x + logo_size/2, logo_y + logo_size/2, logo_size/2 + 4, fill=1, stroke=0)
            
            # Inner border
            p.setStrokeColor(primary_blue)
            p.setLineWidth(2)
            p.circle(logo_x + logo_size/2, logo_y + logo_size/2, logo_size/2 + 2, fill=0, stroke=1)
            
            # Place the coat of arms image
            p.drawImage(logo_path, logo_x, logo_y, width=logo_size, height=logo_size, 
                    preserveAspectRatio=True, mask='auto')
            y_position -= 120
        # Government titles on header
        p.setFillColor(HexColor('#ffffff'))
        p.setFont("Helvetica-Bold", 20)
        p.drawCentredString(width / 2, y_position, "REPUBLIC OF KENYA")
        y_position -= 25
        
        p.setFont("Helvetica-Bold", 14)
        p.drawCentredString(width / 2, y_position, "STATE DEPARTMENT OF TRADE AND INVESTMENT")
        
        # Main content area with white background
        content_y = height - 200
        p.setFillColor(HexColor('#ffffff'))
        p.rect(0, 0, width, content_y, fill=1, stroke=0)
        
        # Add subtle texture to content area
        p.setFillColor(HexColor('#f8f9fa'))
        for i in range(0, int(width), 40):
            for j in range(0, int(content_y), 40):
                if (i + j) % 80 == 0:
                    p.circle(i, j, 1, fill=1, stroke=0)
        
        y_position = content_y - 40
        
        # Certificate title with professional styling
        p.setFillColor(primary_blue)
        p.setFont("Helvetica-Bold", 28)
        p.drawCentredString(width / 2, y_position, "Certificate of Business Registration")
        y_position -= 20
        
        # Subtitle in red
        p.setFillColor(official_red)
        p.setFont("Helvetica-Oblique", 14)
        p.drawCentredString(width / 2, y_position, "Official Document of Commercial Authorization")
        y_position -= 30
        
        # Decorative line with gradient colors
        line_width = 200
        line_x = (width - line_width) / 2
        p.setStrokeColor(official_red)
        p.setLineWidth(3)
        p.line(line_x, y_position, line_x + line_width/3, y_position)
        p.setStrokeColor(gold_accent)
        p.line(line_x + line_width/3, y_position, line_x + 2*line_width/3, y_position)
        p.setStrokeColor(primary_blue)
        p.line(line_x + 2*line_width/3, y_position, line_x + line_width, y_position)
        y_position -= 50
        
        # Certificate body background
        body_margin = 80
        body_height = 300
        p.setFillColor(HexColor('#f8f9fa'))
        p.setStrokeColor(HexColor('#e2e8f0'))
        p.setLineWidth(1)
        p.rect(body_margin, y_position - body_height, width - 2*body_margin, body_height, fill=1, stroke=1)
        
        # Business information in a grid layout
        p.setFillColor(HexColor('#2d3748'))
        info_data = [
            ("Business Name", self.name),
            ("Registration Number", self.registration_number),
            ("Business Type", self.get_business_type_display()),
            ("KRA PIN", self.kra_pin),
            ("County", self.get_county_display()),
            ("Physical Address", self.physical_address),
            ("Date Established", str(self.date_established)),
            ("Date Approved", str(self.created_at.date())),
        ]
        
        # Create info boxes
        info_y = y_position - 40
        box_width = (width - 2*body_margin - 40) / 2
        box_height = 30
        
        for i, (label, value) in enumerate(info_data):
            # Determine position (left or right column)
            col = i % 2
            row = i // 2
            
            box_x = body_margin + 20 + col * (box_width + 20)
            box_y = info_y - row * (box_height + 15)
            
            # Draw professional info box with official styling
            p.setFillColor(HexColor('#ffffff'))
            p.setStrokeColor(HexColor('#e2e8f0'))
            p.setLineWidth(1)
            p.rect(box_x, box_y - box_height, box_width, box_height, fill=1, stroke=1)
            
            # Add official colored left border
            p.setFillColor(official_red)
            p.rect(box_x, box_y - box_height, 4, box_height, fill=1, stroke=0)
            
            # Add accent right border
            p.setFillColor(gold_accent)
            p.rect(box_x + box_width - 2, box_y - box_height, 2, box_height, fill=1, stroke=0)
            
            # Add subtle top border
            p.setFillColor(primary_blue)
            p.rect(box_x, box_y - 2, box_width, 2, fill=1, stroke=0)
            
            # Add label with official styling
            p.setFillColor(primary_blue)
            p.setFont("Helvetica-Bold", 9)
            p.drawString(box_x + 12, box_y - 12, label.upper())
            
            # Add value
            p.setFillColor(text_gray)
            p.setFont("Helvetica", 11)
            p.drawString(box_x + 12, box_y - 24, str(value))
        
        # Official statement
        statement_y = y_position - body_height + 80
        statement_text = ("This certificate is issued in accordance with the laws of the Republic of Kenya "
                        "and authorizes the above-named entity to conduct business operations within "
                        "the specified jurisdiction.")
        
        # Statement background
        p.setFillColor(HexColor('#e6f3ff'))
        p.setStrokeColor(HexColor('#bee3f8'))
        p.rect(body_margin + 20, statement_y - 30, width - 2*body_margin - 40, 40, fill=1, stroke=1)
        
        # Statement text
        p.setFillColor(secondary_blue)
        p.setFont("Helvetica-Oblique", 9)
        
        # Word wrap the statement
        words = statement_text.split()
        lines = []
        current_line = []
        line_width = width - 2*body_margin - 80
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if p.stringWidth(test_line, "Helvetica-Oblique", 9) <= line_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        for i, line in enumerate(lines):
            p.drawCentredString(width / 2, statement_y - 15 - i * 12, line)
        
        # Signature section
        sig_y = statement_y - 80
        
        # Signature lines
        sig_width = 150
        left_sig_x = body_margin + 40
        right_sig_x = width - body_margin - sig_width - 40
        
        p.setStrokeColor(secondary_blue)
        p.setLineWidth(1)
        p.line(left_sig_x, sig_y, left_sig_x + sig_width, sig_y)
        p.line(right_sig_x, sig_y, right_sig_x + sig_width, sig_y)
        
        # Signature labels
        p.setFillColor(text_gray)
        p.setFont("Helvetica-Bold", 8)
        p.drawCentredString(left_sig_x + sig_width/2, sig_y - 15, "AUTHORIZED OFFICER")
        p.drawCentredString(right_sig_x + sig_width/2, sig_y - 15, "DATE OF ISSUE")
        
        # Official seal
        seal_x = width - 150
        seal_y = 100
        p.setStrokeColor(secondary_blue)
        p.setLineWidth(2)
        p.circle(seal_x, seal_y, 40, fill=0, stroke=1)
        
        p.setFillColor(secondary_blue)
        p.setFont("Helvetica-Bold", 8)
        p.drawCentredString(seal_x, seal_y + 5, "OFFICIAL")
        p.drawCentredString(seal_x, seal_y - 5, "SEAL")
        
        # Add subtle watermark
        p.setFillColor(HexColor("#d1d1d1"))
        p.setFont("Helvetica-Bold", 48)
        p.saveState()
        p.translate(width/2, height/2)
        p.rotate(45)
        p.drawCentredString(0, 0, "SPECIMEN")
        p.restoreState()
        
        p.showPage()
        p.save()
        
        # Save PDF to model
        filename = f"{self.registration_number.replace('/', '_')}_certificate.pdf"
        self.registration_certificate.save(filename, ContentFile(buffer.getvalue()), save=False)
        buffer.close()
        
        # Save the model instance to persist registration_certificate path
        self.save(update_fields=['registration_certificate'])

        return filename

    def __str__(self):
        return f"{self.name} ({self.get_business_type_display()}) - status: {self.status}"


class PartnershipDetail(models.Model):
    business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name='partnership_detail')
    partners_name = models.CharField(max_length=512, help_text="Comma-separated full names of partners", null=True, blank=True)
    partners_id_numbers = models.CharField(max_length=512, help_text="Comma-separated ID numbers of partners", null=True, blank=True)

class CompanyDetail(models.Model):
    business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name='company_detail')
    directors = models.CharField(max_length=512, help_text="Comma-separated full names of directors", null=True, blank=True)
    share_capital = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)