from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist
import datetime
import os
from django.conf import settings
from django.core.mail import send_mail 
import numpy as np
from django.contrib import messages
from subprocess import check_output, CalledProcessError,STDOUT
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, request
from django.http import Http404
import socket
import asyncio
import logging
import channels
from channels.worker import Worker
from django.conf import settings
from channels.db import database_sync_to_async
import json
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
def turnon(request, atm_code):
    choice = request.GET.get("choice")
    context = {
        "char_choice": choice, 
        "room_code": atm_code
    }
    return render(request, "login.html", context)

def login(request):
    print("requested for login page")
    if request.method=="POST":
        print("requested for login")
        username=request.POST.get("username")
        password=request.POST.get("password")
        print("username and password",username,password)
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            print("Login granted")
            auth.login(request,user)
            print("sent reply to the client side")
            return redirect('/dashboard')
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('login')
    return render(request,"login.html")
def logout(request):
    print("Requested to logout")
    auth.logout(request)
    return render(request,"login.html")
def home(request):
    return render(request,"home.html")
def dashboard(request):
    print("Redirected to Dashboard")
    return render(request,"dashboard.html")
def withdraw(request):
    p1=request.user
    print("Requested withdraw money page",p1.username)
    if request.method=="POST":
        amount=request.POST.get("amount")
        print("Withdrawal request of Rs ",amount)
        print("Balance and requested cash",int(p1.last_name),int(amount))
        if(int(p1.last_name)<int(amount)):
            print("insufficient amount")
            messages.info(request,"Insufficient amount")
            return redirect('withdraw')
        else:
            User.objects.filter(username=p1.username).update(last_name=str(int(p1.last_name)-int(amount)))
            try:
                print("Withdrawal request of Rs ",amount," successful")
                subject = 'Withdraw request successful'   
                message = f'Hi {p1.username},You have successfully withdrawal {amount}RS.'
                email_from = settings.EMAIL_HOST_USER 
                recipient_list = [p1.username] 
                send_mail( subject, message, email_from, recipient_list ,fail_silently=False)
                print("email sent successfully.")
            except:
                print("exception in mail.")
            messages.info(request,"(RS "+amount+")Withdraw request successful. Mail has been sent to your gmail address.")
            return redirect('dashboard')
    return render(request,"withdraw.html")
def changepin(request):
    p1=request.user
    print("requested change pin page")
    if request.method=="POST":
        old=request.POST.get("old")
        new=request.POST.get("new")
        rnew=request.POST.get("rnew")
        if(p1.first_name==old and new==rnew):
            print("pin got changed")
            User.objects.filter(username=p1.username).update(first_name=new)
            u = User.objects.get(username=p1.username)
            u.set_password(new)
            u.save()
            try:
                subject = 'Pin change request successful'   
                message = f'Hi {p1.username},You have successfully changed pin.'
                email_from = settings.EMAIL_HOST_USER 
                recipient_list = [p1.username] 
                send_mail( subject, message, email_from, recipient_list ,fail_silently=False)
                print("email sent successfully.")
            except:
                print("exception in mail.")
            messages.info(request,"Pin changed")
            return redirect('logout')       
        else:
            print("Wrong pin or password not matching")
            messages.info(request,"Wrong pin or password not matching")
            messages.info(request,"changepin.html")
    return render(request,"changepin.html")

def checkbalance(request):
    print("check balance page triggered")
    p1=request.user
    msg="Your balance amount is "+p1.last_name+" ."
    return render(request,"checkbalance.html",{"msg":msg})
def deposite(request):
    p1=request.user
    print("Deposite money page triggered")
    if request.method=="POST":
        amount=request.POST.get("amount")
        User.objects.filter(username=p1.username).update(last_name=str(int(p1.last_name)+int(amount)))
        try:
            subject = 'Deposite request successful'   
            message = f'Hi {p1.username},You have successfully deposited {amount}RS.'
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = [p1.username] 
            send_mail( subject, message, email_from, recipient_list ,fail_silently=False)
            print("email sent successfully.")
            print("Deposite request of Rs ",amount," successful")
        except:
            print("exception in mail.")
        messages.info(request,"(RS "+amount+")Deposite request successful. Mail has been sent to your gmail address.")
        return redirect('dashboard')
    return render(request,"deposite.html")
