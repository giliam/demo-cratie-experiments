from django.conf.urls import include, url
from views import *


urlpatterns = [
    url(r'^vote/display/(\d+)/(\d+)', display_vote, name="display_vote"),
    url(r'^list/', display_polls),
    url(r'^vote/', vote),
    url(r'^results/', get_results),
    url(r'^testlength/', test_length)
    ]