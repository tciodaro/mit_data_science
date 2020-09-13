from django.db import models
from datetime import datetime

# Create your models here.

class coletatestetreino(models.Model):
    
    id = models.CharField(max_length=30, primary_key=True)    
    din_evento = models.DateTimeField(null=True)
    dsc_texto = models.TextField(null=True) 
    tip_supervisao  = models.CharField(max_length=10,null=True)    
   
    def __str__(self):
        return self.id

class coleta(models.Model):
    
    id = models.CharField(max_length=30, primary_key=True)    
    din_evento = models.DateTimeField(null=True)
    dsc_texto = models.TextField(null=True)    
   
    def __str__(self):
        return self.id

class treinoteste(models.Model):
    
    #id = models.AutoField(primary_key=True) 
    id = models.CharField(max_length=30, primary_key=True) 
    dsc_texto = models.TextField(null=True)     
    tip_legenda  = models.CharField(max_length=10,null=True)        
    tip_predicao = models.CharField(max_length=5,null=True)
    pct_predicao = models.CharField(max_length=5, null=True)
    din_calculo = models.DateTimeField(null=True)  

    def __str__(self):
        return self.id


class predicao(models.Model):
    
    id = models.CharField(max_length=30, primary_key=True) 
    dsc_texto = models.TextField(null=True)    
    tip_supervisao = models.CharField(max_length=5,null=True) 
    din_execucao = models.DateTimeField(null=True)  
    tip_predicao = models.CharField(max_length=5,null=True)
    pct_predicao = models.CharField(max_length=5, null=True)

    def __str__(self):
        return self.id


class estatistica(models.Model):
    
    id = models.AutoField(primary_key=True) 
    din_execucao = models.DateTimeField(null=True)       
    dsc_predicao = models.CharField(max_length=20,null=True)
    qtd_registro = models.IntegerField(null=True)
    tip_legenda =  models.CharField(max_length=20,null=True)
   
    def __str__(self):
        return self.id





class DadosColeta(models.Model):
    
    id = models.CharField(max_length=30, primary_key=True)    
    din_evento = models.DateTimeField(null=True)
    dsc_manutencao = models.TextField()
    tip_evento = models.CharField(max_length=5,null=True)
   
    def __str__(self):
        return self.id


class DadosRetreino(models.Model):
    
    id = models.AutoField(primary_key=True) 
    id_sin = models.CharField(max_length=30,null=True)    
    dsc_texto = models.TextField(null=True)   
    tip_supervisao = models.CharField(max_length=5,null=True)  
    din_execucao = models.DateTimeField(null=True)      
    tip_evento = models.CharField(max_length=5,null=True)        
    tip_predicao = models.CharField(max_length=5,null=True)
    pct_predicao = models.CharField(max_length=10, null=True)

   
    def __str__(self):
        return self.id

class DadosPredicao(models.Model):
    
   # id = models.AutoField(primary_key=True) 
    id_sin = models.CharField(max_length=30,primary_key=True)    
    dsc_texto = models.TextField(null=True)
    tip_supervisao = models.CharField(max_length=5,null=True)      
    din_execucao = models.DateTimeField(null=True)  
    tip_evento = models.CharField(max_length=5,null=True)           
    tip_predicao = models.CharField(max_length=5,null=True)
    pct_predicao = models.CharField(max_length=10, null=True)


class DadosEstatistica(models.Model):
    
    id = models.AutoField(primary_key=True) 
    din_execucao = models.DateTimeField(null=True)       
    dsc_predicao = models.CharField(max_length=20,null=True)
    qtd_registro = models.IntegerField()
   
    def __str__(self):
        return self.id
