from django.contrib import admin
from .models import Fingerprint, HCenterSPOC, HCenterEmployee, HealthCenter, GIDMap, RecordMaps

class MultiDBModelAdmin(admin.ModelAdmin):
    using = 'keydb'

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def queryset(self, request):
        return super(MultiDBModelAdmin, self).queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)

class HealthCenterAdmin(MultiDBModelAdmin):
	model = HealthCenter

class HCenterEmployeeAdmin(MultiDBModelAdmin):
	model = HCenterEmployee

class FingerprintAdmin(MultiDBModelAdmin):
	model = Fingerprint

class HCenterSPOCAdmin(MultiDBModelAdmin):
	model = HCenterSPOC

class GIDMapAdmin(MultiDBModelAdmin):
    model = GIDMap

class RecordMapsAdmin(MultiDBModelAdmin):
    model = RecordMaps

admin.site.register(Fingerprint,FingerprintAdmin)
admin.site.register(HCenterSPOC,HCenterSPOCAdmin)
admin.site.register(HealthCenter,HealthCenterAdmin)
admin.site.register(HCenterEmployee,HCenterEmployeeAdmin)
admin.site.register(GIDMap,GIDMapAdmin)
admin.site.register(RecordMaps,RecordMapsAdmin)
