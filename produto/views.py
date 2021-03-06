from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models


class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 12
    ordering = '-id'


class DetalheProdutos(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


class AdcionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(self.request, 'Erro ao adicionar o produto ao carrinho.')
            return redirect(http_referer)

        variacao = get_object_or_404(models.Variacao, id=variacao_id)

        if variacao.estoque < 1:
            messages.error(self.request, 'Estoque insuficiente.')
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = dict()
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            # TODO: Variação existe no carrinho
            pass
        else:
            carrinho[variacao_id] = {
                
            }

        return HttpResponse(f'{variacao.produto} {variacao.nome}')


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Remover do carrinho')


class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Carrinho')


class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')
