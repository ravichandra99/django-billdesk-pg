from payments.views import payment_request,handleResponse
from django.urls import path


app_name = 'payments'


urlpatterns =[
	path('', payment_request, name='paymentpage'),
	path('s2sresp/', handleResponse, name='s2shandle'),
]