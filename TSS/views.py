from django.shortcuts import render
from  gestionPedidos.models import Pedido, Empleado
from django.db.models import Sum

def holaMund(request):

   return render(request, "holamundo.html")




def asignacion_pedidos(request):
  
  lunes_pedidos = ["10","20","30","40","50","60","70","80","90","100","110","120","130","140","150","160","170","180","190","200","210","220","230","240"]
  hora = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
  lista_empleados = ["Diego","Felix","Ramiro","Ivan","Chiri"]
  cant_pedido_x_trabajador = 30
  cantidad_sobrante_dia_x = 0
  
  Cantidad= 200
  Hora = 15
  Dia = "LUNES"
  Prioridad = 1

    
  #cantidad = models.IntegerField(max_length=5, default=0)
  #destino = models.CharField(max_length = 30)
  #hora = models.CharField(max_length = 30)
  #dia = models.CharField(max_length = 30)
  #empleado_asignado = models.ForeignKey(Empleado,models.SET_NULL,blank=True, null=True)
  
  
  """ if Cantidad < 30:
     pedido = Pedido(cantidad=Cantidad, prioridad = Prioridad, hora = Hora, dia = Dia )
     pedido.save()
  else:
    dividirPedido(Prioridad, Cantidad, Hora, Dia) """
  

  if Dia == "VIERNES":
    if (Hora >= 7 and Hora <= 9):
      lista = Pedido.objects.filter(empleado_asignado__isnull=True, prioridad__lte = 2).order_by('prioridad')
      asignarEmpleadoViernes(lista)
    
  if Dia == "SABADO" and (Prioridad == 1 or Prioridad == 2):
    if (Hora >= 8  and Hora <= 12):
      lista = Pedido.objects.filter(empleado_asignado__isnull=True, prioridad__lte = 2).order_by('prioridad')
      asignarEmpleadoFinSemana(lista, Hora)
    
  if Dia == "DOMINGO" and Prioridad == 1:
    if (Hora >= 8 and Hora != 12):
      lista = Pedido.objects.filter(empleado_asignado__isnull=True, prioridad = 1).order_by('prioridad')
      asignarEmpleadoFinSemana(lista, Hora)
  else:
    if (Hora >= 8 and Hora < 18 and Hora != 13):
      lista = Pedido.objects.filter(empleado_asignado__isnull=True).order_by('prioridad')
      asignarEmpleado(lista, Hora)

  """
  for i in hora:
    diccionario_asignacion[str(i)] = lunes_pedidos[j] 
    j = j+1

  suma_pedido = 0
  j=0
   """


  """"
  for i in diccionario_asignacion:

    if (i > 7 and i < 19 ):
          for emp in lista_empleados:
            if cantidadAsignado(emp) < 31:
              #Asignar al empleado
              suma_pedido -= diccionario_asignacion[i]
              break
    else:
        #suma_pedido = suma_pedido + lunes_pedidos[j]

    j = j+1


  print(diccionario_asignacion)
    """
  
def cantidadAsignado(empleado):
  cantAsignado = 3
  #Consulta para saber asignaciones#
  return cantAsignado

def dividirPedido(prioridad, cantidad, hora, dia):
  cantidad2 = cantidad
  bandera = True
  while(bandera):
     cantidad_aux = cantidad2 - 30
     if cantidad_aux <= 30:
       pedido = Pedido(cantidad=cantidad_aux, prioridad = prioridad, hora = hora, dia = dia )
       pedido.save()
       bandera = False
     else:
       pedido = Pedido(cantidad=30, prioridad = prioridad, hora = hora, dia = dia )
       pedido.save()
       cantidad2 = cantidad_aux

  pedido = Pedido(cantidad=30, prioridad = prioridad, hora = hora, dia = dia )
  pedido.save()


def pedidos_acumulados():
  #pedidos = Pedido.objects.filter(hora__lte=7,hora__gte=18)
  pedidos = Pedido.objects.filter(empleado_asignado__isnull=True).order_by('prioridad')
  #pedidos = Pedido.objects.filter(hora = 1, hora=5)
  #pedidos = Pedido.objects.get()
  print("Imprimir pedidos")
  print (pedidos)

