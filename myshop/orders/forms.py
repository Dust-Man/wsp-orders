from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email','tel','business','notes']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full border-2 border-principal placeholder:text-zinc-400 p-2 rounded-lg focus:border-3 text-lg focus:shadow-sm focus:outline-0',
                'placeholder': 'Nombre(s)',
                'required': 'required'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full border-2 border-principal placeholder:text-zinc-400 p-2 rounded-lg focus:border-3 text-lg focus:shadow-sm focus:outline-0',
                'placeholder': 'Apellidos'
            }),
            'tel': forms.TextInput(attrs={
                'class': 'w-full border-2 border-principal placeholder:text-zinc-400 p-2 rounded-lg focus:border-3 text-lg focus:shadow-sm focus:outline-0',
                'placeholder': 'Teléfono ej: +525512345686'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border-2 border-principal placeholder:text-zinc-400 p-2 rounded-lg focus:border-3 text-lg focus:shadow-sm focus:outline-0',
                'placeholder': 'Correo ej: ejemplo@ejemplo.com'
            }),
            'business': forms.TextInput(attrs={
                'class': 'w-full border-2 border-principal placeholder:text-zinc-400 p-2 rounded-lg focus:border-3 text-lg focus:shadow-sm focus:outline-0',
                'placeholder': 'Negocio'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full border-2 border-principal placeholder:text-zinc-400 p-2 rounded-lg focus:border-3 text-lg focus:shadow-sm focus:outline-0 h-25',
                'placeholder': 'Dirección'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full border-2 border-principal placeholder:text-zinc-400 p-2 rounded-lg focus:border-3 text-lg focus:shadow-sm focus:outline-0 h-40',
                'placeholder': 'Mensaje (Opcional). Escribe cualquier detalle adicional de tu pedido'
            }),
           
        }

    # Eliminar los labels en la plantilla
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = None
