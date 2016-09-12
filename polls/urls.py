from django.conf.urls import include, url
from views import *


urlpatterns = [
    url(r'^vote/', vote),
    url(r'^results/', get_results),
    url(r'^testlength/', test_length)
    ]