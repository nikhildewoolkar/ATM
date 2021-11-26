from . import views
# from .views import *
from django.urls import path
urlpatterns=[
    path("dashboard/",views.dashboard,name="dashboard"),
    path("logout/",views.logout,name="logout"),
    path("withdraw/",views.withdraw,name="withdraw"),
    path("changepin/",views.changepin,name="changepin"),
    path("checkbalance/",views.checkbalance,name="checkbalance"),
    path("deposite/",views.deposite,name="deposite"),
    path("login/",views.login,name="login"),
    path("",views.login,name="login"),
    path("home/",views.home,name="home"),
]