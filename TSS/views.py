from django.shortcuts import render
from  gestionPedidos.models import Pedido, Empleado
from django.db.models import Sum

def holaMund(request):

   return render(request, "holamundo.html")




def asignacion_pedidos(request):
  
  """ if request.method=="POST":
    
    Cantidad= request.POST.get('cantidad', '')
    Hora = request.POST.get('hora', '')
    Dia = request.POST.get('dia', '')
    Prioridad = request.POST.get('prioridad', '') """
  
  Cantidad= 10
  Hora = 10
  Dia = "MARTES"
  Prioridad = 1

  #Divide los pedidos
  if Cantidad < 30:
      pedido = Pedido(cantidad=Cantidad, prioridad = Prioridad, hora = Hora, dia = Dia )
      pedido.save()
  else:
      dividirPedido(Prioridad, Cantidad, Hora, Dia)
  

  #Segun el dia y prioridad se asigna a los empleados
  if Dia == "VIERNES":
    if (Hora >= 18 and Hora <= 21):
      lista = Pedido.objects.filter(empleado_asignado__isnull=True, prioridad__lte = 2).order_by('prioridad')
      print(lista)
      asignarEmpleadoViernes(lista, Hora, Dia)
    
  if Dia == "SABADO" and (Prioridad == 1 or Prioridad == 2):
    if (Hora >= 8  and Hora <= 12):
      lista = Pedido.objects.filter(empleado_asignado__isnull=True, prioridad__lte = 2).order_by('prioridad')
      print(lista)
      asignarEmpleadoFinSemana(lista, Hora, 3)
    
  if Dia == "DOMINGO" and Prioridad == 1:
    if (Hora >= 8 and Hora <= 12):
      lista = Pedido.objects.filter(empleado_asignado__isnull=True, prioridad = 1).order_by('prioridad')
      asignarEmpleadoFinSemana(lista, Hora, Dia, 2)

  if Dia == "LUNES" or Dia == "MARTES" or Dia == "MIERCOLES" or Dia == "JUEVES" or Dia == "VIERNES":
    if (Hora >= 8 and Hora < 18 and Hora != 13):
      lista = Pedido.objects.filter(empleado_asignado__isnull=True).order_by('prioridad')
      asignarEmpleado(lista, Hora, Dia)


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


def asignarEmpleado(lista, Hora, Dia):
  
  #Numero de empleados, segun la hora
  cantEmp = 8
  if Hora == 17: cantEmp = 15
  
  #Libera al empleado de los pedidos que esta realizando
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

        #Controlar que un empleado no trabaje mas de 30 pedidos en una hora
        sumPedidoTrabaja = Pedido.objects.filter(empleado_asignado=empleado.id, horaTrabajada = Hora, diaTrabajado = Dia).aggregate(Sum('cantidad'))
        cantPedido = sumPedidoTrabaja["cantidad__sum"]
        if cantPedido == None: cantPedido = 0
        totalCantPedidoTrabaja = cantPedido + pedido.cantidad

        if(empleado.trabajando < 30 and sumaAux <= 30 and totalCantPedidoTrabaja <= 30):
          """ cantPedidosAsignados = Pedido.objects.filter(empleado_asignado=empleado.id, hora = pedido.hora, dia=pedido.dia).aggregate(Sum('cantidad'))

          aux2 = cantPedidosAsignados["cantidad__sum"]

          if aux2 == None:  aux2 = 0

          aux = aux2 + pedido.cantidad """
          
          #if (aux2 <= 30 and aux <=30):
          pedidoGuardar = Pedido.objects.get(id = pedido.id)
          pedidoGuardar.empleado_asignado_id = empleado.id
          pedidoGuardar.horaTrabajada = Hora
          pedidoGuardar.diaTrabajado = Dia
          pedidoGuardar.pagoxHora = 12.5
          pedidoGuardar.save()

          empleadoGuardar = Empleado.objects.get(id = empleado.id)
          empleadoGuardar.trabajando = empleadoGuardar.trabajando + pedido.cantidad
          empleadoGuardar.save()
          break
  

def asignarEmpleadoFinSemana(lista, Hora,Dia, emp):
  
  #Numero de empleados, segun la hora
  cantEmp = emp
  if Hora == 12: cantEmp = emp+1
  
  #Libera al empleado de los pedidos que esta realizando
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

        #Controlar que un empleado no trabaje mas de 30 pedidos en una hora
        sumPedidoTrabaja = Pedido.objects.filter(empleado_asignado=empleado.id, horaTrabajada = Hora, diaTrabajado = Dia).aggregate(Sum('cantidad'))
        cantPedido = sumPedidoTrabaja["cantidad__sum"]
        if cantPedido == None: cantPedido = 0
        totalCantPedidoTrabaja = cantPedido + pedido.cantidad

        if(empleado.trabajando < 30 and sumaAux <= 30 and totalCantPedidoTrabaja <= 30):

          pedidoGuardar = Pedido.objects.get(id = pedido.id)
          pedidoGuardar.empleado_asignado_id = empleado.id
          pedidoGuardar.horaTrabajada = Hora
          pedidoGuardar.diaTrabajado = Dia
          pedidoGuardar.pagoxHora = 50
          pedidoGuardar.save()

          empleadoGuardar = Empleado.objects.get(id = empleado.id)
          empleadoGuardar.trabajando = empleadoGuardar.trabajando + pedido.cantidad
          empleadoGuardar.save()
          break

