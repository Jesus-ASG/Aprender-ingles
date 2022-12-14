from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tag, Story, Page, Dialogue, Image, RepeatPhrase


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


class HistoriaForm(forms.ModelForm):
	class Meta:
		model = Story
		fields = '__all__'
		exclude = ['route']

		widgets = {
			'title1': forms.TextInput(attrs={'class': 'form-control'}),
			'cover': forms.FileInput(attrs={'class': 'form-control'}),
			'description1': forms.TextInput(attrs={'class': 'form-control'}),
		}

		labels = {
			'title1': 'Título',
			'cover': 'Portada',
			'description1': 'Descripción',
		}

	tag = forms.ModelMultipleChoiceField(
		queryset=Tag.objects.all(),
		widget=forms.CheckboxSelectMultiple(),
		required=False,
		label = 'Categorías',
	)


class PageForm(forms.ModelForm):
	class Meta:
		model = Page
		fields = '__all__'
		exclude = ['story', 'subtitle1', 'subtitle2', 'page_type']


class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = '__all__'
		exclude = ['page', 'image', 'element_number']


class DialogueForm(forms.ModelForm):
	class Meta:
		model = Dialogue
		fields = '__all__'
		exclude = ['page', 'name', 'content1', 'content2',
		'color', 'element_number']
		

# Exercises
class RepeatPhraseForm(forms.ModelForm):
	class Meta:
		model = RepeatPhrase
		fields = '__all__'
		exclude = ['page', 'content1', 'content2', 'element_number']

