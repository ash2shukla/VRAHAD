from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from fingerprint import views
from django.contrib import admin

urlpatterns = [
    url(r'^fingerprint/verify/(?P<fp>[a-zA-Z0-9@$!]{69})$', views.FingerprintVerify.as_view()),
    url(r'^fingerprint/$', views.FingerprintSave.as_view()),
    url(r'^SPOC/$', views.HCenterSPOCVerify.as_view()),
    url(r'^admin/', admin.site.urls),
]

urlpatterns = format_suffix_patterns(urlpatterns)
