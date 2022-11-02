from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tag, Story, Page


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
		model = Tag
		fields = '__all__'

class PaginaForm(forms.ModelForm):
	class Meta:
		model = Page
		fields = '__all__'
		exclude = ['texto', 'story']
	
	


class HistoriaForm(forms.ModelForm):
	class Meta:
		model = Story
		fields = '__all__'
		exclude = ['route']

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'cover': forms.FileInput(attrs={'class': 'form-control'}),
			'description': forms.TextInput(attrs={'class': 'form-control'}),
		}

	id_categoria = forms.ModelMultipleChoiceField(
		queryset=Tag.objects.all(),
		widget=forms.CheckboxSelectMultiple(attrs={'class': ''}),
		required=False,
		label = 'Categorías',
	)


