from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from .utils import get_random_code
from django.db import models

STATUS_CHOICES = (('send', 'send'), ('accepted', 'accepted'))

class Profile(models.Model):
	first_name = models.CharField(max_length=200, blank=True)
	last_name = models.CharField(max_length=200, blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(default="no bio...", max_length=300)
	email = models.EmailField(max_length=200, blank=True)
	country = models.CharField(max_length=200, blank=True)
	avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
	friends = models.ManyToManyField(User, blank=True, related_name='friends')
	slug = models.SlugField(unique=True, blank=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user.username}'

	def get_friends(self):
		return self.friends.all()

	def get_friends_number(self):
		return self.friends.all().count()

	def get_posts_number(self):
		return self.posts.all().count()

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


class Relationship(models.Model):
	sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
	receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
	status = models.CharField(max_length=8, choices=STATUS_CHOICES)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.sender} - {self.receiver} - {self.status}'

