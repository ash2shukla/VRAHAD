from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from fingerprint import views as fviews
from AUA import views as Aviews
from django.contrib import admin

urlpatterns = [
    url(r'^fingerprint/verify/(?P<fp>[a-zA-Z0-9@$!]{69})$', fviews.FingerprintVerify.as_view()),
    url(r'^fingerprint/$', fviews.FingerprintSave.as_view()),
    url(r'^SPOC/$', fviews.HCenterSPOCVerify.as_view()),
	url(r'^getKey/(?P<asaID>[a-zA-Z0-9_]+)$', Aviews.getKey.as_view()),
	url(r'^getSession/(?P<asaID>[a-zA-Z0-9_]+)$',Aviews.getSession.as_view()),
    url(r'^admin/', admin.site.urls),
]

urlpatterns = format_suffix_patterns(urlpatterns)
