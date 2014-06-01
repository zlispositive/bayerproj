from django.shortcuts import render_to_response
from django.http import HttpResponse
from ta.models import Testing_Activity

#-*- coding: UTF-8 -*-

def search_form(request):
	return render_to_response('search_form.html')

def search(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		# testingactivities = Testing_Activity.objects.filter(testing_name__icontains=q)
		testingactivities = Testing_Activity.objects.all()
		return render_to_response('search_result.html', {'query':q, 'tas':testingactivities})
	else:
		return HttpResponse('Please submit a search term.')

def thanks(request):
	return render_to_response('thanks.html')

def present_everything(request):
	return
