from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    sku = models.CharField(max_length=30, blank=True)
    categoria = models.CharField(max_length=80, default="General")
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_creacion"]
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def __str__(self):
        return self.nombre
