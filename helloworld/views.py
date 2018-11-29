from django.shortcuts import render,redirect   # 加入 redirect 套件
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
from event.models import Event, Respose


def index(request):
	error = False
	if request.GET:
		eventName = request.GET.get('eventName')
		dayChosen = request.GET.get('dayChosen')
		randUrl = '/' + request.GET.get('randUrl') + '/'
		#dC = dayChosen.split(",",dayChosen.count(","))
		#k = len(dC)
		#if not eventName or not dayChosen:
		#	error = True
		#if not error:
		Event.objects.create(eventName=eventName, dayChosen=dayChosen, randUrl=randUrl)
		return redirect(randUrl)
		#return render(request, 'user.html')
		#return HttpResponse('Done')

	return render(request, 'week.html')

def get_name(request):
	event = request.get_full_path()
	current = Event.objects.get(randUrl=event)
	dayChosen = current.dayChosen
	dC = dayChosen.split(",",dayChosen.count(","))
	if request.method == 'POST':
		userName = request.POST.get('userName')
		freeDay = request.POST.get('freeDay')
		Respose.objects.create(userName=userName, freeDay=freeDay, event=current)
		return redirect(event+'result')
	return render(request, 'user.html',locals())

def resultpage(request):
	event = request.get_full_path()
	return render(request, 'result.html',locals())