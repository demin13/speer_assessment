from django.urls import path
from .views import CreateUserView, SignInView
urlpatterns = [
    path('signup/', CreateUserView.as_view(), name='create_user'),
    path('login/', SignInView.as_view(), name='sign_in'),
]
