from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tag, Story, Page, Dialogue, Image, RepeatPhrase, Score, UserProfile, UserAnswer


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


class SelectDefaultImageForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['default_profile_image']


class CategoriaForm(forms.ModelForm):
	class Meta:
		model = Tag
		fields = '__all__'

		input_classes = 'form-control fs-6'

		widgets = {
			'name1': forms.TextInput(attrs={'class': input_classes}),
			'name2': forms.TextInput(attrs={'class': input_classes}),
		}

		labels = {
			'name1': 'Nombre en inglés',
			'name2': 'Nombre en español',
		}


class HistoriaForm(forms.ModelForm):
	class Meta:
		model = Story
		fields = '__all__'
		exclude = ['route', 'likes_number']

		input_classes = 'form-control fs-6'

		widgets = {
			'title1': forms.TextInput(attrs={'class': input_classes}),
			'title2': forms.TextInput(attrs={'class': input_classes}),
			'cover': forms.FileInput(attrs={'class': input_classes}),
			'description1': forms.Textarea(attrs={'class': 'form-control fs-6 txta'}),
			'description2': forms.Textarea(attrs={'class': 'form-control fs-6 txta'}),
			'xp_required': forms.NumberInput(attrs={'class': input_classes}),
		}

		labels = {
			'title1': 'Título en inglés',
			'title2': 'Título en español',
			'cover': 'Portada',
			'description1': 'Descripción en inglés',
			'description2': 'Descripción en español',
			'xp_required': 'XP necesaria para desbloquear esta historia',
		}

	tags = forms.ModelMultipleChoiceField(
		queryset=Tag.objects.all(),
		widget=forms.CheckboxSelectMultiple(),
		required=False,
		label = 'Categorías',
	)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# Sort tags by name
		self.fields['tags'].widget.choices = sorted(
			self.fields['tags'].widget.choices,
			key=lambda choice: choice[1].lower()
    )


class ScoreForm(forms.ModelForm):
	class Meta:
		model = Score
		fields = '__all__'
		exclude = ['user_profile', 'story', 'date', 'score', 'score_limit', 
	     'score_percentage','writing_percentage', 'comprehension_percentage', 'speaking_percentage']


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
		exclude = ['page', 'content1', 'content2', 'element_number', 'show_text']


class UserAnswerForm(forms.ModelForm):
	class Meta:
		model = UserAnswer
		exclude = '__all__'
