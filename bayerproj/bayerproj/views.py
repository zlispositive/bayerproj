#-*- coding: UTF-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from ta.models import *
from accounts.models import *
from accounts.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from tr.forms import TestingRequestForm
from tr.models import TestingRequest


@login_required
def index(request):
	context = RequestContext(request)

	userprofile_list = UserProfile.objects.order_by('rank')

	categoryAction = {
		'A': 'boss.html',
		'B': 'tghead.html',
		'C': 'pjhead.html',
		'D': 'pjstaff.html',
		'E': 'tgstaff.html',
	} #20140502-1146


	inputdata_dic = {
		'userprofiles' : userprofile_list, 
		'up':request.user.get_profile(),
		'rank':request.user.get_profile().rank,
		'tas':Testing_Activity.objects.all(),
		'category':categoryAction.get(request.user.get_profile().rank),
	}


	# temp = 'index.html'
	# return render_to_response(temp, inputdata_dic, context)
	# return render_to_response(categoryAction.get(request.user.get_profile().rank), inputdata_dic, context)
	return render_to_response(inputdata_dic.get('category'), inputdata_dic,context)

@login_required
def requestinfo(request, listnumber):
	context = RequestContext(request)
	data_dic={}
	data_dic['RequestInfo'] = TestingRequest.objects.filter(pk__exact=listnumber)[0]

	print listnumber,'mark'

	return render_to_response('requestinfo.html', data_dic, context)


def search_form(request):
	return render_to_response('search_form.html')

def search(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		# testingactivities = Testing_Activity.objects.filter(testing_name__iexact=q)
		testingactivities = Testing_Activity.objects.all()
		return render_to_response('search_result.html', {'query':q, 'tas':testingactivities})
	else:
		return HttpResponse('Please submit a search term.')

def thanks(request):
	return render_to_response('thanks.html')

def present_everything(request):
	return None

def register(request):

	context = RequestContext(request)
	registered = False

	categoryAction = {
		'A': 'boss',
		'B': 'tghead',
		'C': 'pjhead',
		'D': 'pjstaff',
		'E': 'tgstaff',
	} 

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit = False)
			profile.user = user


			profile.save()

			registered = True

			# amount = User.objects.all().count()
			# temp = User.objects.filter(pk=amount)[0].title
			# User.objects.filter(pk=amount).update(rank=categoryAction.get(temp))
			# User.objects.get(pk=amount).save()
			

		else:
			print user_form.errors, profile_form.errors

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	categoryAction = {
		'boss': 'A',
		'tghead': 'B' ,
		'pjhead': 'C' ,
		'pjstaff': 'D' ,
		'tgstaff': 'E' ,
	} #20140502-1146\

	if registered:
		# temp = request.user.get_profile().rank
		# temp = categoryAction.get(temp)

		# return HttpResponse('/index/%s/' % temp)
		print 'starting replacing none level'
		amount = UserProfile.objects.all().count()
		temp = str(UserProfile.objects.filter(pk=amount)[0].title).lower()
		print temp,categoryAction.get(temp)
		UserProfile.objects.filter(pk=amount).update(rank=categoryAction.get(temp))
		print UserProfile.objects.filter(pk=amount)
		# UserProfile.objects.get(pk=amount).rank = temp
		# UserProfile.objects.get(pk=amount).save()

	return render_to_response(
			'register.html',
			{'user_form': user_form, 'profile_form': profile_form, 'registered':registered},
			context
		)
	
def user_login(request):
	context = RequestContext(request)

	# categoryAction = {
	# 	'A': 'boss',
	# 	'B': 'tghead',
	# 	'C': 'pjhead',
	# 	'D': 'pjstaff',
	# 	'E': 'tgstaff',
	# } #20140502-1146

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)


		if user is not None:
			if user.is_active:
				login(request, user)
				# temp = request.user.get_profile().rank
				# temp = categoryAction.get(temp)
				temp = request.user.get_profile().title
				# return HttpResponseRedirect('/index/')
				return HttpResponseRedirect('/index/%s/' % str(temp)) #20140502-2332
			else:
				return HttpResponse("Your account is not active.")
		else:
			print "In valid login details: {0}, {1}".format(username, password)
			return HttpResponse(" Invalid login details supplied. <br \> <br \>  Please re-login or contact IT staff.  <br \> <br \>  <a href='/login/''>Login Again</a>")
	else:
		return render_to_response('login.html', {}, context)

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/login/')

