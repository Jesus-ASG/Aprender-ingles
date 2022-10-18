from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Categoria, Historia, Pagina


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class CategoriaForm(forms.ModelForm):
	class Meta:
		model = Categoria
		fields = '__all__'

class PaginaForm(forms.ModelForm):
	class Meta:
		model = Pagina
		fields = '__all__'
		exclude = ['texto','historia']
	
	


class HistoriaForm(forms.ModelForm):
	class Meta:
		model = Historia
		fields = '__all__'

		widgets = {
			'titulo': forms.TextInput(attrs={'class': 'form-control'}),
			'portada': forms.FileInput(attrs={'class': 'form-control'}),
			'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
		}

	id_categoria = forms.ModelMultipleChoiceField(
		queryset=Categoria.objects.all(),
		widget=forms.CheckboxSelectMultiple(attrs={'class': ''}),
		required=False,
		label = 'Id categoría',
	)

