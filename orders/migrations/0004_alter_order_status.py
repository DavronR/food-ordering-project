# Generated by Django 3.2.25 on 2024-09-02 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20240901_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Received', 'Received'), ('Picked Up', 'Picked Up'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Received', max_length=20),
        ),
    ]
