from django.urls import path
from .views import users_list,activate_view,login_user

app_name="account"
urlpatterns = [
    path('register/', users_list),
    path('activate/<slug:uidb64>/<slug:token>/',activate_view, name="activate"),
    path('login',login_user, name="login"),
]


