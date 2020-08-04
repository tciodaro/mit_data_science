from django.db import models

# Create your models here.

class Countries(models.Model):
    id=models.AutoField(primary_key=True)
    code =  models.CharField(max_length=5,blank=False, null=False)


    class Meta:
        unique_together = ('code',)



class Measurements(models.Model):
    id=models.AutoField(primary_key=True)
    cases = models.FloatField(default=0, null=False)
    deaths = models.FloatField(default=0, null=False)
    recovered = models.FloatField(default=0, null=False)
    date  = models.DateField(null=False)

    country = models.ForeignKey(Countries, to_field='id', on_delete=models.CASCADE)


    class Meta:
        unique_together = ('date', 'country')



class ForecastModels(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(default='fbprophet', max_length=50, null=False)
    train_last_date = models.DateField(null=False)
    test_score = models.FloatField(null=False, default=0.0)
    country = models.ForeignKey(Countries, to_field='id',on_delete=models.CASCADE, related_name='countries')
    status = models.BooleanField(null=False, default=True)


    class Meta:
        unique_together = ('name', 'train_last_date', 'country')



class Forecasts(models.Model):
    id=models.AutoField(primary_key=True)
    estimated_cases = models.FloatField(default=0)
    date = models.DateField(null=False)
    error = models.FloatField(default=0)

    forecast_model = models.ForeignKey(ForecastModels, to_field='id', on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurements, null=True, to_field='id',on_delete=models.CASCADE)


    class Meta:
        unique_together = ('forecast_model', 'date', )
