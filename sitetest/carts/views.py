from django.shortcuts import redirect, render
from django.views import View

# Create your views here.

class CartAddView(View):
    def post(self, request):
        return redirect(request, 'base.html')



class CartChangeView(View):
    def post(self, request):
        return redirect(request, 'base.html')



class CartRemoveView(View):
    def post(self, request):
        return redirect(request, 'base.html')