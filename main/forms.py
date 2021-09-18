from django import forms

from main.models import Voter


class VoterForm(forms.ModelForm):
    birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    address1 = forms.CharField(
        label="English Address", widget=forms.Textarea(attrs={'rows': 3}))
    address2 = forms.CharField(
        label="Hindi Address", widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Voter
        fields = "__all__"
