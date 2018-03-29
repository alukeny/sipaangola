# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import orgao, categoria, posto, servico, cidadao, agente, diasuteis, agendamento, Event
from .serializers import orgaoSerializer, categoriaSerializer, postoSerializer, servicoSerializer, cidadaoSerializer, agenteSerializer, diasuteisSerializer, agendamentoSerializer, marcacaoSerializer
from django.http import Http404
from rest_framework.decorators import api_view
from allauth.account.views import *
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

# Area de criação de views

#Metodo que retorna a view home, para a página principal


class JointLoginSignupView(LoginView):
    form_class = LoginForm
    signup_form = SignupForm

    def __init__(self, **kwargs):
        super(JointLoginSignupView, self).__init__(*kwargs)

    def get_context_data(self, **kwargs):
        ret = super(JointLoginSignupView, self).get_context_data(**kwargs)
        ret['signupform'] = get_form_class(app_settings.FORMS, 'signup', self.signup_form)
        return ret


login = JointLoginSignupView.as_view()
def home(request):
    context = locals()
    template = 'home.html'
    return  render(request, template, context)


#View para listar orgãos
class orgaoLista(APIView):
    """
    Fornece a lista de todos os orgãos e da a possibilidade de criar um novo.
    """
    def get(self, request, format=None):
        dados = orgao.objects.all()
        serializer = orgaoSerializer(dados, many=True)
        authentication_classes = [SessionAuthentication]
        permission_classes = (IsAuthenticated,)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = orgaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#View para exibir o orgão em função do primary key e outras operações - update e delete.
class orgaoDetalhes(APIView):
    """
    Fornece opções de consultar por pk, actualizar e deletar.
    """
    def get_object(self, pk):
        try:
            return orgao.objects.get(pk=pk)
        except orgao.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = orgaoSerializer(dados)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = orgaoSerializer(dados, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dados = self.get_object(pk)
        dados.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#View para listar categorias
class categoriaLista(APIView):

    def get(self, request, format=None):
        dados = categoria.objects.all()
        serializer = categoriaSerializer(dados, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = categoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#View para exibir a categoria em função do primary key e outras operações - update e delete.
class categoriaDetalhes(APIView):
    """
    Fornece opções de consultar por pk, actualizar e deletar.
    """
    def get_object(self, pk):
        try:
            return categoria.objects.get(pk=pk)
        except categoria.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = categoriaSerializer(dados)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = categoriaSerializer(dados, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dados = self.get_object(pk)
        dados.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#View para listar postos
class postoLista(APIView):
    def get(self, request, format=None):
        dados = posto.objects.all()
        serializer = postoSerializer(dados, many=True)
        return  Response(serializer.data)

    def post(self, request, format=None):
        serializer = postoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#View para exibir o posto em função do primary key e outras operações - update e delete.
class postoDetalhes(APIView):
    """
    Fornece opções de consultar por pk, actualizar e deletar.
    """
    def get_object(self, pk):
        try:
            return posto.objects.get(pk=pk)
        except posto.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = postoSerializer(dados)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = postoSerializer(dados, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dados = self.get_object(pk)
        dados.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# View para listar serviços
class servicoLista(APIView):

    def get(self, request, format=None):
        dados = servico.objects.all()
        serializer = servicoSerializer(dados, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = servicoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#View para exibir o serviço em função do primary key e outras operações - update e delete.
class servicoDetalhes(APIView):
    """
    Fornece opções de consultar por pk, actualizar e deletar.
    """
    def get_object(self, pk):
        try:
            return servico.objects.get(pk=pk)
        except servico.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = servicoSerializer(dados)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = servicoSerializer(dados, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dados = self.get_object(pk)
        dados.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# View para listar os cidadãos
class cidadaoLista(APIView):

    def get(self, request, format=None):
        dados = cidadao.objects.all()
        serializer = cidadaoSerializer(dados, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = cidadaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class cidadaoDetalhes(APIView):
    """
    Fornece opções de consultar por pk, actualizar e deletar.
    """
    def get_object(self, pk):
        try:
            return cidadao.objects.get(pk=pk)
        except cidadao.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = cidadaoSerializer(dados)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = cidadaoSerializer(dados, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dados = self.get_object(pk)
        dados.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# View para listar os agentes
class agenteLista(APIView):

    def get(self, request, format=None):
        dados = agente.objects.all()
        serializer = agenteSerializer(dados, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = agenteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class agenteDetalhes(APIView):
    """
    Fornece opções de consultar por pk, actualizar e deletar.
    """
    def get_object(self, pk):
        try:
            return agente.objects.get(pk=pk)
        except agente.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = agenteSerializer(dados)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = agenteSerializer(dados, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dados = self.get_object(pk)
        dados.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# View para listar os dias uteis
class diasuteisLista(APIView):

    def get(self, request, format=None):
        dados = diasuteis.objects.all()
        serializer = diasuteisSerializer(dados, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = diasuteisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class diasuteisDetalhes(APIView):
    """
    Fornece opções de consultar por pk, actualizar e deletar.
    """
    def get_object(self, pk):
        try:
            return diasuteis.objects.get(pk=pk)
        except diasuteis.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = diasuteisSerializer(dados)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = diasuteisSerializer(dados, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dados = self.get_object(pk)
        dados.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # View para listar os agendamentos
class agendamentoLista(APIView):

    def get(self, request, format=None):
        dados = agendamento.objects.all()
        serializer = agendamentoSerializer(dados, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = agendamentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class agendamentoDetalhes(APIView):
    """
    Fornece opções de consultar por pk, actualizar e deletar.
    """
    def get_object(self, pk):
        try:
            return agendamento.objects.get(pk=pk)
        except agendamento.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = agendamentoSerializer(dados)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = agendamentoSerializer(dados, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dados = self.get_object(pk)
        dados.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # View para listar as marcações
class marcacaoLista(APIView):

    def get(self, request, format=None):
        dados = Event.objects.all()
        serializer = marcacaoSerializer(dados, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = marcacaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class marcacaoDetalhes(APIView):
    """
    Fornece opções de consultar por pk, actualizar e deletar.
    """
    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = marcacaoSerializer(dados)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        dados = self.get_object(pk)
        serializer = marcacaoSerializer(dados, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dados = self.get_object(pk)
        dados.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)