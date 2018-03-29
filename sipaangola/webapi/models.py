# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse


# Aréa de criação dos modelos
#Orgãos - Ex: Ministério do Comércio
class orgao(models.Model):
    cod_orgao=models.IntegerField(unique=True, verbose_name='Código')
    descricao=models.CharField(max_length=100,unique=True, verbose_name='Descrição')
    sigla=models.CharField(max_length=20, verbose_name='SIGLA')
    site=models.CharField(max_length=20,verbose_name='Site', default='www.sipa.co.ao')
    estado=models.BooleanField(default=True, verbose_name='Activado')
    data_registo=models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name='Orgão'

    def __unicode__(self): #unicode para aceittar o encondig: utf8 para os acentos do português.
        return self.descricao

# Categórias - Ex: Loja de Registo | Conservatória | Posto de Identificação
class categoria(models.Model):
    cod_categoria = models.IntegerField(unique=True, verbose_name='Código')
    descricao = models.CharField(max_length=100, unique=True, verbose_name='Descrição')
    estado = models.BooleanField(default=True, verbose_name='Activado')
    data_registo = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name='Catégoria'

    def __unicode__(self):
        return self.descricao


class servico(models.Model):
     cod_servico = models.IntegerField(unique=True, verbose_name='Código')
     descricao = models.CharField(max_length=100, unique=True, verbose_name='Descrição')
     estado = models.BooleanField(default=True, verbose_name='Activado')
     data_registo = models.DateTimeField(auto_now=True, null=True, blank=True)

     class Meta:
         verbose_name='Serviço'

     def __unicode__(self):
         return self.descricao

class diasuteis(models.Model):
         DIA_CHOICES = (
             (u'segunda-feira', 'Segunda-Feira'),
             (u'terça-feira', 'Terça-Feira'),
             (u'quarta-feira', 'Quarta-Feira'),
             (u'quinta-feira', 'Quinta-Feira'),
             (u'sexta-feira', 'Sexta-Feira'),
         )
         servico = models.ForeignKey(servico, related_name='servico', on_delete=models.CASCADE)
         dia = models.CharField(max_length=20, choices=DIA_CHOICES)
         horainicio = models.TimeField(u'Hora Ínicial', help_text=u'Hora Ínicial')
         horafinal = models.TimeField(u'Hora Final', help_text=u'Hora Final')

         class Meta:
             verbose_name = 'Dias Utéis'
             verbose_name_plural = 'Dias Utéis'

         def __unicode__(self):
             return '(%s) %s: de %s à %s' % (self.servico, self.dia, self.horainicio, self.horafinal)


#Postos - Ex: Posto de Identificação do Rangel
class posto(models.Model):
    cod_posto=models.IntegerField(unique=True, verbose_name='Código')
    descricao=models.CharField(max_length=100, unique=True, verbose_name='Descrição')
    nif=models.CharField(max_length=15, unique=True, verbose_name='Número de Idenficação Fiscal')
    tel=models.CharField(max_length=20, verbose_name='Telefone')
    email=models.EmailField(default='info@sipa.co.ao', verbose_name='E-mail')
    endereco=models.CharField(max_length=50, verbose_name='Endereço')
    estado=models.BooleanField(default=True, verbose_name='Activado')
    data_registo=models.DateTimeField(auto_now=True, null=True, blank=True)
    orgao=models.ForeignKey(orgao, related_name='orgao', on_delete=models.CASCADE, verbose_name='Orgão')
    categoria=models.ForeignKey(categoria, related_name='categoria', on_delete=models.CASCADE)
    servicos=models.ManyToManyField(servico, verbose_name='Serviços Prestados')
    diasuteis = models.ManyToManyField(diasuteis, verbose_name='Dias Utéis')

    class Meta:
        unique_together = ('orgao', 'descricao', 'categoria')
        ordering = ['descricao']

    def __unicode__(self):
        return '%s' % (self.descricao)


#Cidadao - Ex: Adilson Pedro
class cidadao(models.Model):
    nome=models.CharField(max_length=50, verbose_name='Nome')
    sobrenome=models.CharField(max_length=50, verbose_name='Sobrenome')
    numerobi=models.CharField(max_length=14, verbose_name='Nº Bilhete de Identidade')
    tel=models.CharField(max_length=20, verbose_name='Telefone')
    email=models.EmailField(default='eu@exemplo.com', verbose_name='E-mail')
    endereco=models.CharField(max_length=50, verbose_name='Morada')
    estado=models.BooleanField(default=True, verbose_name='Activado')
    data_registo=models.DateTimeField(auto_now=True, null=True)
    utilizador = models.OneToOneField(User)

    class Meta:
        verbose_name='Cidadão'

    def __unicode__(self):
        return '%s, %s' % (self.nome, self.sobrenome)


class agente(models.Model):
    nome=models.CharField(max_length=50, verbose_name='Nome')
    sobrenome=models.CharField(max_length=50, verbose_name='Sobrenome')
    tel=models.CharField(max_length=20, verbose_name='Telefone')
    email=models.EmailField(default='eu@exemplo.com', verbose_name='E-mail')
    endereco=models.CharField(max_length=50, verbose_name='Morada')
    estado=models.BooleanField(default=True, verbose_name='Activado')
    data_registo=models.DateTimeField(auto_now=True, null=True)
    utilizador = models.OneToOneField(User)
    posto = models.ForeignKey(posto, related_name='posto', on_delete=models.CASCADE)

    class Meta:
        verbose_name='Agente'

    def __unicode__(self):
        return '%s, %s' % (self.nome, self.sobrenome)

#Tudo sobre agendamento
class Event(models.Model):
    day = models.DateField(u'Dia do Atendimento', help_text=u'Dia do Atendimento')
    start_time = models.TimeField(u'Hora de Ínicio', help_text=u'Hora de Ínicio')
    end_time = models.TimeField(u'Hora Final', help_text=u'Hora Final')
    notes = models.TextField(u'Notas', help_text=u'Coloque uma nota se for necessário', blank=True, null=True)

    class Meta:
        verbose_name = u'Marcação'
        verbose_name_plural = u'Marcações'

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:    #edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end): #innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end: #outter limits
            overlap = True

        return overlap

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, str(self.start_time))

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('Hora Final deve ser após a Hora de Ínicio')

        events = Event.objects.filter(day=self.day)
        if events.exists():
            for event in events:
                if self.check_overlap(event.start_time, event.end_time, self.start_time, self.end_time):
                    raise ValidationError(
                        'Já existe um agendamento neste período: ' + str(event.day) + ', ' + str(
                            event.start_time) + '-' + str(event.end_time))

    def __unicode__(self):
        return '%s de %s à %s' % (self.day,self.start_time, self.end_time)


class agendamento(models.Model):
    ESTADO_CHOICES = (
             (u'aberto', 'Aberto'),
             (u'em atendimento', 'Em Atendimento'),
             (u'em espera', 'Em Espera'),
             (u'atendido', 'Atendido'),
             (u'cancelado', 'Cancelado'),
         )

    utilizador = models.OneToOneField(User)
    posto = models.ForeignKey(posto, related_name='postos', on_delete=models.CASCADE)
    diasuteis = models.ManyToManyField(diasuteis, verbose_name='Serviços e Dias Utéis')
    agenda = models.OneToOneField(Event, verbose_name='Marcação')
    estado = models.CharField(max_length=20, verbose_name='Estado do Pedido', default='Aberto', choices=ESTADO_CHOICES)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __unicode__(self):
        return '%s | %s | %s (%s)' % (self.utilizador, self.posto, self.agenda, self.estado)