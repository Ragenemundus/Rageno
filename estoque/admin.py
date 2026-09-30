from django.contrib import admin
from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'quantidade_atual', 'quantidade_minima', 'data_validade')
    list_filter = ('categoria',)
    search_fields = ('nome',)