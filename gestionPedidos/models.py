from django.db import models

# Create your models here.
class Empleado(models.Model):
    nombre = models.CharField(max_length = 30)
    apellido = models.CharField(max_length = 30)
    pago = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)

class Pedido(models.Model):
   destino = models.CharField(max_length = 30)
   hora = models.CharField(max_length = 30)
   dia = models.CharField(max_length = 30)
   entregado = models.BooleanField()
   empleado_asignado = models.ForeignKey(Empleado,models.SET_NULL,blank=True, null=True)



