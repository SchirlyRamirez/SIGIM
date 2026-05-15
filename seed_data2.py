import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sigim.settings')
django.setup()

from django.contrib.auth.models import User
from inventario.models import Proveedor, Producto

p1,_ = Proveedor.objects.get_or_create(nombre='Distribuidora Alimentaria del Eje', defaults={'contacto':'Carlos Perez','telefono':'3001234567','email':'c@dae.com','direccion':'Manizales'})
p2,_ = Proveedor.objects.get_or_create(nombre='Aseo y Hogar Ltda', defaults={'contacto':'Maria Gonzalez','telefono':'3107654321','email':'m@aseo.co','direccion':'Pereira'})
p3,_ = Proveedor.objects.get_or_create(nombre='Lacteos del Cafe SA', defaults={'contacto':'Andres Rios','telefono':'3204567890','email':'a@lacteos.com','direccion':'Calarca'})
p4,_ = Proveedor.objects.get_or_create(nombre='Distribuidora Nacional de Granos', defaults={'contacto':'Sofia Vargas','telefono':'3156789012','email':'s@dng.com','direccion':'Manizales'})
print('Proveedores OK')

productos = [
    ('ALI-001','Arroz Diana 1kg','Alimentos',3200,120,30,p4),
    ('ALI-002','Frijol Baltico 500g','Alimentos',4100,8,20,p4),
    ('ALI-003','Aceite Gourmet 1L','Alimentos',9800,45,15,p1),
    ('ALI-004','Azucar Riopaila 2kg','Alimentos',6500,0,25,p1),
    ('ALI-005','Sal Refisal 1kg','Alimentos',1200,200,40,p1),
    ('LAC-001','Leche Colanta 1L','Lacteos',2600,12,30,p3),
    ('LAC-002','Yogurt Alpina 200g','Lacteos',1800,35,15,p3),
    ('LAC-003','Queso Campesino 250g','Lacteos',5200,5,10,p3),
    ('ASE-001','Detergente Ariel 1kg','Aseo',8900,40,20,p2),
    ('ASE-002','Jabon Palmolive 3und','Aseo',4200,80,25,p2),
    ('ASE-003','Shampoo HyS 400ml','Aseo',15900,3,10,p2),
    ('BEB-001','Gaseosa Postobon 2L','Bebidas',4500,55,20,p1),
    ('BEB-002','Agua Cristal 600ml','Bebidas',1500,150,50,p1),
]

for cod,nom,cat,precio,disp,smin,prov in productos:
    Producto.objects.get_or_create(codigo_unico=cod, defaults=dict(nombre=nom,categoria=cat,precio=precio,cantidad_disponible=disp,stock_minimo=smin,unidad_medida='UND',proveedor=prov))
    print(f'OK: {nom}')

print('Listo!')