@login_required
def about(request):
	return render_to_response('about.html', )

@login_required
def category(request, title):
	context = RequestContext(request)
	data_dic={}

	try:
		data_dic = {
		'up': request.user.get_profile(),
		}
	except Exception, e:
		print Exception,":",e

	# switch ={
	# 'pjstaff': requesthistroy(request, data_dic, TestingRequest),
	# 'tgstaff': '',
	# }

	if title ==	'boss':
		None

	if title == 'pjhead':
		staffrhsummary(request, data_dic)
		# pjwaitinglist(request, data_dic)
		# pjprocessinglist(request,data_dic)
		# pjcompletedlist(request, data_dic)

		pjlist(request, data_dic)

	if title == 'pjstaff':
		requesthistroy(request, data_dic)
		#get request histroy for pjstaff
	
	if title == 'tgstaff':
		waitinglist(request, data_dic)
		completedlist(request, data_dic)
		deletedlist(request, data_dic)
		processinglist(request, data_dic)

	if title == 'tghead':
		requester_count(request, data_dic)
		date_count(request, data_dic)
		date_action_count(request, data_dic)
		item_count(request, data_dic)
		status_count(request, data_dic)
		testingtime_count(request, data_dic)


	# for item in data_dic:
	# 	print item,":", data_dic[item]

	return render_to_response('%s.html' % title, data_dic, context)

def staffrhsummary(request, data_dic):
	requesthistroy_summary={}

	pusername = request.user.username
	puser = User.objects.get(username=pusername)
	pbu = UserProfile.objects.get(user=puser).bu

	for pjs in UserProfile.objects.filter(bu=pbu):
		if pjs.title == 'pjstaff':
			if pjs not in requesthistroy_summary:
				# requesthistroy_summary[pjs.user] = []
				requesthistroy_summary[pjs.user] = {}
			for pjstr in TestingRequest.objects.filter(requester=pjs.user):
				for pjstritem in pjstr.item.all():
					if pjstritem not in requesthistroy_summary[pjs.user]:
						requesthistroy_summary[pjs.user][pjstritem] = int(1)
					else:
						requesthistroy_summary[pjs.user][pjstritem] = requesthistroy_summary[pjs.user][pjstritem] + 1				
			# requesthistroy_summary[pjs.user].append()
			# else:
			# 	requesthistroy_summary[pjs.user].append()

	print 'staffrhsummary functions'

	data_dic['RequestHistoySummary']=requesthistroy_summary
	return data_dic

def pjlist(request, data_dic):
	pj_list = {
	'WaitingList':[],
	'ProcessingList':[],
	'CompletedList':[],
	'DeletedList':[],
	}

	pusername = request.user.username
	puser = User.objects.get(username=pusername)
	pbu = UserProfile.objects.get(user=puser).bu
	
	for tritem in TestingRequest.objects.all():
		requester = tritem.requester
		user = User.objects.get(username=requester)
		bu = UserProfile.objects.get(user=user).bu
		if bu == pbu:
			if tritem.status == 'Waiting List':
				pj_list['WaitingList'].append(tritem)
			elif tritem.status == 'Processing':
				pj_list['ProcessingList'].append(tritem)
			elif tritem.status == 'Completed':
				pj_list['CompletedList'].append(tritem)
			elif tritem.status == 'Deleted':
				pj_list['DeletedList'].append(tritem)
			else:
				print 'Wrong Status'
	
	print pj_list

	data_dic['PjList']=pj_list
	return data_dic

def pjwaitinglist(request, data_dic):
	pj_waitinglist={}

	pusername = request.user.username
	puser = User.objects.get(username=pusername)
	pbu = UserProfile.objects.get(user=puser).bu
	
	for tritem in TestingRequest.objects.all():
		requester = tritem.requester
		user = User.objects.get(username=requester)
		bu = UserProfile.objects.get(user=user).bu
		if bu == pbu:
			print 'Own people'
		else:
			print 'Alien'


	data_dic['PjWaitingList']=pj_waitinglist
	return data_dic

