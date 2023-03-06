from django.urls import path, include
from student import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.home, name= "home"), # homepage 
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path("signout",auth_views.LogoutView.as_view(next_page="signin"),name="signout"),
    path('update', views.update, name='update'),
    path('achome', views.accountshome, name='achome'),
    path('updatefee/<int:id>', views.updatefee, name='updatefee'),
    path('adhome', views.adminhome, name='adhome'),
    path('adupdate/<int:id>', views.adupdate, name='adupdate'),
    path('adelete/<int:id>', views.adelete, name='adelete'),
    path('search', views.search, name='search'),

]