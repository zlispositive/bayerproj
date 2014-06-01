from django import forms
from tr.models import TestingRequest
from ta.models import Testing_Activity

class TestingRequestForm(forms.ModelForm):

	# requester = forms.ModelMultipleChoiceField(queryset=User.objects.all())
	requester = forms.CharField(widget=forms.HiddenInput(), max_length=128, help_text="Please enter your name.", initial=' ')

	# requester = forms.CharField(max_length=128, help_text="Please enter your name.")

	responser = forms.CharField(widget=forms.HiddenInput(), initial='MSC', max_length=128)
	# date = forms.DateTimeField()
	item = forms.ModelMultipleChoiceField(queryset=Testing_Activity.objects.all())
	comment = forms.CharField(widget=forms.Textarea, help_text="Please attach your specific requirment.", initial="PUR or CAS or PCS? \nSpecific Requirment start here")
	email = forms.EmailField(widget=forms.HiddenInput(),initial='x@bayer.com')
	status = forms.CharField(widget=forms.HiddenInput(), max_length=128, initial='Waiting List') # , help_text='Please indicate your present action: Processing or Tackled.')
	
	class Meta:
		model = TestingRequest

	fields = ('requester','responser' ,'item', 'email', 'comment','status')