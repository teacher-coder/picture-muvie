from django import forms


class LyricForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    artist = forms.CharField(max_length=100, required=True)
    lyrics = forms.CharField(widget=forms.Textarea(attrs={"rows": "15"}))
