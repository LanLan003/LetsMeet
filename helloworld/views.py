from django.shortcuts import render,redirect   # 加入 redirect 套件
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
from event.models import Event, Response


def createEvent(request):
	#error = False
	if request.GET:
		eventName = request.GET.get('eventName')
		owner = request.GET.get('owner')
		dayChosen = request.GET.get('dayChosen')
		timeChosen = request.GET.get('timeChosen')
		randUrl = '/' + request.GET.get('randUrl') + '/'
		#if not eventName or not dayChosen:
		#	error = True
		#if not error:
		Event.objects.create(eventName=eventName, owner=owner, dayChosen=dayChosen, timeChosen=timeChosen, randUrl=randUrl)
		return redirect(randUrl)
	return render(request, 'week.html')



def newEvent(request):
	current = request.get_full_path()
	event = Event.objects.get(randUrl=current)
	eventName = event.eventName

	dC = event.dayChosen
	dayChosen = dC.split(",",dC.count(","))
	tC = event.timeChosen
	timeChosen = tC.split(",",tC.count(","))

	if request.method == 'POST':
		yourName = request.POST.get('yourName')
		freeTime = request.POST.get('freeTime')
		Response.objects.create(yourName=yourName, freeTime=freeTime, event=event)
		return redirect(current+'result')
	return render(request, 'user.html',locals())



def resultpage(request):
	copy = request.build_absolute_uri()[0:-6]
	current = request.get_full_path()
	current = current[0:-6]
	event = Event.objects.get(randUrl=current)
	eventName = event.eventName

	dC = event.dayChosen
	dayChosen = dC.split(",",dC.count(","))
	tC = event.timeChosen
	timeChosen = tC.split(",",tC.count(","))
	
	options = []
	for h in timeChosen:
		for d in dayChosen:
			options.append(d + " : " + h)
	lo = len(options)

	results = Response.objects.filter(event=event)
	
	fT = []
	for i in range(len(results)):
		yourName = results[i].yourName
		f = results[i].freeTime
		freeTime = f.split(",",f.count(","))
		fT.append({yourName:freeTime})
		#fD.extend(f)

	# 計算星期幾出現幾次：
	times = []
	for t in fT:
		a = list(t.values())
		times.extend(a[0])
	
	counting = []
	for i in options:
		counting.append(times.count(i))
	
	maxNum = max(counting)
	scaleRange = range(maxNum)
	reply = len(results)


	#return HttpResponse(options)
	return render(request, 'result_try.html',locals())