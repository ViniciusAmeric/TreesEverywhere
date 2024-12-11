from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import PlantedTree, Account
from .forms import PlantedTreeForm

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PlantedTreeSerializer


class UserPlantedTreesView(LoginRequiredMixin, ListView):
    model = PlantedTree
    template_name = "user_planted_trees.html"
    context_object_name = "planted_trees"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id  # Get user ID directly
        
        user_accounts = Account.objects.filter(users__id=user_id) 

        account_id = self.request.GET.get('account_id')
        if account_id:
            account = Account.objects.get(id=account_id)
            account_trees = PlantedTree.objects.filter(account=account)  
            context['account_trees'] = account_trees
        
        context['user_accounts'] = user_accounts  # Pass user accounts to context
        return context

    def get_queryset(self):
        return PlantedTree.objects.filter(user_id=self.request.user.id) 


class PlantedTreeDetailView(LoginRequiredMixin, DetailView):
    model = PlantedTree
    template_name = "planted_tree_detail.html"
    context_object_name = "planted_tree"

    def get_queryset(self):
        user_id = self.request.user.id 
        if not user_id:
            raise ValueError("User not authenticated trying to access tree details.")
        return PlantedTree.objects.filter(user_id=user_id)


class AddPlantedTreeView(LoginRequiredMixin, CreateView):
    model = PlantedTree
    form_class = PlantedTreeForm
    template_name = "add_planted_tree.html"
    success_url = reverse_lazy("user_planted_trees")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id 
        return super().form_valid(form)


class AccountPlantedTreesView(LoginRequiredMixin, ListView):
    model = PlantedTree
    template_name = "account_planted_trees.html"
    context_object_name = "planted_trees"

    def get_queryset(self):
        user_accounts = Account.objects.filter(users__id=self.request.user.id)  # Get user accounts
        return PlantedTree.objects.filter(account__in=user_accounts, user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_accounts'] = Account.objects.filter(users__id=self.request.user.id)  # Include user accounts in context
        return context


class UserPlantedTreesViewAPI(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this API

    def get(self, request):
        planted_trees = PlantedTree.objects.filter(user_id=request.user.id)
        serializer = PlantedTreeSerializer(planted_trees, many=True)  
        return Response(serializer.data) 
