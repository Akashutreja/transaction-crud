from django.urls import path
from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^transaction/(?P<transaction_id>[0-9]+)/$', TransactionDetailsView.as_view()),
    path('sum/', TransactionChildAmountDetails.as_view()),
    url(r'^types/(?P<type_id>[0-9a-f-]+\w+)/$', TransactionTypeDetailView.as_view()),
]