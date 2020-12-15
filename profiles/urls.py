from .views import profile_view, UsersListView, UserProfileDetailView, follow_unfollow_profile
from django.urls import path

app_name = 'profiles'

urlpatterns = [
	path('myprofile/', profile_view, name='profile-view'),
	path('users/', UsersListView.as_view(), name='users-view'),
	path('follow/', follow_unfollow_profile, name='follow-unfollow-view'),
	path('<pk>/', UserProfileDetailView.as_view(), name='user-profile-detail-view'),
]
