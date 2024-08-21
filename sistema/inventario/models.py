from django.db import models
from django.contrib.auth.models import AbstractUser

# MODELOS

#--------------------------------USUARIO------------------------------------------------
class Usuario(AbstractUser):
    # id
    username = models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=60)
    nivel = models.IntegerField(null=True) 

    @classmethod
    def numeroRegistrados(cls):
        return cls.objects.count()   

    @classmethod
    def numeroUsuarios(cls, tipo):
        if tipo == 'administrador':
            return cls.objects.filter(is_superuser=True).count()
        elif tipo == 'usuario':
            return cls.objects.filter(is_superuser=False).count()

class Opciones(models.Model):
    # id
    moneda = models.CharField(max_length=20, null=True)
    valor_iva = models.IntegerField(unique=True)   
    nombre_negocio = models.CharField(max_length=25, null=True)
    mensaje_factura = models.TextField(null=True)

#---------------------------------------------------------------------------------------

#-------------------------------PRODUCTO------------------------------------------------
class Producto(models.Model):
    # id
    decisiones = [('1', 'Unidad'), ('2', 'Kilo'), ('3', 'Litro'), ('4', 'Otros')]
    descripcion = models.CharField(max_length=40)
    precio = models.DecimalField(max_digits=9, decimal_places=2)
    disponible = models.IntegerField(null=True)
    categoria = models.CharField(max_length=20, choices=decisiones)
    tiene_iva = models.BooleanField(null=True)

    @classmethod
    def numeroRegistrados(cls):
        return cls.objects.count()
   
    @classmethod
    def productosRegistrados(cls):
        return cls.objects.all().order_by('descripcion')

    @classmethod
    def preciosProductos(cls):
        objetos = cls.objects.all().order_by('id')
        arreglo = []
        etiqueta = True
        extra = 1

        for indice, objeto in enumerate(objetos):
            arreglo.append([])
            if etiqueta:
                arreglo[indice].append(0)
                arreglo[indice].append("------")
                etiqueta = False
                arreglo.append([])

            arreglo[indice + extra].append(objeto.id)
            precio_producto = objeto.precio
            arreglo[indice + extra].append(f"{precio_producto:.2f}")

        return arreglo 

    @classmethod
    def productosDisponibles(cls):
        objetos = cls.objects.all().order_by('id')
        arreglo = []
        etiqueta = True
        extra = 1

        for indice, objeto in enumerate(objetos):
            arreglo.append([])
            if etiqueta:
                arreglo[indice].append(0)
                arreglo[indice].append("------")
                etiqueta = False
                arreglo.append([])

            arreglo[indice + extra].append(objeto.id)
            productos_disponibles = objeto.disponible
            arreglo[indice + extra].append(f"{productos_disponibles}")

        return arreglo 
#---------------------------------------------------------------------------------------

#------------------------------------------CLIENTE--------------------------------------
class Cliente(models.Model):
    # id
    cedula = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    direccion = models.CharField(max_length=200)
    nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=20)
    telefono2 = models.CharField(max_length=20, null=True)
    correo = models.CharField(max_length=100)
    correo2 = models.CharField(max_length=100, null=True)

    @classmethod
    def numeroRegistrados(cls):
        return cls.objects.count()

    @classmethod
    def cedulasRegistradas(cls):
        objetos = cls.objects.all().order_by('nombre')
        arreglo = []
        for objeto in objetos:
            arreglo.append([])
            arreglo[-1].append(objeto.cedula)
            nombre_cliente = f"{objeto.nombre} {objeto.apellido}"
            arreglo[-1].append(f"{nombre_cliente}. C.I: {cls.formatearCedula(objeto.cedula)}")
 
        return arreglo   

    @staticmethod
    def formatearCedula(cedula):
        # Elimina todos los caracteres que no sean números
        numero = ''.join(filter(str.isdigit, cedula))
        # Formatea el número y luego reconstruye la cédula con guiones
        if len(numero) > 8:
            return f"{numero[:-4]}-{numero[-4:]}"
        return numero
