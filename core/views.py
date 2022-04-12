import django.utils.timezone
from django.shortcuts import render
from django.template import loader
from .pytomate import enviar_email
from .form import FormularioLogin, LoginCatchForm, FormularioSingup
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from .pylo7 import VendasDeSucesso
import httpagentparser
import requests
import ast
from ipware import get_client_ip


class index(View):
    template_name = "index.html"

    def get(self, request):
        info_lvl1 = {}
        agent = request.META["HTTP_USER_AGENT"]
        info_lvl1['so'] = httpagentparser.detect(agent)["os"]
        so = info_lvl1['so']
        try:
            ip_address, is_routable = get_client_ip(request)

            auth = '8eaf1e5d-df69-4671-b5e4-58426c165d97'
            url = 'https://ipfind.co/?auth=' + auth + '&ip=' + ip_address
            response = requests.request('GET', url)
            conteudo = ast.literal_eval(response.content.decode('UTF-8').replace('"', "'").replace('null', "'null'"))

            info_lvl1['País'] = conteudo['country']
            info_lvl1['Estado'] = conteudo['region']
            info_lvl1['Cidade'] = conteudo['city']
            info_lvl1['País'] = conteudo['country']
            info_lvl1['Latitude'] = conteudo['latitude']
            info_lvl1['Longitude'] = conteudo['longitude']

            texto = "Novo acesso ao seu portifólio amo! Informações retidas: \n" + str(info_lvl1)
            enviar_email("danrley2109@gmail.com", "danrley2109@gmail.com", texto, "Novo acesso ao seu portfólio")

        except:
            pass

        context = {}
        context['imagem'] = {}
        if so['name'] != 'Windows':

            context['imagem']['tamanho'] = 'small'
            return render(request, "index.html", context)
        else:
            context['imagem']['tamanho'] = 'big'
            print('renderizou aq', context)
            return render(request, "index.html", context)

    def post(self, request):
        agent = request.META["HTTP_USER_AGENT"]
        s = httpagentparser.detect(agent)["os"]

        if request.POST['quantidade_produtos'] == "":
            qte_produtos = 0
        else:
            qte_produtos = request.POST['quantidade_produtos']

        if 1 <= int(request.POST['quantidade_produtos']) <= 1200:
            prod = VendasDeSucesso(request.POST['termo_interesse'], int(qte_produtos))
            estatisticas = prod.info_gerais()
            media_primeiros10 = prod.media_primeiros_10()
            numero_paginas = prod.numero_paginas()

            produto = {'infos': {'nome': request.POST['termo_interesse'], 'n_pag_vasculhadas': numero_paginas, 'media_primeiros10': media_primeiros10['price'], 'total': estatisticas['count'], 'media': estatisticas['mean'], 'minimo': estatisticas['min'] ,
                                 'maximo': estatisticas['max']}, 'user': {'s.o': s['name']}}

        else:
            produto = {'infos': {'nome': request.POST['termo_interesse'], 'n_pag_vasculhadas': 'proibido',
                                 'media_primeiros10': '', 'total': '',
                                 'media': '', 'minimo': '',
                                 'maximo': '', 'user': {'s.o': s['name']}}}

        return JsonResponse(produto)


class loginz(View):
    template_name = "loginz.html"

    def get(self, request):
        context = {}
        form = FormularioLogin()
        context['form'] = form
        return render(request, "loginz.html", context)

    def post(self, request):
        autenticado = autenticacao(request)
        if autenticado is not None:
            return render(request, "logado.html")
        else:
            return render(request, "index.html")


def logado(request):
    if request.method == 'POST':
        print(request.body)


def autenticacao(requisicao):
    auth = {}
    auth['email'] = requisicao.POST['email']
    auth['senha'] = requisicao.POST['senha']
    user = User.objects.filter(email=auth['email'])
    username = user.values_list('username')[0][0]
    autenticado = authenticate(username=username, password=auth['senha'])
    return autenticado


class singup(View):
    form = FormularioSingup()
    context = {}
    context['form'] = form

    def get(self, request):
        return render(request, "singup.html")

    def post(self, request):
        user = authenticate(user=request.POST['usuario'])
        print(user)
        if user != None:
            print("usuário já cadastrado")
        else:
            qte_usuarios = len(User.objects.all())+1
            novo_usuario = User(id=qte_usuarios, password='', last_login=django.utils.timezone.now(), is_superuser=0,username=request.POST['usuario'],
                                last_name=request.POST['sobrenome'], email=request.POST['email'], is_staff=1, is_active=1, date_joined=django.utils.timezone.now(),
                                first_name=request.POST['nome'])

            novo_usuario.save()
            novo_usuario.set_password(request.POST['senha'])
            novo_usuario.save()

        return render(request, "index.html")


def capta_login(request):
    form = LoginCatchForm(request)
    return form



def error404(request, ex):
    template = loader.get_template('error404.html')
    return HttpResponse(content=template.render(), content_type='text/html; charset=utf8', status=404)