def asignarEmpleadoViernes(lista, Hora, Dia):
  
  #Libera al empleado de los pedidos que esta realizando
  empleadosLista = Empleado.objects.all()
  empleados = empleadosLista[:4]
  for empleado in empleados:
    empleadoGuardar = Empleado.objects.get(id = empleado.id)
    empleadoGuardar.trabajando = 0
    empleadoGuardar.save()

  for pedido in lista:
    empleadosLista = Empleado.objects.all()
    empleados = empleadosLista[:4]

    for empleado in empleados:
        sumaAux = empleado.trabajando + pedido.cantidad

        #Controlar que un empleado no trabaje mas de 30 pedidos en una hora
        sumPedidoTrabaja = Pedido.objects.filter(empleado_asignado=empleado.id, horaTrabajada = Hora, diaTrabajado = Dia).aggregate(Sum('cantidad'))
        cantPedido = sumPedidoTrabaja["cantidad__sum"]
        if cantPedido == None: cantPedido = 0
        totalCantPedidoTrabaja = cantPedido + pedido.cantidad

        if(empleado.trabajando < 30 and sumaAux <= 30 and totalCantPedidoTrabaja <= 30):

          pedidoGuardar = Pedido.objects.get(id = pedido.id)
          pedidoGuardar.empleado_asignado_id = empleado.id
          pedidoGuardar.horaTrabajada = Hora
          pedidoGuardar.diaTrabajado = Dia
          pedidoGuardar.pagoxHora = 37.5
          pedidoGuardar.save()

          empleadoGuardar = Empleado.objects.get(id = empleado.id)
          empleadoGuardar.trabajando = empleadoGuardar.trabajando + pedido.cantidad
          empleadoGuardar.save()
          break


def pagarEmpleado(request):
  
  empleados = Empleado.objects.all()
  semana = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO']

  for empleado in empleados:
    for hoy in semana:
      for i in range(24):
        pedido = Pedido.objects.filter(empleado_asignado = empleado.id).filter(diaTrabajado = hoy).filter(horaTrabajada = i )
        
        if pedido.count() >= 1:
          empleado = Empleado.objects.get(id = empleado.id)
          empleado.pago = empleado.pago + pedido.first().pagoxHora
          empleado.save()

def pedidoxEmpleado(request):
  empleados = Empleado.objects.all()
  contexto = {}

  for empleado in empleados:
    totalCantidad = Pedido.objects.filter(empleado_asignado = empleado.id).aggregate(Sum('cantidad'))
    sumCantidad = totalCantidad["cantidad__sum"]
    contexto[empleado.nombre] = sumCantidad
  
  return render(request, "nombrePlanilla.html", contexto)

def pedidoxDia(request):
  
  lunes = Pedido.objects.filter(dia = "LUNES").aggregate(Sum('cantidad'))
  sumLunes = lunes["cantidad__sum"]
  if sumLunes == None: sumLunes = 0
  martes = Pedido.objects.filter(dia = "MARTES").aggregate(Sum('cantidad'))
  sumMartes = martes["cantidad__sum"]
  if sumMartes == None: sumMartes = 0
  miercoles = Pedido.objects.filter(dia = "MIERCOLES").aggregate(Sum('cantidad'))
  sumMiercoles = miercoles["cantidad__sum"]
  if sumMiercoles == None: sumMiercoles = 0
  jueves = Pedido.objects.filter(dia = "JUEVES").aggregate(Sum('cantidad'))
  sumJueves = jueves["cantidad__sum"]
  if sumJueves == None: sumJueves = 0
  viernes = Pedido.objects.filter(dia = "VIERNES").aggregate(Sum('cantidad'))
  sumViernes = viernes["cantidad__sum"]
  if sumViernes == None: sumViernes = 0
  sabado = Pedido.objects.filter(dia = "SABADO").aggregate(Sum('cantidad'))
  sumSabado = sabado["cantidad__sum"]
  if sumSabado == None: sumSabado = 0
  domingo = Pedido.objects.filter(dia = "DOMINGO").aggregate(Sum('cantidad'))
  sumDomingo = domingo["cantidad__sum"]
  if sumDomingo == None: sumDomingo = 0
  
  contexto = {
    'lunes' : sumLunes,
    'martes' : sumMartes,
    'miercoles' : sumMiercoles,
    'jueves' : sumJueves,
    'viernes' : sumViernes,
    'sabado' : sumSabado,
    'domingo' : sumDomingo
  }

  return render(request, "plantilla.html", contexto)

def pedidoxHora(request):
  contexto = {}

  for i in range(24):
    sumHora = Pedido.objects.filter(hora = i).aggregate(Sum('cantidad'))
    cantHora = sumHora["cantidad__sum"]
    contexto[i] = cantHora

  return render(request, "plantilla.html", contexto)

def gananciaxEmp(request):
  empleados = Empleado.objects.all()

  contexto = {}
  
  for empleado in empleados:
    contexto[empleado.nombre] = empleado.pago 

  return render(request, "lantilla.html", contexto)

def devolverEmpleados(request):
  empleados = Empleado.objects.all()
  return render(request, "plantilla.html", empleados)

def devolverPedidos(request):
  pedidos = Pedido.objects.all()
  return render(request, "plantilla.html", pedidos)

