# Generated by Django 4.0.2 on 2022-02-22 21:31

from django.db import migrations

def fee_default(apps, schema_editor):
    Fee = apps.get_model('fees', 'Fee')
    
    Fee.objects.create(credit_fee=0.05, debit_fee=0.03)

class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fee_default)
    ]