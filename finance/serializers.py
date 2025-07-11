from rest_framework import serializers
from finance.models import Transaction, Budget
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import Value
from django.db.models import DecimalField


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ('category', 'limit')

    def validate_limit(self,value):
        if value <= 0:
            raise serializers.ValidationError('Budget limit can not be negative or zero')
        
        if value > 1000000:
            raise serializers.ValidationError('budget can not be higher than 1000000')  
        
        return value
    
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def validate(self, data):
        budget = data['budget_category']
        amount = data['amount']
        type1 = data['type']

        if type1 == 'Expense':
            total_expense = Transaction.objects.filter(budget_category=budget,type = 'Expense').aggregate(
                total=Coalesce(Sum('amount'), 
                               Value(0), 
                               output_field=DecimalField()))['total']
        
        if total_expense + amount > budget.limit:
            raise serializers.ValidationError({"message":"budget is less than expense"})
        
        return data

    def transaction_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Transaction Value can not be negative or zero')
        
        return value
    
   