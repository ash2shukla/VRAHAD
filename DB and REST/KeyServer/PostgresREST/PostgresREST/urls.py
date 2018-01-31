from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from ASA import views as Aviews
from HCenter import views as Hviews
from django.contrib import admin

urlpatterns = [
    url(r'^fingerprint/verify/(?P<fp>[a-zA-Z0-9@$!]{69})$', Hviews.FingerprintVerify.as_view()),
    url(r'^fingerprint/$', Hviews.FingerprintSave.as_view()),
    url(r'^SPOC/$', Hviews.HCenterSPOCVerify.as_view()),
	url(r'^EMP/$', Hviews.HCenterEmployeeVerify.as_view()),
	url(r'^EMPAuth/(?P<eid>[a-zA-Z0-9@$!_]+)/(?P<tok>[a-zA-Z0-9@$!]+)/$', Hviews.HCenterEmployeeAuth.as_view()),
	url(r'^forwardAuthReq/$',Aviews.ForwardAuthReq.as_view()),
	url(r'^forwardeKYCReq/$',Aviews.ForwardeKYCReq.as_view()),
	url(r'^forwardOTPReq/$',Aviews.ForwardOTPReq.as_view()),
    url(r'^admin/', admin.site.urls),
]

urlpatterns = format_suffix_patterns(urlpatterns)
