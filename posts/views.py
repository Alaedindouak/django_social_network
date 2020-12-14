from django.views.generic import UpdateView, DeleteView
from .forms import PostModelForm, CommentModelForm
from django.shortcuts import render, redirect
from profiles.models import Profile
from .models import Post, Like
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def post_comment_create_and_list_view(request):
	posts = Post.objects.all()
	# profile = Profile.objects.filter().filter()
	profile = Profile.objects.get(user=request.user)
	post_form = PostModelForm()
	comment_form = CommentModelForm()
	if 'submit_post_form' in request.POST:
		post_form = PostModelForm(request.POST, request.FILES)
		if post_form.is_valid():
			post = Post()
			post.author = profile
			post.content = post_form.data.get('content')
			post_form_instance = post_form.save(commit=False)
			post_form_instance.author = profile
			post_form_instance.save()
			post_form = PostModelForm()

	if 'submit_comment_form' in request.POST:
		comment_form = CommentModelForm(request.POST)
		if comment_form.is_valid():
			comment_form_instance = comment_form.save(commit=False)
			comment_form_instance.user = profile
			comment_form_instance.post = Post.objects.get(id=request.POST.get('post_comment_id'))
			comment_form_instance.save()
			comment_form = CommentModelForm()

	context = {
		'posts': posts,
		'profile': profile,
		'post_form': post_form,
		'comment_form': comment_form,
	}

	return render(request, 'posts/main.html', context)


def like_unlike_post(request):
	user = request.user
	if request.method == 'POST':
		post_id = request.POST.get('post_id')
		post = Post.objects.get(id=post_id)
		profile = Profile.objects.get(user=user)
		# profile = Profile.objects.filter().first()

		if profile in post.liked.all():
			post.liked.remove(profile)
		else:
			post.liked.add(profile)

		like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

		if not created:
			if like.value == 'like':
				like.value = 'unlike'
			else:
				like.value = 'like'
		else:
			like.value = 'like'

			post.save()
			like.save()

	return  redirect('posts:main-post-view')


class PostDeleteView(DeleteView, LoginRequiredMixin):
	model = Post
	template_name = 'posts/delete.html'
	success_url = '/posts/'

	""" check if the author pf the post matches the self request user (logged in user)"""
	def get_object(self, *args, **kwargs):
		pk = self.kwargs.get('pk')
		post = Post.objects.get(pk=pk)

		if not post.author.user == self.request.user:
			messages.warning(self.request, 'you need to be the author if post in order to delete it')

		return post

class PostUpdateView(UpdateView, LoginRequiredMixin):
	form_class = PostModelForm
	model = Post
	template_name = 'posts/update.html'
	success_url = '/posts/'

	""" check if the author of the post matches the user that is logged in """
	def form_valid(self, form):
		profile = Profile.objects.get(user=self.request.user)
		if form.instance.author == profile:
			return super().form_valid(form)
		else:
			form.add_error(None, 'you need to be the author if post in order to update it')
			return super().form_valid(form)

