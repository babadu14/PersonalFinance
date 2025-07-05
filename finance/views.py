from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from finance.serializers import BudgetSerializer, TransactionSerializer
from finance.models import Budget, Transaction


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        budget_pk = self.kwargs['budget_pk']
        user = self.request.user
        return Transaction.objects.filter(
            budget_category_id=budget_pk,
            budget_category__user=user)
    
    def perform_create(self, serializer):
        budget = Budget.objects.get(pk=self.kwargs['budget_pk'])
        return serializer.save(budget_category=budget)