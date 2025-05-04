from django.contrib import admin
from finance.models import Budget, Transaction
# Register your models here.

class TrasnsactionInline(admin.StackedInline):
    model = Transaction
    extra = 1

class BudgetAdmin(admin.ModelAdmin):
    model = Budget
    list_display = ['id', 'category', 'limit']
    search_fields = ['category']
    inlines = [TrasnsactionInline]

class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ['amount', 'budget_category', 'date']

admin.site.register(Budget, BudgetAdmin)
admin.site.register(Transaction, TransactionAdmin)
