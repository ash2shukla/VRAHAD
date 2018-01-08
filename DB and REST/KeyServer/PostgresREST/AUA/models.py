from django.db import models
from time import time

class LicenseKey(models.Model):
	lk = models.CharField(max_length=64)
	ts = models.CharField(max_length=20,default = str(int(time())))

	def __str__(self):
		return self.ts

######## Define Router ########

class LicenseKeyRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'AUA':
            return 'AUA'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'AUA':
            return 'AUA'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'AUA' or \
           obj2._meta.app_label == 'AUA':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'AUA':
            return db == 'AUA'
        return None
