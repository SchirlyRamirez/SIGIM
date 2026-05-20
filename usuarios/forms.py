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
    password1 = forms.CharField(
        label='Contrasena',
        widget=forms.PasswordInput(attrs={'placeholder': 'Minimo 8 caracteres'}),
    )
    password2 = forms.CharField(
        label='Confirmar contrasena',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repite la contrasena'}),
    )
    rol = forms.ChoiceField(choices=ROLES, label='Rol')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electronico',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Sin espacios ni caracteres especiales'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if len(username) < 4:
            raise forms.ValidationError('El usuario debe tener al menos 4 caracteres.')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya esta en uso.')
        return username

    def clean_first_name(self):
        nombre = self.cleaned_data.get('first_name', '').strip()
        if not nombre:
            raise forms.ValidationError('El nombre es obligatorio.')
        return nombre

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo ya esta registrado.')
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1', '')
        if len(password) < 8:
            raise forms.ValidationError('La contrasena debe tener al menos 8 caracteres.')
        if password.isdigit():
            raise forms.ValidationError('La contrasena no puede ser solo numeros.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Las contrasenas no coinciden.')
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
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electronico',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if len(username) < 4:
            raise forms.ValidationError('El usuario debe tener al menos 4 caracteres.')
        qs = User.objects.filter(username=username)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Este nombre de usuario ya esta en uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if email:
            qs = User.objects.filter(email=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Este correo ya esta registrado.')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('first_name', css_class='col-md-6'), Column('last_name', css_class='col-md-6')),
            Row(Column('username', css_class='col-md-6'), Column('email', css_class='col-md-6')),
            'rol',
            Submit('submit', 'Guardar cambios', css_class='btn btn-primary mt-2'),
        )