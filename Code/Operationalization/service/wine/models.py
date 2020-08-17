from django.db import models

# Create your models here.




class Supplier(models.Model):
    id=models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=100, blank=False)

    class Meta:
        unique_together = ('name',)
        ordering = ['created']



class Wine(models.Model):
    id=models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, blank=False)
    fixed_acidity = models.FloatField(blank=False)
    volatile_acidity = models.FloatField(blank=False)
    citric_acid = models.FloatField(blank=False)
    residual_sugar = models.FloatField(blank=False)
    chlorides = models.FloatField(blank=False)
    free_sulfur_dioxide = models.FloatField(blank=False)
    total_sulfur_dioxide = models.FloatField(blank=False)
    density = models.FloatField(blank=False)
    pH = models.FloatField(blank=False)
    sulphates = models.FloatField(blank=False)
    alcohol = models.FloatField(blank=False)
    estimated_score = models.FloatField(null=True)

    class Meta:
        unique_together = ('name',)
        ordering = ['created']


class SupplierMenu(models.Model):
    id=models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    wine = models.ForeignKey(Wine, to_field='id', on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, to_field='id', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('wine','supplier',)
        ordering = ['supplier','created']
