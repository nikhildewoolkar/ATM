from django.conf.urls import url

from atmweb.consumers import AtmConsumer

websocket_urlpatterns = [
    url(r'^ws/turnon/(?P<atm_code>\w+)/$', AtmConsumer.as_asgi()),
]