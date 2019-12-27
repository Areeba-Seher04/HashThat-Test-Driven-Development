from django import forms

class HashForm(forms.Form):
	text = forms.CharField(label='Enter Hash here:',widget=forms.Textarea)