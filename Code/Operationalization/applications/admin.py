from django.contrib import admin
from .models import coleta


# Registro modelo DadoColeta fica disponível na página da administração
admin.site.register(coleta)