def pjprocessinglist(request, data_dic):
	return data_dic

def pjcompletedlist(request, data_dic):
	return data_dic


def requesthistroy(request, data_dic):
	data_dic['RequestHistroy']=TestingRequest.objects.filter(requester=request.user.username)
	print 'requesthistroy functions'
	return data_dic

def waitinglist(request, data_dic):
	data_dic['WaitingList']=TestingRequest.objects.filter(status__iexact='Waiting List')
	print 'waitinglist functions'
	return	data_dic

def completedlist(request, data_dic):
	data_dic['CompletedList']=TestingRequest.objects.filter(status__iexact='Completed')
	print 'tackledlist functions'
	return data_dic

def processinglist(request, data_dic):
	data_dic['ProcessingList']=TestingRequest.objects.filter(status__iexact='Processing')
	print 'processinglist functions'
	return data_dic

def deletedlist(request, data_dic):
	data_dic['DeletedList']=TestingRequest.objects.filter(status__iexact='Deleted')
	print 'deletedlist functions'
	return data_dic

def requester_count_fun(keyword):
	return TestingRequest.objects.filter(requester__iexact=keyword).count()
	#

def requester_count(request, data_dic):
	requestercounter={}

	print 'requester counter'

	for im in TestingRequest.objects.all():
		if im.requester not in requestercounter:
			# print im.requester

			puser = User.objects.get(username=im.requester)
			pbu = UserProfile.objects.get(user=puser).bu
			requestercounter[ str(pbu)+' '+str(im.requester)] = requester_count_fun(im.requester)
			
			#requester-->User--->UserProfile
			
	data_dic['RequesterCounter']=requestercounter
	return data_dic

# def date_count(self, keyword):
# 	return self.filter(date__iexact=keyword).count()

def date_count(request, data_dic):
	
	datecounter = {}
	dateyearcounter={}
	datemonthcounter={}
	dateweekcounter={}

	for im in TestingRequest.objects.all():
		# print im.date.strftime('%Y-%m-%d %H:%M:%S %U')
		date = str(im.date.strftime('%Y %B %d'))
		date_year = str(im.date.strftime('%Y'))
		date_month = str(im.date.strftime('%B'))
		date_week = str(im.date.strftime('%W'))

		if date in datecounter:
			datecounter[date] = datecounter[date] + 1 
		else:
			datecounter[date] = 0

		if date_year in dateyearcounter:
			dateyearcounter[date_year] = dateyearcounter[date_year] + 1
		else:
			dateyearcounter[date_year] = 0
		
		temp = date_year+' '+date_month 
		if temp in datemonthcounter:
			datemonthcounter[temp] = datemonthcounter[temp] + 1
		else:
			datemonthcounter[temp] = 0

		temp = date_year +' #'+ date_week
		if temp in dateweekcounter:
			dateweekcounter[temp] = dateweekcounter[temp] + 1
		else:
			dateweekcounter[temp] = 0


	data_dic['DateCounter']=datecounter
	data_dic['DateYearCounter']=dateyearcounter
	data_dic['DateMonthCounter']=datemonthcounter
	data_dic['DateWeekCounter']=dateweekcounter

	return data_dic

