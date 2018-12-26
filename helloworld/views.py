from django.shortcuts import render,redirect   # 加入 redirect 套件
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
from event.models import Event, Response


def index(request):
	#error = False
	if request.GET:
		eventName = request.GET.get('eventName')
		owner = request.GET.get('owner')
		dayChosen = request.GET.get('dayChosen')
		randUrl = '/' + request.GET.get('randUrl') + '/'
		#dC = dayChosen.split(",",dayChosen.count(","))
		#k = len(dC)
		#if not eventName or not dayChosen:
		#	error = True
		#if not error:
		Event.objects.create(eventName=eventName, owner=owner, dayChosen=dayChosen, randUrl=randUrl)
		return redirect(randUrl)
		#return render(request, 'user.html')
		#return HttpResponse('Done')
	return render(request, 'week_try_daytime.html')

def get_name(request):
	event = request.get_full_path()
	current = Event.objects.get(randUrl=event)
	dayChosen = current.dayChosen
	#dC = dayChosen.split(",",dayChosen.count(","))
	if request.method == 'POST':
		userName = request.POST.get('userName')
		freeDay = request.POST.get('freeDay')
		Response.objects.create(userName=userName, freeDay=freeDay, event=current)
		return redirect(event+'result')
	return render(request, 'user_try_daytime.html',locals())

def resultpage(request):
	copy = request.build_absolute_uri()[0:-6]
	event = request.get_full_path()
	event = event[0:-6]
	current = Event.objects.get(randUrl=event)
	dayChosen = current.dayChosen
	dC = dayChosen.split(",",dayChosen.count(","))

	results = Response.objects.filter(event=event)
	fD = []
	for i in range(len(results)):
		userName = results[i].userName
		freeDay = results[i].freeDay
		f = freeDay.split(",",freeDay.count(","))
		fD.append({userName:f})
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
	return render(request, 'result.html',locals())