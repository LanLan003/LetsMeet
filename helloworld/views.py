from django.shortcuts import render,redirect   # 加入 redirect 套件
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
from event.models import Event, Response

def index(request):
	return render(request, 'welnew.html',locals())

def login(request):
	if request.user.is_authenticated:
		return render(request, 'home.html',locals())

	if request.method == 'POST':
		username = request.POST.get('name')
		password = request.POST.get('pass')
		user = auth.authenticate(username=username, password=password)
		auth.login(request,user)
		if user is not None:
			if user.is_active:
				auth.login(request,user)
				events = Event.objects.filter(owner=user.username)
				eventName = []
				for i in range(len(events)):
					name = events[i].eventName
					eventName.append(name)
			else:
				return HttpResponse('尚未登入')
		else:
			return HttpResponse('登入失敗!')
	return render(request, 'home.html', locals())

def logout(request):
	auth.logout(request)
	return render(request, 'welnew.html',locals())

def signup(request):
	if request.method == 'POST':
		username = request.POST.get('regname')
		password = request.POST.get('regpass')
		email = ""
		
		# --- 不會顯示登入error! --- #
		try:
			user = User.objects.get(username=username)
		except:
			#user = None
			#if user is None:
			user = User.objects.create_user(username, email, password)
			user.save()
			#messages.add_message(request, messages.INFO, '註冊成功')
			messages.info(request, '註冊成功')
			#print('註冊成功')
		else:
			#messages.add_message(request, messages.INFO, '此使用者已經有人使用')
			messages.info(request, '此使用者已經有人使用')
			#print("此使用者已經有人使用")              
		
		return redirect('/')


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
	while "" in dayChosen:
		dayChosen.remove("")
	tC = event.timeChosen
	timeChosen = tC.split(",",tC.count(","))
	while "" in timeChosen:
		timeChosen.remove("")

	error = False # 完成使用者名稱不重複！
	if request.method == 'POST':
		yourName = request.POST.get('yourName')
		try:
			Response.objects.get(yourName=yourName, event=event)
			error = True
		except:
			freeTime = request.POST.get('freeTime')
			Response.objects.create(yourName=yourName, freeTime=freeTime, event=event)
			return redirect(current+'result')
	lastDay = dayChosen[len(dayChosen)-1]

	ifDate = False
	num = "0123456789"
	for i in num:
		if i in dC:
			ifDate = True

	if ifDate == True:
		return render(request, 'user_date.html',locals())
	else:
		return render(request, 'user.html',locals())


def resultpage(request):
	copy = request.build_absolute_uri()[0:-6]
	current = request.get_full_path()
	current = current[0:-6]
	event = Event.objects.get(randUrl=current)
	eventName = event.eventName

	dC = event.dayChosen
	dayChosen = dC.split(",",dC.count(","))
	while "" in dayChosen:
		dayChosen.remove("")
	tC = event.timeChosen
	timeChosen = tC.split(",",tC.count(","))
	while "" in timeChosen:
		timeChosen.remove("")
	
	options = []
	for h in timeChosen:
		for d in dayChosen:
			options.append(d + "_" + h)
	lo = len(options)

	results = Response.objects.filter(event=event)
	
	fT = []
	yourName = []
	freeTime = []
	for i in range(len(results)):
		yourName.append(results[i].yourName)
		f = results[i].freeTime
		freeTime.extend(f.split(",",f.count(",")))
		fT.append({results[i].yourName:f.split(",",f.count(","))})
		#fD.extend(f)


	# 計算各個時段出現幾次：

	#times = []
	#for t in fT:
	#	a = list(t.values())
	#	times.extend(a[0])
	
	counting = []
	for o in options:
		counting.append(freeTime.count(o))
	
	maxNum = max(counting)
	scaleRange = range(maxNum)
	reply = len(results)

	
	# 找出每個時段的人:

	ao = []
	do = []

	for o in options:
		p_in_o = []
		p_notin_o = []

		for p in yourName:
			r = Response.objects.get(yourName=p, event=event)  # 記得刪掉重複的名字！
			f = r.freeTime
			free = f.split(",",f.count(","))

			if o in free:
				p_in_o.append(p)
			else:
				p_notin_o.append(p)

			
			#for j in range(len(r)):
				#f = r[j].freeTime
				
		ao.append({o:p_in_o})
		do.append({o:p_notin_o})	

	lastDay = dayChosen[len(dayChosen)-1]

	ifDate = False
	num = "0123456789"
	for i in num:
		if i in dC:
			ifDate = True

	if ifDate == True:
		return render(request, 'result_date.html',locals())
	else:
		return render(request, 'result.html',locals())