from .forms import RegisterForm, ProfileModelForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.decorators import login_required


def register(request):
	form = RegisterForm()
	if request.method == 'POST':
		form = RegisterForm(request.POST)

		if form.is_valid():
			form.save()
			# username = form.cleaned_data.get('username')
			# messages.success(request, f'{username} your account has been created successfully')
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

	return render(request, 'profiles/profile-page.html', context)
