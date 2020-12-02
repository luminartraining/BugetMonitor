from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from django.shortcuts import redirect
from django.db.models import Sum,Aggregate
from Budget.forms import RegistrationForm,LoginForm
from Budget.models import Expenses
from Budget.forms import AddExpensForm,ReviewExpenseForm

from django.contrib.auth.decorators import login_required
def index(request):
    return render(request,"Budget/base.html")
def register(request):
    form=RegistrationForm()
    context={}
    context["form"]=form
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"Budget/login.html")
    return render(request,"Budget/registration.html",context)

def signIn(request):
    form=LoginForm()
    context={}
    context["form"]=form
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)

                return render(request, "Budget/home.html")
            else:

                return render(request, "Budget/login.html", context)
    return render(request,"Budget/login.html",context)

def singOut(request):
    logout(request)
    return redirect("signIn")

from django.contrib.auth.models import User
@login_required
def editProfile(request):
    user=User.objects.get(username=request.user)
    form=RegistrationForm(instance=user)
    context={}
    context["form"]=form
    if request.method=="POST":
        form=RegistrationForm(instance=user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        context["form"]=form
        return render(request, "Budget/editProfile.html", context)

    return render(request,"Budget/editProfile.html",context)



def userHome(request):
    return render(request,"Budget/home.html")

@login_required
def addExpens(request):
    form=AddExpensForm(initial={"user":request.user})
    context={}
    context["form"]=form
    expenses=Expenses.objects.filter(user=request.user)
    context["expenses"]=expenses
    if request.method=="POST":
        form=AddExpensForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("addExpenses")

    return render(request,"Budget/addexpens.html",context)

@login_required
def editExpenses(request,id):
    expense=Expenses.objects.get(id=id)
    print(expense)
    form=AddExpensForm(instance=expense)
    context={}
    context["form"]=form
    if request.method=="POST":
        form=AddExpensForm(instance=expense,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("addExpenses")
        else:
            context["form"]=form
            return render(request, "Budget/editexpense.html", context)

    return render(request,"Budget/editexpense.html",context)


@login_required
def deleteExpense(request,id):
    try:
        Expenses.objects.get(id=id).delete()
        return redirect("addExpenses")
    except Exception as e:
        return redirect("addExpenses")
@login_required
def review_expens(request):
    form=ReviewExpenseForm(initial={"user":request.user})
    context={}
    context["form"]=form
    if request.method=='POST':
        form=ReviewExpenseForm(request.POST)
        if form.is_valid():
            frmdate=form.cleaned_data.get("from_date")
            todate= form.cleaned_data.get("to_date")
            print(frmdate,",",todate)



            total=Expenses.objects.filter(date__gte=frmdate,date__lte=todate,user=request.user).aggregate(Sum('amount'))
            expenses = Expenses.objects.filter(date__gte=frmdate, date__lte=todate, user=request.user)

            context["total"]=total
            context["expenses"]=expenses
            return render(request, "Budget/reviewExpenses.html", context)
    return render(request,"Budget/reviewExpenses.html",context)