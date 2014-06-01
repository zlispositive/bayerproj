from django.contrib import admin
from ta.models import Business_Unit, Testing_Machine, Accessory, Chemical, Testing_Activity
# Register your models here.
class Business_UnitAdmin(admin.ModelAdmin):
	list_display = ('bu_name', 'bu_staff')
	list_filter = ('bu_name',)
	ordering = ('bu_name',)

class Testing_MachineAdmin(admin.ModelAdmin):
	list_display = ('owner', 'status', 'equipment_code', 'equipment_name', 'equipment_model')
	search_fields = ('owner', 'status', 'equipment_code', 'equipment_name', 'equipment_model')
	list_filter = ('owner', 'status','equipment_shared')
	ordering = ('owner', 'status','equipment_shared')

class Testing_ActivityAdmin(admin.ModelAdmin):
	list_display = ('bu', 'testing_name', 'testing_type', 'testing_material', 'outsourcing_partner')
	search_fields = ('bu', 'testing_name', 'testing_type', 'testing_material', 'outsourcing_partner')
	list_filter = ('bu', 'testing_type')
	ordering = ('bu', 'testing_type', 'machines', 'accessories', 'chemicals')
	filter_horizontal = ('machines', 'accessories', 'chemicals',)
	# raw_id_fields = ('bu',)


class AccessoryAdmin(admin.ModelAdmin):
	list_display = ('accessory_item', 'accessory_price', 'accessory_reusalbe')
	search_fields = ('accessory_item', 'accessory_price', 'accessory_reusalbe')
	list_filter = ('accessory_reusalbe',)
	ordering = ('accessory_item', 'accessory_price', 'accessory_reusalbe')


class ChemicalAdmin(admin.ModelAdmin):
	list_display = ('chem_item', 'chem_unit_cost')
	search_fields = ('chem_item', 'chem_unit_cost')
	# list_filter = ('',)
	ordering = ('chem_item', 'chem_unit_cost')

admin.site.register(Business_Unit, Business_UnitAdmin)
admin.site.register(Testing_Machine, Testing_MachineAdmin)
admin.site.register(Accessory, AccessoryAdmin)
admin.site.register(Chemical, ChemicalAdmin)
admin.site.register(Testing_Activity, Testing_ActivityAdmin)