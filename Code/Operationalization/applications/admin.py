from django.contrib import admin
from .models import DadosColeta


# Registro modelo DadoColeta fica disponível na página da administração
admin.site.register(DadosColeta)
