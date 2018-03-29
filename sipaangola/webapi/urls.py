from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^orgao/$', views.orgaoLista.as_view()),
    url(r'^orgao/(?P<pk>[0-9]+)$', views.orgaoDetalhes.as_view()),
    url(r'^categoria/$', views.categoriaLista.as_view()),
    url(r'^categoria/(?P<pk>[0-9]+)$', views.categoriaDetalhes.as_view()),
    url(r'^posto/$', views.postoLista.as_view()),
    url(r'^posto/(?P<pk>[0-9]+)$', views.postoDetalhes.as_view()),
    url(r'^servico/$', views.servicoLista.as_view()),
    url(r'^servico/(?P<pk>[0-9]+)$', views.servicoDetalhes.as_view()),
    url(r'^cidadao/$', views.cidadaoLista.as_view()),
    url(r'^cidadao/(?P<pk>[0-9]+)$', views.cidadaoDetalhes.as_view()),
    url(r'^agente/$', views.agenteLista.as_view()),
    url(r'^agente/(?P<pk>[0-9]+)$', views.agenteDetalhes.as_view()),
    url(r'^diasuteis/$', views.diasuteisLista.as_view()),
    url(r'^diasuteis/(?P<pk>[0-9]+)$', views.diasuteisDetalhes.as_view()),
    url(r'^agendamento/$', views.agendamentoLista.as_view()),
    url(r'^agendamento/(?P<pk>[0-9]+)$', views.agendamentoDetalhes.as_view()),
    url(r'^marcacao/$', views.marcacaoLista.as_view()),
    url(r'^marcacao/(?P<pk>[0-9]+)$', views.marcacaoDetalhes.as_view()),
]

