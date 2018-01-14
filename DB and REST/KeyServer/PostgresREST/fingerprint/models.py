from django.db import models
from django.contrib.postgres.fields import JSONField

class HealthCenter(models.Model):
	HealthCenterID = models.CharField(max_length=100,primary_key=True)
	Data = JSONField(default={'asa_sign':False})

	def __str__(self):
		return self.HealthCenterID

class HCenterSPOC(models.Model):
	SPOCID = models.CharField(max_length=100,primary_key=True)
	passhash = models.CharField(max_length=100,null=False,blank=False)
	HealthCenter = models.ForeignKey(HealthCenter, on_delete = models.CASCADE, \
									null=True, blank = False)
	Data = JSONField(default={})

	def __str__(self):
		return self.SPOCID

class Fingerprint(models.Model):
	SPOCID = models.ForeignKey(HCenterSPOC, on_delete = models.CASCADE,\
								null=True, blank=False)
	fingerprint = models.CharField(max_length=100, null=False, blank=False)
	Data = JSONField(default={})

	def __str__(self):
		return self.SPOCID.HealthCenter.HealthCenterID

class HCenterEmployee(models.Model):
	EmployeeID = models.CharField(max_length=100,primary_key=True)
	HCenterSPOC = models.ForeignKey(HCenterSPOC, on_delete = models.CASCADE,\
									null=True, blank = False)
	Data = JSONField(default={})

	def __str__(self):
		return self.EmployeeID


###### Define Router ######

class HealthCenterRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'fingerprint':
            return 'keydb'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'fingerprint':
            return 'keydb'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'fingerprint' or \
           obj2._meta.app_label == 'fingerprint':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'AUA':
            return db == 'keydb'
        return None