def date_action_count(request, data_dic):
	
	dateactioncounter = {}
	dateactionyearcounter={}
	dateactionmonthcounter={}
	dateactionweekcounter={}

	for im in TestingRequest.objects.all():
		# print im.dateaction.strftime('%Y-%m-%d %H:%M:%S %U')
		dateaction = str(im.date_action.strftime('%Y %B %d'))
		dateaction_year = str(im.date_action.strftime('%Y'))
		dateaction_month = str(im.date_action.strftime('%B'))
		dateaction_week = str(im.date_action.strftime('%W'))

		# if dateaction in dateactioncounter:
		# 	dateactioncounter[dateaction] = dateactioncounter[dateaction] + 1 
		# else:
		# 	dateactioncounter[dateaction] = 0

		# if dateaction_year in dateactionyearcounter:
		# 	dateactionyearcounter[dateaction_year] = dateactionyearcounter[dateaction_year] + 1
		# else:
		# 	dateactionyearcounter[dateaction_year] = 0

		# if dateaction_month in dateactionmonthcounter:
		# 	dateactionmonthcounter[dateaction_month] = dateactionmonthcounter[dateaction_month] + 1
		# else:
		# 	dateactionmonthcounter[dateaction_month] = 0

		# if dateaction_week in dateactionweekcounter:
		# 	dateactionweekcounter[dateaction_week] = dateactionweekcounter[dateaction_week] + 1
		# else:
		# 	dateactionweekcounter[dateaction_week] = 0

		if dateaction in dateactioncounter:
			dateactioncounter[dateaction] = dateactioncounter[dateaction] + 1 
		else:
			dateactioncounter[dateaction] = 0

		if dateaction_year in dateactionyearcounter:
			dateactionyearcounter[dateaction_year] = dateactionyearcounter[dateaction_year] + 1
		else:
			dateactionyearcounter[dateaction_year] = 0
		
		temp = dateaction_year+' '+dateaction_month 
		if temp in dateactionmonthcounter:
			dateactionmonthcounter[temp] = dateactionmonthcounter[temp] + 1
		else:
			dateactionmonthcounter[temp] = 0

		temp = dateaction_year +' #'+ dateaction_week
		if temp in dateactionweekcounter:
			dateactionweekcounter[temp] = dateactionweekcounter[temp] + 1
		else:
			dateactionweekcounter[temp] = 0

	data_dic['DateActionCounter']=dateactioncounter
	data_dic['DateActionYearCounter']=dateactionyearcounter
	data_dic['DateActionMonthCounter']=dateactionmonthcounter
	data_dic['DateActionWeekCounter']=dateactionweekcounter

	return data_dic

# def item_count_fun(keyword):
# 	return TestingRequest.objects.get_or_create(item=keyword).count()

def item_count(requester, data_dic):
	itemcounter={}
	print 'item counter'
	for im in TestingRequest.objects.all():
		for ims in im.item.all():
			# if ims not in itemcounter:
				# itemcounter[str(ims)] = item_count_fun(str(ims)) #internal count is not applicable
			itemcounter[str(ims)] = 0
		# if im.item not in itemcounter:
		# 	print 'print i.item', im.item.all()

		# 	# itemcounter[str(im.item)] = item_count_fun(im.item)
	for im in TestingRequest.objects.all():
		for ims in im.item.all():
			itemcounter[str(ims)] = itemcounter[str(ims)]+1


	data_dic['ItemCounter']=itemcounter
	return data_dic

def status_count_fun(keyword):
	return TestingRequest.objects.filter(status__iexact=keyword).count()

def status_count(request, data_dic):
	statuscounter={}
	print 'status counter'

	for im in TestingRequest.objects.all():
		if im.status not in statuscounter:
			statuscounter[str(im.status)] = status_count_fun(im.status)
	data_dic['StatusCounter'] = statuscounter

	return data_dic

def testingtime_count(request, data_dic):
	testingtimecount={}

	for im in TestingRequest.objects.all():
		date2 = im.date_action
		date1 = im.date
		delta = date2- date1
		dayscount = delta.days
		hourscount = delta.seconds/60/60
		minutescount = delta.seconds%3600/60
		secondscount = delta.seconds%60

		if im.item.all().count() == 1:
			temp = str(im.item.all()[0])
			testingtimecount[temp] = '%s Time: %sdays %shours %sminutes %sseconds' % (im.status ,dayscount, hourscount, minutescount, secondscount)
		else:
			print 'Not applicable'

	data_dic['TestingTimeCount']=testingtimecount
	return data_dic

