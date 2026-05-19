from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

ROLES = [
    ('encargado', 'Encargado de Inventario'),
    ('cajero', 'Cajero'),
    ('admin', 'Administrador'),
]

class UsuarioCrearForm(forms.ModelForm):
    password1 = forms.CharField(label='Contrasena', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contrasena', widget=forms.PasswordInput)
    rol = forms.ChoiceField(choices=ROLES, label='Rol')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electronico',
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contrasenas no coinciden.')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('first_name', css_class='col-md-6'), Column('last_name', css_class='col-md-6')),
            Row(Column('username', css_class='col-md-6'), Column('email', css_class='col-md-6')),
            'rol',
            Row(Column('password1', css_class='col-md-6'), Column('password2', css_class='col-md-6')),
            Submit('submit', 'Crear usuario', css_class='btn btn-primary mt-2'),
        )


class UsuarioEditarForm(forms.ModelForm):
    rol = forms.ChoiceField(choices=ROLES, label='Rol')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electronico',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('first_name', css_class='col-md-6'), Column('last_name', css_class='col-md-6')),
            Row(Column('username', css_class='col-md-6'), Column('email', css_class='col-md-6')),
            'rol',
            Submit('submit', 'Guardar cambios', css_class='btn btn-primary mt-2'),
        )