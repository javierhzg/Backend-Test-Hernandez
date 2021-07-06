from django.db import models
import uuid


# Create your models here.
class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()


class Options(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu = models.ForeignKey(Menu, on_delete=models.DO_NOTHING)
    option = models.CharField(max_length=500)


class Selections(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    option = models.ForeignKey(Options, on_delete=models.DO_NOTHING)
    notes = models.CharField(max_length=500)