@login_required
def add_request(request):
	context = RequestContext(request)
	filed = False

	# categoryAction = {
	# 	'A': 'boss',
	# 	'B': 'tghead',
	# 	'C': 'pjhead',
	# 	'D': 'pjstaff',
	# 	'E': 'tgstaff',
	# } #20140502-1146

	temp=request.user.get_profile().title
	# temp=categoryAction.get(temp)

	if temp == 'pjstaff':
		if request.method == 'POST':
			form = TestingRequestForm(request.POST)

			if form.is_valid():
				form.save(commit=True)
				filed = True
				# return category(request,str(temp))
			else:
				print 'error in add_request'
				print form.errors
		else:
			form = TestingRequestForm()
	else:
		errors={'error':"You are not allowed to file a request."}
		# return render_to_response('errors.html',errors, context)
		return HttpResponseRedirect('/index/pjstaff/')
	
	print filed
	if filed:
		amount=TestingRequest.objects.all().count()
		TestingRequest.objects.filter(pk=amount).update(requester=request.user.username)
		TestingRequest.objects.filter(pk=amount).update(email=request.user.email)
		TestingRequest.objects.get(pk=amount).save()
		return HttpResponseRedirect('/index/pjstaff/')

	return render_to_response(
		'add_request.html', 
		{'form':form,'filed':filed}, 
		context)

@login_required
def del_request(request, listnumber):
	#del_request is actually just changing the status of a testing request
	
	context = RequestContext(request)
	data_dic={}
	errors={}

	pusername = request.user.username
	puser = User.objects.get(username=pusername)
	ptitle = str(UserProfile.objects.get(user=puser).title).lower()

	if ptitle == 'pjhead':
		# delete anyway
		if TestingRequest.objects.filter(pk=str(listnumber))[0].status == 'Deleted':
			errors['AlreadyDeletedError']='AlreadyDeletedError'
		else:	
			# TestingRequest.objects.get(pk__exact=str(listnumber))[0].status = 'Deleted'
			# TestingRequest.objects.get(pk__exact=str(listnumber))[0].save()
			TestingRequest.objects.filter(pk=listnumber).update(status='Deleted')
			TestingRequest.objects.get(pk=listnumber).save()

			temp = TestingRequest.objects.filter(pk=listnumber)[0].comment
			temp = temp+('\n %s deleted @ %s \n' % ( request.user.username, TestingRequest.objects.filter(pk=listnumber)[0].date_action.strftime('%Y-%m-%d %H:%M:%S')))
			TestingRequest.objects.filter(pk=listnumber).update(comment=temp)

			TestingRequest.objects.get(pk=listnumber).save()

			# print TestingRequest.objects.filter(pk=str(listnumber))[0].status 
			errors['Deleted']='Deleted'
	else:
		# need to check identity
		if request.user.username == TestingRequest.objects.filter(pk=str(listnumber))[0].requester:
			if TestingRequest.objects.filter(pk=str(listnumber))[0].status == 'Deleted':
				errors['AlreadyDeletedError']='AlreadyDeletedError'
			else:	
				# TestingRequest.objects.get(pk__exact=str(listnumber))[0].status = 'Deleted'
				# TestingRequest.objects.get(pk__exact=str(listnumber))[0].save()
				TestingRequest.objects.filter(pk=listnumber).update(status='Deleted')
				TestingRequest.objects.get(pk=listnumber).save()

				temp = TestingRequest.objects.filter(pk=listnumber)[0].comment
				temp = temp+('\n %s deleted @ %s \n' % ( request.user.username, TestingRequest.objects.filter(pk=listnumber)[0].date_action.strftime('%Y-%m-%d %H:%M:%S')))
				TestingRequest.objects.filter(pk=listnumber).update(comment=temp)

				TestingRequest.objects.get(pk=listnumber).save()

				# print TestingRequest.objects.filter(pk=str(listnumber))[0].status 
				errors['Deleted']='Deleted'
		else:
			errors['WrongUserError']='WrongUserError'
	

	# if request.user.username == TestingRequest.objects.filter(pk=str(listnumber))[0].requester:
	# 	if TestingRequest.objects.filter(pk=str(listnumber))[0].status == 'Deleted':
	# 		errors['AlreadyDeletedError']='AlreadyDeletedError'
	# 	else:	
	# 		# TestingRequest.objects.get(pk__exact=str(listnumber))[0].status = 'Deleted'
	# 		# TestingRequest.objects.get(pk__exact=str(listnumber))[0].save()
	# 		TestingRequest.objects.filter(pk=listnumber).update(status='Deleted')
	# 		TestingRequest.objects.get(pk=listnumber).save()

	# 		temp = TestingRequest.objects.filter(pk=listnumber)[0].comment
	# 		temp = temp+('\n %s deleted @ %s \n' % ( request.user.username, TestingRequest.objects.filter(pk=listnumber)[0].date_action.strftime('%Y-%m-%d %H:%M:%S')))
	# 		TestingRequest.objects.filter(pk=listnumber).update(comment=temp)

	# 		TestingRequest.objects.get(pk=listnumber).save()

	# 		# print TestingRequest.objects.filter(pk=str(listnumber))[0].status 
	# 		errors['Deleted']='Deleted'
	# else:
	# 	errors['WrongUserError']='WrongUserError'


	data_dic['Errors']=errors

	data_dic['item']=TestingRequest.objects.filter(pk=str(listnumber))[0]

	# return render_to_response('del_request.html',
	# 	data_dic,
	# 	context) 


	if ptitle == 'pjstaff':
		return HttpResponseRedirect('/index/pjstaff/') #20140505-1428
	elif ptitle == 'pjhead':
		return HttpResponseRedirect('/index/pjhead/') #20140505-1428
	else:
		pass

