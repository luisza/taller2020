from django import forms


class MiContacto(forms.Form):
    nombre = forms.CharField( )
    email = forms.EmailField( )
    mensaje = forms.CharField(widget=forms.Textarea)

    def clean_nombre(self):
        letra = self.cleaned_data['nombre'][0]
        if letra.lower() != "a":
            raise forms.ValidationError("El nombre no inicia con A")
        return self.cleaned_data['nombre']

    def clean(self):
        super(MiContacto, self).clean()
        if 'nombre' in self.cleaned_data and 'email' in self.cleaned_data:
            nombre = self.cleaned_data['nombre'].split(' ')[0]
            email = self.cleaned_data['email'].split("@")[0]

            if nombre.lower() != email.lower():
                raise forms.ValidationError("No el correo no es el primer nombre")



class CSVForm(forms.Form):
    file = forms.FileField()