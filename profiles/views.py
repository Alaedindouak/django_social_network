from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView
from .forms import RegisterForm, ProfileModelForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile


def register(request):
	form = RegisterForm()
	if request.method == 'POST':
		form = RegisterForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('login-view')
		else:
			form = RegisterForm()

	return render(request, 'profiles/register.html', {'form': form})

@login_required
def profile_view(request):
	profile = Profile.objects.get(user=request.user)
	# profile = Profile.objects.filter().first()
	form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)

	if request.method == 'POST':
		if form.is_valid():
			form.save()

	context = {
		'profile': profile,
		'form': form,
	}

	return render(request, 'profiles/profile.html', context)

class UsersListView(ListView):
	model = Profile
	template_name = 'profiles/users.html'
	context_object_name = 'users'

	def get_queryset(self):
		return Profile.objects.all().exclude(user=self.request.user)

class UserProfileDetailView(DeleteView):
	model = Profile
	template_name = 'profiles/detail.html'

	""" get profile with pk """
	def get_object(self, **kwargs):
		pk = self.kwargs.get('pk')
		view_profile = Profile.objects.get(pk=pk)
		return view_profile

	""" passing some data to template """
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		view_profile = self.get_object() # get user
		my_profile = Profile.objects.get(user=self.request.user) # my profile

		if view_profile.user in my_profile.following.all():
			follow = True
		else:
			follow = False

		context['follow'] = follow
		return context

@login_required
def follow_unfollow_profile(request):
	if request.method == "POST":
		my_profile = Profile.objects.get(user=request.user)
		pk = request.POST.get('profile_pk')
		obj_user = Profile.objects.get(pk=pk)

		if obj_user.user in my_profile.following.all():
			my_profile.following.remove(obj_user.user)
		else:
			my_profile.following.add(obj_user.user)
			return redirect(request.META.get('HTTP_REFERER'))
	return redirect('profiles:users-view')
