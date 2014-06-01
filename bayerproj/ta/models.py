from django.db import models				
# Create your models here.

class Business_Unit(models.Model):
	bu_name = models.CharField(max_length=5)
	bu_staff = models.CharField(max_length=50, blank=True, null=True)
	email = models.EmailField(verbose_name='e-mail', blank=True)
	

	def __unicode__(self):
		return u'%s %s' % (self.bu_name, self.bu_staff)

class Testing_Machine(models.Model):

	status = models.CharField(max_length=20)
	# owner = models.ForeignKey(Business_Unit)
	owner = models.CharField(max_length=3)
	equipment_code = models.CharField(max_length=20)
	equipment_name = models.CharField(max_length=40)
	equipment_model = models.CharField(max_length=40)
	equipment_amount = models.CharField(max_length=5)

	# equipment_shared = models.BooleanField()
	equipment_shared = models.CharField(max_length=5)

	capacity_theoretical = models.CharField(max_length=5)
	plained_downtime = models.CharField(max_length=5)
	plained_nonwork = models.CharField(max_length=5)
	capacity_practical = models.CharField(max_length=5)
	adjustment_ratio = models.CharField(max_length=5)				# max_digits=1, decimal_places=1
	capacity_normal = models.CharField(max_length=5)

	waiting_time = models.CharField(max_length=5)				# max_digits=3, decimal_places=1
	processing_time = models.CharField(max_length=5)				# max_digits=6, decimal_places=1

	

	def __unicode__(self):
		return u'Owner:%s Status:%s, Code:%s, Name:%s, Model:%s' % (self.owner, self.status, self.equipment_code, self.equipment_name, self.equipment_model)

class Accessory(models.Model):
	accessory_item = models.CharField(max_length=60)
	accessory_price = models.CharField(max_length=5)				# max_digits=3, decimal_places=1

	# accessory_reusalbe = models.BooleanField()
	accessory_reusalbe = models.CharField(max_length=3)

	def __unicode__(self):
		return u'%s ' % (self.accessory_item)

class Chemical(models.Model):
	chem_item = models.CharField(max_length=60)
	chem_unit_cost = models.CharField(max_length=5)				# max_digits=4, decimal_places=1

	def __unicode__(self):
		return u'%s ' % (self.chem_item)

class Testing_Activity(models.Model):
	bu = models.CharField(max_length=3)
	testing_type = models.CharField(max_length=5)
	testing_name = models.CharField(max_length=60)
	testing_material = models.CharField(max_length=20)
	testing_capability1 = models.CharField(max_length=10)
	testing_capability2 = models.CharField(max_length=10)

	time_ad = models.CharField(max_length=40)				# max_digits=6, decimal_places=2
	setuptime_machine = models.CharField(max_length=40)				# max_digits=6, decimal_places=2
	setuptime_labor = models.CharField(max_length=40)				# max_digits=3, decimal_places=2
	runtime_machine = models.CharField(max_length=40)				# max_digits=6, decimal_places=2
	runtime_labor = models.CharField(max_length=40)				# max_digits=4, decimal_places=2
	conditiontime = models.CharField(max_length=40)				# max_digits=6, decimal_places=2
	outsourcing_price = models.CharField(max_length=40)
	outsourcing_partner = models.CharField(max_length=40, blank=True, null=True)
	outsourcing_risk = models.CharField(max_length=40)				# max_digits=3, decimal_places=2
	outsourcing_cost = models.CharField(max_length=40)

	# time_ad = models.FloatField()				# max_digits=6, decimal_places=2
	# setuptime_machine = models.FloatField()				# max_digits=6, decimal_places=2
	# setuptime_labor = models.FloatField()				# max_digits=3, decimal_places=2
	# runtime_machine = models.FloatField()				# max_digits=6, decimal_places=2
	# runtime_labor = models.FloatField()				# max_digits=4, decimal_places=2
	# conditiontime = models.FloatField()				# max_digits=6, decimal_places=2
	# outsourcing_price = models.FloatField()
	# outsourcing_partner = models.CharField(max_length=50, blank=True, null=True)
	# outsourcing_risk = models.FloatField()				# max_digits=3, decimal_places=2
	# outsourcing_cost = models.FloatField()


	# bu = models.ForeignKey(Business_Unit)
	machines = models.ManyToManyField(Testing_Machine, blank=True)
	accessories = models.ManyToManyField(Accessory, blank=True)
	chemicals = models.ManyToManyField(Chemical, blank=True)

	
	# machines = models.CharField(max_length=50, blank=True)
	# accessories = models.CharField(max_length=30, blank=True)
	# chemicals = models.CharField(max_length=50, blank=True)

	def __unicode__(self):
		return u'%s: %s' % (self.bu ,self.testing_name)

