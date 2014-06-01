from django.contrib import admin
from tr.models import TestingRequest

class TestingRequestAdmin(admin.ModelAdmin):
	list_display = ('id' ,'requester', 'responser' ,'date', 'date_action','status')
	list_filter = ( 'requester' , 'responser' ,'date', 'status' )
	search_fields = ('requester', 'date','item', 'date_action')
	ordering = ('date',)
	filter_horizontal = ('item',)

admin.site.register(TestingRequest, TestingRequestAdmin)


# Register your models here.
