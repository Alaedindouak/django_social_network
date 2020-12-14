from django import forms
from .models import Post, Comment

class PostModelForm(forms.ModelForm):
	content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':1, 'placeholder': 'add a post...'}))

	class Meta:
		model = Post
		fields = ('content', 'image')


class CommentModelForm(forms.ModelForm):
	body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'add a comment...', 'id':'post_comment_id'}))

	class Meta:
		model = Comment
		fields = ('body',)
