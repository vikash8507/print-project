from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "name", "phone", "shop_name", "shop_address", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.name = self.cleaned_data['name']
		user.phone = self.cleaned_data['phone']
		user.shop_name = self.cleaned_data['shop_name']
		user.shop_address = self.cleaned_data['shop_address']
		if commit:
			user.save()
		return user