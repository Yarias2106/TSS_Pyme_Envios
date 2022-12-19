"""TSS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from TSS.views import inicio, asignacion_pedidos, pedidoxEmpleado, pagarEmpleado, pedidoxDia, pedidoxHora, gananciaxEmp, devolverEmpleados, devolverPedidosSinAsignar, devolverPedidosAsignados,rescatarDatos

urlpatterns = [
    path('admin/', admin.site.urls),
    path("inicio/", inicio),
    path("funcion/", asignacion_pedidos),
    path("pagarEmpleados/",pagarEmpleado),
    path("pedxEmp/", pedidoxEmpleado),
    path("pedxDia/", pedidoxDia),
    path("pedxHora/", pedidoxHora),
    path("gananciaxEmp/", gananciaxEmp),
    path("empleados/", devolverEmpleados),
    path("pedidosSinAsignar/", devolverPedidosSinAsignar),
    path("pedidosAsignados/", devolverPedidosAsignados),
    path("rescatar/", rescatarDatos)
]
