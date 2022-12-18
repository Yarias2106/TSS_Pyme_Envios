from django.db import models

# Create your models here.
class Empleado(models.Model):
    nombre = models.CharField(max_length = 30)
    apellido = models.CharField(max_length = 30)
    pago = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    trabajando = models.IntegerField(max_length=2, default=0)

class Pedido(models.Model):
   cantidad = models.IntegerField(max_length=4, default=0)
   prioridad = models.IntegerField(max_length = 1, default=0)
   hora = models.IntegerField(max_length = 2)
   dia = models.CharField(max_length = 30)
   empleado_asignado = models.ForeignKey(Empleado,models.SET_NULL,blank=True, null=True)



