# Generated by Django 4.0.3 on 2022-03-22 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fees', '0001_initial'),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payable',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('paid', 'paid'), ('waiting_funds', 'waiting_funds')], max_length=13)),
                ('payment_date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=19)),
                ('fee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payables', to='fees.fee')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payables', to=settings.AUTH_USER_MODEL)),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payable', to='transactions.transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
