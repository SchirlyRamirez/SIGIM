"""
Script de carga de datos iniciales para SIGIM.
Ejecutar con:  python manage.py shell < seed_data.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sigim.settings')
django.setup()

from django.contrib.auth.models import User
from inventario.models import Proveedor, Producto

# ─── Superusuario ─────────────────────────────────────────────────────────────
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@mercaldas.com', 'admin1234')
    print('✔ Superusuario creado: admin / admin1234')

# ─── Usuarios por rol ─────────────────────────────────────────────────────────
roles = [
    ('encargado', 'encargado@mercaldas.com', 'Encargado', 'Inventario', '1234'),
    ('cajero1',   'cajero@mercaldas.com',    'Cajero',    'Uno',        '1234'),
]
for uname, email, fname, lname, pwd in roles:
    if not User.objects.filter(username=uname).exists():
        u = User.objects.create_user(uname, email, pwd, first_name=fname, last_name=lname)
        print(f'✔ Usuario creado: {uname} / {pwd}')

# ─── Proveedores ──────────────────────────────────────────────────────────────
proveedores_data = [
    ('Distribuidora Alimentaria del Eje',  'Carlos Pérez',    '3001234567', 'cperez@dae.com',    'Carrera 23 #15-40, Manizales'),
    ('Aseo & Hogar Ltda.',                 'María González',  '3107654321', 'mgonzalez@aseo.co', 'Calle 50 #8-12, Pereira'),
    ('Lácteos del Café S.A.',              'Andrés Ríos',     '3204567890', 'arios@lacteos.com', 'Vía La Línea km 3, Calarcá'),
    ('Distribuidora Nacional de Granos',   'Sofía Vargas',    '3156789012', 'svargas@dng.com',   'Zona Industrial, Manizales'),
]
proveedores = {}
for nombre, contacto, tel, email, dir_ in proveedores_data:
    p, _ = Proveedor.objects.get_or_create(
        nombre=nombre,
        defaults=dict(contacto=contacto, telefono=tel, email=email, direccion=dir_)
    )
    proveedores[nombre] = p
print(f'✔ {len(proveedores)} proveedores cargados')

# ─── Productos ────────────────────────────────────────────────────────────────
dist_alim = proveedores['Distribuidora Alimentaria del Eje']
aseo      = proveedores['Aseo & Hogar Ltda.']
lacteos   = proveedores['Lácteos del Café S.A.']
granos    = proveedores['Distribuidora Nacional de Granos']

productos_data = [
    # (codigo, nombre, categoria, precio, disponible, stock_min, unidad, proveedor)
    ('ALI-001', 'Arroz Diana 1kg',          'Alimentos',  3200,  120, 30, 'UND', granos),
    ('ALI-002', 'Frijol Báltico 500g',      'Alimentos',  4100,   8,  20, 'UND', granos),
    ('ALI-003', 'Aceite Gourmet 1L',        'Alimentos',  9800,  45,  15, 'UND', dist_alim),
    ('ALI-004', 'Azúcar Riopaila 2kg',      'Alimentos',  6500,   0,  25, 'UND', dist_alim),
    ('ALI-005', 'Sal Refisal 1kg',          'Alimentos',  1200, 200,  40, 'UND', dist_alim),
    ('ALI-006', 'Pasta Doria 500g',         'Alimentos',  2800,  60,  20, 'UND', dist_alim),
    ('LAC-001', 'Leche Colanta 1L',         'Lácteos',   2600,  12,  30, 'UND', lacteos),
    ('LAC-002', 'Yogurt Alpina 200g',       'Lácteos',   1800,  35,  15, 'UND', lacteos),
    ('LAC-003', 'Queso Campesino 250g',     'Lácteos',   5200,   5,  10, 'UND', lacteos),
    ('ASE-001', 'Detergente Ariel 1kg',     'Aseo',      8900,  40,  20, 'UND', aseo),
    ('ASE-002', 'Jabón Palmolive 3und',     'Aseo',      4200,  80,  25, 'UND', aseo),
    ('ASE-003', 'Shampoo Head&Shoulders',   'Aseo',     15900,   3,  10, 'UND', aseo),
    ('ASE-004', 'Papel Higiénico Familia',  'Aseo',      5800,  90,  30, 'UND', aseo),
    ('BEB-001', 'Gaseosa Postobón 2L',      'Bebidas',   4500,  55,  20, 'UND', dist_alim),
    ('BEB-002', 'Agua Cristal 600ml',       'Bebidas',   1500, 150,  50, 'UND', dist_alim),
]

for codigo, nombre, cat, precio, disp, stock_min, unidad, prov in productos_data:
    Producto.objects.get_or_create(
        codigo_unico=codigo,
        defaults=dict(
            nombre=nombre, categoria=cat, precio=precio,
            cantidad_disponible=disp, stock_minimo=stock_min,
            unidad_medida=unidad, proveedor=prov
        )
    )
print(f'✔ {len(productos_data)} productos cargados')
print('\n✅ Datos iniciales cargados exitosamente.')
print('   Accede en: http://127.0.0.1:8000')
print('   Usuario admin: admin / admin1234')
print('   Encargado:     encargado / 1234')
print('   Cajero:        cajero1 / 1234')
