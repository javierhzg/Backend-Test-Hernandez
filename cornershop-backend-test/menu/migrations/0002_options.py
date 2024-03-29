# Generated by Django 3.0.8 on 2021-06-29 21:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('option', models.CharField(max_length=500)),
                ('menu_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='menu.Menu')),
            ],
        ),
    ]
