from django.urls import path, include
from rest_framework import routers
from finance.views import BudgetViewSet, TransactionViewSet
from rest_framework_nested import routers



router = routers.DefaultRouter()
router.register('budgets', BudgetViewSet)

budgets_router = routers.NestedDefaultRouter(
    router,
    'budgets',
    lookup='budget'
)

budgets_router.register('transactions', TransactionViewSet, basename='budget-transactions')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(budgets_router.urls)),

]