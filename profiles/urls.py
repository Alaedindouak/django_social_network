from .views import profile_view
from django.urls import path

urlpatterns = [
	path('myprofile/', profile_view, name='profile-view'),
]