def asignarEmpleado(lista, Hora):
  
  cantEmp = 8
  if Hora == 17: cantEmp = 15
  
  empleadosLista = Empleado.objects.all()
  empleados = empleadosLista[:cantEmp]
  for empleado in empleados:
    empleadoGuardar = Empleado.objects.get(id = empleado.id)
    empleadoGuardar.trabajando = 0
    empleadoGuardar.save()

  for pedido in lista:
    empleadosLista = Empleado.objects.all()
    empleados = empleadosLista[:cantEmp]
    for empleado in empleados:
        sumaAux = empleado.trabajando + pedido.cantidad
        if(empleado.trabajando < 30 and sumaAux <= 30):
          cantPedidosAsignados = Pedido.objects.filter(empleado_asignado=empleado.id, hora = pedido.hora, dia=pedido.dia).aggregate(Sum('cantidad'))

          aux2 = cantPedidosAsignados["cantidad__sum"]

          if aux2 == None:  aux2 = 0

          aux = aux2 + pedido.cantidad

          if (aux2 <= 30 and aux <=30):
            pedidoGuardar = Pedido.objects.get(id = pedido.id)
            pedidoGuardar.empleado_asignado_id = empleado.id
            pedidoGuardar.save()

            empleadoGuardar = Empleado.objects.get(id = empleado.id)
            empleadoGuardar.trabajando = empleadoGuardar.trabajando + pedido.cantidad
            empleadoGuardar.save()
            break

def asignarEmpleadoFinSemana(lista, Hora):
  
  cantEmp = 4
  if Hora == 12: cantEmp = 5
  
  empleadosLista = Empleado.objects.all()
  empleados = empleadosLista[:cantEmp]
  for empleado in empleados:
    empleadoGuardar = Empleado.objects.get(id = empleado.id)
    empleadoGuardar.trabajando = 0
    empleadoGuardar.save()

  for pedido in lista:
    empleadosLista = Empleado.objects.all()
    empleados = empleadosLista[:cantEmp]
    for empleado in empleados:
        sumaAux = empleado.trabajando + pedido.cantidad
        if(empleado.trabajando < 30 and sumaAux <= 30):
          cantPedidosAsignados = Pedido.objects.filter(empleado_asignado=empleado.id, hora = pedido.hora, dia=pedido.dia).aggregate(Sum('cantidad'))

          aux2 = cantPedidosAsignados["cantidad__sum"]

          if aux2 == None:  aux2 = 0

          aux = aux2 + pedido.cantidad

          if (aux2 <= 30 and aux <=30):
            pedidoGuardar = Pedido.objects.get(id = pedido.id)
            pedidoGuardar.empleado_asignado_id = empleado.id
            pedidoGuardar.save()

            empleadoGuardar = Empleado.objects.get(id = empleado.id)
            empleadoGuardar.trabajando = empleadoGuardar.trabajando + pedido.cantidad
            empleadoGuardar.save()
            break

def asignarEmpleadoViernes(lista):
  cantEmp = 4
  
  empleadosLista = Empleado.objects.all()
  empleados = empleadosLista[:cantEmp]
  for empleado in empleados:
    empleadoGuardar = Empleado.objects.get(id = empleado.id)
    empleadoGuardar.trabajando = 0
    empleadoGuardar.save()

  for pedido in lista:
    empleadosLista = Empleado.objects.all()
    empleados = empleadosLista[:cantEmp]
    for empleado in empleados:
        sumaAux = empleado.trabajando + pedido.cantidad
        if(empleado.trabajando < 30 and sumaAux <= 30):
          cantPedidosAsignados = Pedido.objects.filter(empleado_asignado=empleado.id, hora = pedido.hora, dia=pedido.dia).aggregate(Sum('cantidad'))

          aux2 = cantPedidosAsignados["cantidad__sum"]

          if aux2 == None:  aux2 = 0

          aux = aux2 + pedido.cantidad

          if (aux2 <= 30 and aux <=30):
            pedidoGuardar = Pedido.objects.get(id = pedido.id)
            pedidoGuardar.empleado_asignado_id = empleado.id
            pedidoGuardar.save()

            empleadoGuardar = Empleado.objects.get(id = empleado.id)
            empleadoGuardar.trabajando = empleadoGuardar.trabajando + pedido.cantidad
            empleadoGuardar.save()
            break
  

