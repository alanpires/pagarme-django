# Generated by Django 4.0.3 on 2022-03-22 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentInfo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('payment_method', models.CharField(choices=[('debit', 'debit'), ('credit', 'credit')], max_length=6)),
                ('card_number', models.CharField(max_length=16)),
                ('cardholders_name', models.CharField(max_length=30)),
                ('card_expiring_date', models.DateField()),
                ('cvv', models.CharField(max_length=4)),
                ('is_active', models.BooleanField(default=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_info', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