def tackle_request(request, listnumber):
	context = RequestContext(request)
	acted = False

	data_dic={'form':TestingRequestForm(request.POST)} # Very important to pass it

	data_dic['ListNumber'] = int(listnumber)
	data_dic['ChosenItem'] = TestingRequest.objects.filter(pk=str(listnumber))

	if request.method == 'POST':
		form = TestingRequestForm(request.POST)

		if form.is_valid():
			form.save(commit=True)
			acted = True
		else:
			print form.errors
	else:
		form = TestingRequestForm()


	print listnumber
	return render_to_response('tackle_request.html',
		data_dic,
		context)

def process_request(request, listnumber):
	context = RequestContext(request)
	data_dic={'ListNumber':listnumber}

	data_dic['RequestInfo'] = TestingRequest.objects.get(pk=listnumber)
	TestingRequest.objects.filter(pk=listnumber).update(status='Processing')
	TestingRequest.objects.filter(pk=listnumber).update(responser=request.user.username)
	TestingRequest.objects.get(pk=listnumber).save()


	temp = TestingRequest.objects.filter(pk=listnumber)[0].comment
	temp = temp+('\n %s started processing @ %s \n' % ( request.user.username, TestingRequest.objects.filter(pk=listnumber)[0].date_action.strftime('%Y-%m-%d %H:%M:%S')))
	TestingRequest.objects.filter(pk=listnumber).update(comment=temp)



	TestingRequest.objects.get(pk=listnumber).save()

	if str(TestingRequest.objects.get(pk=listnumber).status).lower() == 'processing':
		cbcindex=True
		data_dic['cbcindex']=cbcindex

	return render_to_response('process_request.html',
		data_dic,
		context)

def complete_request(request, listnumber):
	context = RequestContext(request)
	data_dic={'ListNumber':listnumber}

	data_dic['RequestInfo'] = TestingRequest.objects.get(pk=listnumber)
	TestingRequest.objects.filter(pk=listnumber).update(status='Completed')
	TestingRequest.objects.get(pk=listnumber).save()

	temp = TestingRequest.objects.filter(pk=listnumber)[0].comment
	temp = temp+('\n %s completed @ %s \n' % ( request.user.username, TestingRequest.objects.filter(pk=listnumber)[0].date_action.strftime('%Y-%m-%d %H:%M:%S')))
	TestingRequest.objects.filter(pk=listnumber).update(comment=temp)

	TestingRequest.objects.get(pk=listnumber).save()

	# return render_to_response('complete_request.html',
	# 	data_dic,
	# 	context)
	return HttpResponseRedirect('/index/tgstaff/')