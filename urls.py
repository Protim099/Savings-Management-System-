from django.urls import path
from .views import (
    MeView, DashboardView, PlanListView, AccountListView, DepositView,
    WithdrawalView, PendingDepositsView, ApproveDepositView, TransactionListView
)
urlpatterns = [
    path("me/", MeView.as_view()),
    path("dashboard/", DashboardView.as_view()),
    path("plans/", PlanListView.as_view()),
    path("accounts/", AccountListView.as_view()),
    path("deposits/", DepositView.as_view()),
    path("deposits/pending/", PendingDepositsView.as_view()),
    path("deposits/<str:pk>/approve/", ApproveDepositView.as_view()),
    path("withdrawals/", WithdrawalView.as_view()),
    path("transactions/", TransactionListView.as_view()),
]
