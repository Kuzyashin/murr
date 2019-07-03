from django.urls import path

from Murren.viewsets import CurrentUserView, CustomAuthToken
from . import views as murren

urlpatterns = [
    path('follow/', murren.follow, name='murren_follow'),
    path('unfollow/', murren.unfollow, name='murren_unfollow'),
    path('<str:username>/', murren.profile, name='murren_profile'),
    path('my/myprofile/', CurrentUserView.as_view(), name='my_murren'),
    path('profile/get-token/', CustomAuthToken.as_view(), name='get_token'),

]
