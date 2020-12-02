"""BudgetMonitoringSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Budget.views import register,signIn,singOut,editProfile,\
    userHome,addExpens,editExpenses,deleteExpense,review_expens,index
urlpatterns = [
    path("",index,name="index"),
path("register",register,name="register"),
    path("signIn",signIn,name="signIn"),
    path("signOut",singOut,name="signOut"),
    path("edit",editProfile,name="edit"),
    path("home",userHome,name="home"),
    path("addExpenses",addExpens,name="addExpenses"),
    path("editexpenses/<int:id>",editExpenses,name="editexpens"),
    path("deleteexpense/<int:id>", deleteExpense, name="delete"),
    path("review",review_expens,name="review")
]
