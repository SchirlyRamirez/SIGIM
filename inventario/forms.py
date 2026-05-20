from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
from .models import Producto, MovimientoInventario, Proveedor


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'codigo_unico', 'nombre', 'categoria', 'precio',
            'cantidad_disponible', 'stock_minimo', 'unidad_medida', 'proveedor'
        ]
        widgets = {
            'codigo_unico': forms.TextInput(attrs={'placeholder': 'Ej: PROD-001'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del producto'}),
            'categoria': forms.TextInput(attrs={'placeholder': 'Ej: Alimentos, Aseo...'}),
            'precio': forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01', 'min': '0'}),
            'cantidad_disponible': forms.NumberInput(attrs={'min': '0'}),
            'stock_minimo': forms.NumberInput(attrs={'min': '1'}),
        }

    def clean_codigo_unico(self):
        codigo = self.cleaned_data.get('codigo_unico', '').strip().upper()
        if len(codigo) < 3:
            raise forms.ValidationError('El codigo debe tener al menos 3 caracteres.')
        qs = Producto.objects.filter(codigo_unico=codigo)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Ya existe un producto con este codigo.')
        return codigo

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres.')
        return nombre

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a cero.')
        return precio

    def clean_stock_minimo(self):
        stock = self.cleaned_data.get('stock_minimo')
        if stock is not None and stock < 1:
            raise forms.ValidationError('El stock minimo debe ser al menos 1.')
        return stock

    def clean(self):
        cleaned_data = super().clean()
        disponible = cleaned_data.get('cantidad_disponible')
        minimo = cleaned_data.get('stock_minimo')
        if disponible is not None and minimo is not None:
            if disponible < 0:
                self.add_error('cantidad_disponible', 'La cantidad no puede ser negativa.')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proveedor'].empty_label = 'Sin proveedor asignado'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('codigo_unico', css_class='col-md-4'),
                Column('nombre', css_class='col-md-8'),
            ),
            Row(
                Column('categoria', css_class='col-md-6'),
                Column('unidad_medida', css_class='col-md-3'),
                Column('precio', css_class='col-md-3'),
            ),
            Row(
                Column('cantidad_disponible', css_class='col-md-6'),
                Column('stock_minimo', css_class='col-md-6'),
            ),
            'proveedor',
            Submit('submit', 'Guardar', css_class='btn btn-primary mt-2'),
        )


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['producto', 'cantidad', 'proveedor', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripcion opcional...'}),
            'cantidad': forms.NumberInput(attrs={'min': 1}),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a cero.')
        return cantidad

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')
        # La validacion de stock suficiente se hace en la vista para salidas
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proveedor'].required = False
        self.fields['proveedor'].empty_label = 'Sin proveedor'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'producto',
            Row(
                Column('cantidad', css_class='col-md-6'),
                Column('proveedor', css_class='col-md-6'),
            ),
            'descripcion',
            Submit('submit', 'Registrar', css_class='btn btn-primary mt-2'),
        )


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'telefono', 'email', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre de la empresa'}),
            'contacto': forms.TextInput(attrs={'placeholder': 'Nombre del contacto'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ej: 3001234567'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@empresa.com'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Direccion completa'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres.')
        qs = Proveedor.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Ya existe un proveedor con este nombre.')
        return nombre

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()
        if telefono and not telefono.isdigit():
            raise forms.ValidationError('El telefono solo debe contener numeros.')
        if telefono and len(telefono) < 7:
            raise forms.ValidationError('El telefono debe tener al menos 7 digitos.')
        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if email:
            qs = Proveedor.objects.filter(email__iexact=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Ya existe un proveedor con este email.')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'nombre',
            Row(
                Column('contacto', css_class='col-md-6'),
                Column('telefono', css_class='col-md-6'),
            ),
            Row(
                Column('email', css_class='col-md-6'),
                Column('direccion', css_class='col-md-6'),
            ),
            Submit('submit', 'Guardar proveedor', css_class='btn btn-primary mt-2'),
        )