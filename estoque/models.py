from django.db import models
from django.utils import timezone
from datetime import timedelta


class Material(models.Model):
    CATEGORIA_CHOICES = [
        ('limpeza', 'Limpeza'),
        ('escritorio', 'Escritório'),
        ('penso', 'Penso'),
        ('impressos','Impressos'),
    ]

    UNIDADE_CHOICES = [
        ('un', 'Unidade'),
        ('cx', 'Caixa'),
        ('pct', 'Pacote'),
        ('l', 'Litro'),
        ('ml', 'Mililitro'),
        ('kg', 'Quilograma'),
        ('g', 'Grama'),
    ]

    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    unidade_medida = models.CharField(max_length=10, choices=UNIDADE_CHOICES, default='un')
    quantidade_atual = models.PositiveIntegerField(default=0)
    quantidade_minima = models.PositiveIntegerField(default=0)
    data_validade = models.DateField(null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Materiais"
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def estoque_baixo(self):
        return self.quantidade_atual <= self.quantidade_minima

    @property
    def vencido(self):
        return bool(self.data_validade and self.data_validade < timezone.now().date())

    @property
    def proximo_vencimento(self):
        if self.data_validade:
            limite = timezone.now().date() + timedelta(days=60)
            return timezone.now().date() <= self.data_validade <= limite
        return False
