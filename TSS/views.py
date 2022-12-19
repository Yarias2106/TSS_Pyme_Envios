from django.shortcuts import render, redirect
from  gestionPedidos.models import Pedido, Empleado
from django.db.models import Sum

def holaMund(request):

   return render(request, "paginainicio.html")




def asignacion_pedidos(request):
  
  lunes_pedidos = ["10","20","30","40","50","60","70","80","90","100","110","120","130","140","150","160","170","180","190","200","210","220","230","240"]
  hora = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
  lista_empleados = ["Diego","Felix","Ramiro","Ivan","Chiri"]
  cant_pedido_x_trabajador = 30
  cantidad_sobrante_dia_x = 0
  
  Cantidad= 50
  Hora = 12
  Dia = "DOMINGO"
  Prioridad = 1

    
  #cantidad = models.IntegerField(max_length=5, default=0)
  #destino = models.CharField(max_length = 30)
  #hora = models.CharField(max_length = 30)
  #dia = models.CharField(max_length = 30)
  #empleado_asignado = models.ForeignKey(Empleado,models.SET_NULL,blank=True, null=True)
  
  
  if Cantidad < 30:
      pedido = Pedido(cantidad=Cantidad, prioridad = Prioridad, hora = Hora, dia = Dia )
      pedido.save()
  else:
      dividirPedido(Prioridad, Cantidad, Hora, Dia)
  

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
  
""" def cantidadAsignado(empleado):
  cantAsignado = 3
  #Consulta para saber asignaciones#
  return cantAsignado """

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


""" def pedidos_acumulados():
  #pedidos = Pedido.objects.filter(hora__lte=7,hora__gte=18)
  pedidos = Pedido.objects.filter(empleado_asignado__isnull=True).order_by('prioridad')
  #pedidos = Pedido.objects.filter(hora = 1, hora=5)
  #pedidos = Pedido.objects.get()
  print("Imprimir pedidos")
  print (pedidos) """

def asignarEmpleado(lista, Hora, Dia):
  
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
            pedidoGuardar.horaTrabajada = Hora
            pedidoGuardar.diaTrabajado = Dia
            pedidoGuardar.pagoxHora = 12.5
            pedidoGuardar.save()

            empleadoGuardar = Empleado.objects.get(id = empleado.id)
            empleadoGuardar.trabajando = empleadoGuardar.trabajando + pedido.cantidad
            empleadoGuardar.save()
            break
  

def asignarEmpleadoFinSemana(lista, Hora,Dia, emp):
  
  cantEmp = emp
  if Hora == 12: cantEmp = emp+1
  
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
  
  empleadosLista = Empleado.objects.all()
  empleados = empleadosLista[:4]
  for empleado in empleados:
    empleadoGuardar = Empleado.objects.get(id = empleado.id)
    empleadoGuardar.trabajando = 0
    empleadoGuardar.save()

  for pedido in lista:
    empleadosLista = Empleado.objects.all()
    empleados = empleadosLista[:4]
    print(empleados)
    for empleado in empleados:
        print(empleado.trabajando)
        sumaAux = empleado.trabajando + pedido.cantidad
        if(empleado.trabajando < 30 and sumaAux <= 30):

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


def pagarEmpleado(idEmpleado):
  

  sumCantPagado = Pedido.objects.filter(empleado_asignado = idEmpleado, ).aaggregate(Sum('pagoxHora'))
  cantPagado = sumCantPagado["cantidad__sum"]

  empleado = Empleado.objects.get(idEmpleado)
  empleado.pago = cantPagado
  empleado.save()

def pedidoxEmpleado(request):
  empleados = Empleado.objects.all()
  contexto = {}

  for empleado in empleados:
    totalCantidad = Pedido.objects.filter(empleado_asignado = empleado.id).aggregate(Sum('cantidad'))
    sumCantidad = totalCantidad["cantidad__sum"]
    contexto[empleado.nombre] = sumCantidad
  
  return render(request, "pedidoxEmpleado.html", contexto)

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

  return render(request, "pedxdia.html", contexto)

def pedidoxHora(request):
  contexto = {}
  lista =["cero","uno","dos","tres","cuatro","cinco","seis","siete","ocho","nueve","diez","once","doce"
      ,"trece","catorce","quince","unoseis","unosiete","unoocho","unonueve","doscero","dosuno","dosdos","dostres"]
  cont = 0
  for i in lista:
    sumHora = Pedido.objects.filter(hora = cont).aggregate(Sum('cantidad'))
    cantHora = sumHora["cantidad__sum"]
    if cantHora == None: cantHora = 0
    contexto[i] = cantHora
    cont = cont + 1

  print(contexto)  
  return render(request, "pedidoxHora.html", contexto)

def gananciaxEmp(request):
  empleados = Empleado.objects.all()

  contexto = {}
  
  for empleado in empleados:
    contexto[empleado.nombre] = empleado.pago 

  return render(request, "gananciaxEmp.html", contexto)

def rescatarDatos(request):
  cant = request.POST.get('cantidad')
  hora = request.POST.get('hora')
  prioridad = request.POST.get('ciudades')
  dia = request.POST.get('dia')

  print(cant)
  print(hora)
  print(prioridad)
  print(dia)

  return redirect("/holamundo/")




