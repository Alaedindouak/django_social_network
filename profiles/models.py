from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from .utils import get_random_code
from django.db import models


class Profile(models.Model):
	first_name = models.CharField(max_length=200, blank=True)
	last_name = models.CharField(max_length=200, blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(default="no bio...", max_length=300)
	email = models.EmailField(max_length=200, blank=True)
	avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
	following = models.ManyToManyField(User, blank=True, related_name='following')
	slug = models.SlugField(unique=True, blank=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user.username}'

	def get_users_to_follow(self):
		return Profile.objects.all().exclude(user=self.user)

	def get_following_count(self):
		return self.following.all().count()

	def profile_posts_count(self):
		return self.posts.all().count()

	def profiles_posts(self):
		return self.posts.all()

	def save(self, *args, **kwargs):
		exist_name = False
		if self.first_name and self.last_name:
			to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
			exist_name = Profile.objects.filter(slug=to_slug).exists()

			while exist_name:
				to_slug = slugify(to_slug + " " + str(get_random_code()))
				exist_name = Profile.objects.filter(slug=to_slug).exists()
		else:
			to_slug = str(self.user)
		self.slug = to_slug
		super().save(*args, **kwargs)



