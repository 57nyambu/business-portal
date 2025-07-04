# Generated by Django 5.2.3 on 2025-07-01 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_remove_companydetail_shareholders_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydetail',
            name='directors',
            field=models.CharField(blank=True, help_text='Comma-separated full names of directors', max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='companydetail',
            name='share_capital',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='partnershipdetail',
            name='partners_id_numbers',
            field=models.CharField(blank=True, help_text='Comma-separated ID numbers of partners', max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='partnershipdetail',
            name='partners_name',
            field=models.CharField(blank=True, help_text='Comma-separated full names of partners', max_length=512, null=True),
        ),
    ]
