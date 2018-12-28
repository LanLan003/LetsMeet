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
		freeDay = request.POST.get('freeDay')
		Response.objects.create(yourName=yourName, freeDay=freeDay, event=event)
		return redirect(current+'result')
	return render(request, 'user_try_daytime.html',locals())



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
	results = Response.objects.filter(event=event)
	fD = []
	for i in range(len(results)):
		yourName = results[i].yourName
		freeDay = results[i].freeDay
		f = freeDay.split(",",freeDay.count(","))
		fD.append({yourName:f})
		#fD.extend(f)

	# 計算星期幾出現幾次：
	days = []
	for d in fD:
		a = list(d.values())
		days.extend(a[0])
	
	counting = []
	for i in dC:
		counting.append(days.count(i))
	
	maxNum = max(counting)
	scaleRange = range(maxNum)
	reply = len(results)






	#顯示每一天有多少人選：


	#show = tuple()
	#for d in fD:
	#	show.insert(d,fD.count(d))
	#	show[d] = show.get(d,0) + 1

	#show = dict()
	#for d in fD:
	#	show[d] = show.get(d,0) + 1

	#--------  我是笨蛋啦繞一圈回來做一樣的事ＱＱ --------#
	# results = Response.objects.filter(event=event) #
	# freeDay = []                                   #
	# for i in range(len(results)):                  #
	# 	free = results[i].freeDay                    #
	# 	f = free.split(",",dayChosen.count(","))     #
	# 	freeDay.extend(f)                            #
	# freeDay.sort()                                 #
	# setFreeDay = list(set(freeDay))                #
	# setFreeDay.sort(key=freeDay.index)             #
	#----------------- 笨蛋紀念區ＱＱ -----------------#

	#return HttpResponse(reply)
	return render(request, 'result_try.html',locals())