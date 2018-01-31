from django.contrib import admin
from django.urls import path
from VerifyEmployee import views as Vviews
from EnrollResident import views as Rviews

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', Vviews.index),
	path('OTP/<str:eid>/<str:tok>/',Vviews.OTP),
	path('Resident/<str:eid>/<str:tok>/',Rviews.index)
]