#-----------------------------------------------------------------------------------------        

#-------------------------------------FACTURA---------------------------------------------
class Factura(models.Model):
    # id
    cliente = models.ForeignKey(Cliente, to_field='cedula', on_delete=models.CASCADE)
    fecha = models.DateField()
    sub_monto = models.DecimalField(max_digits=20, decimal_places=2)
    monto_general = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.ForeignKey(Opciones, to_field='valor_iva', on_delete=models.CASCADE)

    @classmethod
    def numeroRegistrados(cls):
        return cls.objects.count()

    @classmethod
    def ingresoTotal(cls):
        facturas = cls.objects.all()
        total = 0

        for factura in facturas:
            total += factura.monto_general

        return total
#-----------------------------------------------------------------------------------------

#-------------------------------------DETALLES DE FACTURA---------------------------------
class DetalleFactura(models.Model):
    # id
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    sub_total = models.DecimalField(max_digits=20, decimal_places=2)
    total = models.DecimalField(max_digits=20, decimal_places=2)

    @classmethod
    def productosVendidos(cls):
        vendidos = cls.objects.all()
        totalVendidos = 0
        for producto in vendidos:
            totalVendidos += producto.cantidad

        return totalVendidos  

    @classmethod
    def ultimasVentas(cls):
        return cls.objects.all().order_by('-id')[:10]
#---------------------------------------------------------------------------------------

#------------------------------------------PROVEEDOR-----------------------------------
class Proveedor(models.Model):
    # id
    cedula = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    direccion = models.CharField(max_length=200)
    nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=20)
    telefono2 = models.CharField(max_length=20, null=True)
    correo = models.CharField(max_length=100)
    correo2 = models.CharField(max_length=100, null=True)

    @classmethod
    def cedulasRegistradas(cls):
        objetos = cls.objects.all().order_by('nombre')
        arreglo = []
        for objeto in objetos:
            arreglo.append([])
            arreglo[-1].append(objeto.cedula)
            nombre_proveedor = f"{objeto.nombre} {objeto.apellido}"
            arreglo[-1].append(f"{nombre_proveedor}. C.I: {cls.formatearCedula(objeto.cedula)}")
 
        return arreglo 

    @staticmethod
    def formatearCedula(cedula):
        numero = ''.join(filter(str.isdigit, cedula))
        if len(numero) > 8:
            return f"{numero[:-4]}-{numero[-4:]}"
        return numero
#---------------------------------------------------------------------------------------    

#----------------------------------------PEDIDO-----------------------------------------
class Pedido(models.Model):
    # id
    proveedor = models.ForeignKey(Proveedor, to_field='cedula', on_delete=models.CASCADE)    
    fecha = models.DateField()
    sub_monto = models.DecimalField(max_digits=20, decimal_places=2)
    monto_general = models.DecimalField(max_digits=20, decimal_places=2)
    iva = models.ForeignKey(Opciones, to_field='valor_iva', on_delete=models.CASCADE)
    presente = models.BooleanField(null=True)

    @classmethod
    def recibido(cls, pedido):
        return cls.objects.get(id=pedido).presente
#---------------------------------------------------------------------------------------    

#-------------------------------------DETALLES DE PEDIDO-------------------------------
class DetallePedido(models.Model):
    # id
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    sub_total = models.DecimalField(max_digits=20, decimal_places=2)
    total = models.DecimalField(max_digits=20, decimal_places=2)
#---------------------------------------------------------------------------------------

#------------------------------------NOTIFICACIONES------------------------------------
class Notificaciones(models.Model):
    # id
    autor = models.ForeignKey(Usuario, to_field='username', on_delete=models.CASCADE)
    mensaje = models.TextField()
#--------------------------------------------------------------------------------------- 
