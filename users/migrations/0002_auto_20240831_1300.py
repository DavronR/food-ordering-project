from django.db import migrations
from django.contrib.auth.models import Group

def create_groups(apps, schema_editor):
    Group.objects.get_or_create(name='customer')
    Group.objects.get_or_create(name='restaurant_owner')
    Group.objects.get_or_create(name='delivery_personnel')

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
