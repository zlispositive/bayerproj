from django.contrib import admin
from accounts.models import UserProfile
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
	# list_display = ( 'title', 'rank')
	# list_filter =  ( 'title', 'rank')
	ordering = ('rank',)

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'bu' ,'title', 'rank')
	list_filter = ('title', 'rank')
	ordering = ('rank',)

# admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
