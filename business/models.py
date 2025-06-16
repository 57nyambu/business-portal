from django.db import models
from accounts.models import User

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
    ('ltd', 'Limited Company'),
    ('cooperative', 'Cooperative Society'),
    ('ngo', 'Non-Governmental Organization'),
    ('other', 'Other')
]

class Business(models.Model):
    # Required Fields
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
    registration_certificate = models.FileField(upload_to='certificates/', blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_business_type_display()})"