from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from finance.serializers import BudgetSerializer, TransactionSerializer
from finance.models import Budget, Transaction
# Create your views here.

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(budget_category_id=self.kwargs['budget_pk'])
    
    def perform_create(self, serializer):
        budget = Budget.objects.get(pk=self.kwargs['budget_pk'])
        return serializer.save(budget_category=budget)