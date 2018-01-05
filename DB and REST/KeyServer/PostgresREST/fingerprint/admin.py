from django.contrib import admin
from .models import Fingerprint, HCenterSPOC, HCenterEmployee, HealthCenter

admin.site.register(Fingerprint)
admin.site.register(HCenterSPOC)
admin.site.register(HealthCenter)
admin.site.register(HCenterEmployee)
