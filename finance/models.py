from django.db import models

# Create your models here.
class Budget(models.Model):
    category = models.CharField(max_length=100)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.category

class Transaction(models.Model):
    TYPE_CHOICES = (('Income', 'Income'), ('Expense', 'Expense'))
    type = models.CharField(max_length=25, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    budget_category = models.ForeignKey(Budget, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.type} - {self.amount}"