from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from ASA import views as Aviews
from fingerprint import views as fviews
from django.contrib import admin

urlpatterns = [
    url(r'^fingerprint/verify/(?P<fp>[a-zA-Z0-9@$!]{69})$', fviews.FingerprintVerify.as_view()),
    url(r'^fingerprint/$', fviews.FingerprintSave.as_view()),
    url(r'^SPOC/$', fviews.HCenterSPOCVerify.as_view()),
	url(r'^forwardAuthReq/$',Aviews.ForwardAuthReq.as_view()),
	url(r'^forwardeKYCReq/$',Aviews.ForwardeKYCReq.as_view()),
	url(r'^getOTP/$',Aviews.GetOTP.as_view()),
    url(r'^admin/', admin.site.urls),
]

urlpatterns = format_suffix_patterns(urlpatterns)
