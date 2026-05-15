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
            'precio': forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción opcional...'}),
            'cantidad': forms.NumberInput(attrs={'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proveedor'].required = False
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
