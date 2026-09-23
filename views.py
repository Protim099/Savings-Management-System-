from decimal import Decimal
from datetime import datetime
import secrets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *
from .auth import authenticate, tokens_for_user, hash_password
from .permissions import RolePermission
from .serializers import user_data, account_data, plan_data, transaction_data

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user = authenticate(request.data.get("email",""), request.data.get("password",""))
        if not user:
            return Response({"detail":"Invalid credentials"}, status=401)
        return Response({"tokens": tokens_for_user(user), "user": user_data(user)})

class MeView(APIView):
    def get(self, request):
        u = User.objects.get(id=request.auth["user_id"])
        return Response(user_data(u))

class DashboardView(APIView):
    def get(self, request):
        role = request.auth.get("role")
        accounts = Account.objects
        if role == "CUSTOMER":
            accounts = accounts(customer=request.auth["user_id"])
        total = sum((a.balance for a in accounts), Decimal("0"))
        deposits = sum((x.amount for x in Deposit.objects(status="APPROVED")), Decimal("0"))
        withdrawals = sum((x.amount for x in Withdrawal.objects(status="APPROVED")), Decimal("0"))
        return Response({
            "role": role, "total_savings": str(total),
            "total_deposits": str(deposits), "total_withdrawals": str(withdrawals),
            "total_customers": User.objects(role="CUSTOMER").count(),
            "recent_transactions": [transaction_data(x) for x in Transaction.objects.order_by("-created_at")[:8]]
        })

class PlanListView(APIView):
    def get(self, request):
        return Response([plan_data(x) for x in SavingsPlan.objects(is_active=True)])
    def post(self, request):
        if request.auth.get("role") not in ("ADMIN","STAFF"):
            return Response({"detail":"Forbidden"}, status=403)
        p = SavingsPlan(**request.data).save()
        return Response(plan_data(p), status=201)

class AccountListView(APIView):
    def get(self, request):
        qs = Account.objects
        if request.auth.get("role") == "CUSTOMER":
            qs = qs(customer=request.auth["user_id"])
        return Response([account_data(x) for x in qs])
    def post(self, request):
        if request.auth.get("role") not in ("ADMIN","STAFF"):
            return Response({"detail":"Forbidden"}, status=403)
        customer = User.objects.get(id=request.data["customer_id"])
        plan = SavingsPlan.objects.get(id=request.data["plan_id"])
        a = Account(customer=customer, plan=plan, account_number="SA-"+secrets.token_hex(5).upper(),
                    interest_rate=plan.interest_rate).save()
        AuditLog(user=customer, action="ACCOUNT_CREATED", entity="Account", entity_id=str(a.id)).save()
        return Response(account_data(a), status=201)

class DepositView(APIView):
    def post(self, request):
        a = Account.objects.get(id=request.data["account_id"])
        if request.auth.get("role") == "CUSTOMER" and str(a.customer.id) != request.auth["user_id"]:
            return Response({"detail":"Forbidden"}, status=403)
        d = Deposit(account=a, amount=Decimal(str(request.data["amount"])),
                    payment_method=request.data.get("payment_method","CASH"),
                    transaction_id=request.data.get("transaction_id")).save()
        Notification(user=a.customer, title="Deposit submitted",
                     message=f"Deposit {d.amount} is pending approval.").save()
        return Response({"id":str(d.id),"status":d.status}, status=201)

class WithdrawalView(APIView):
    def post(self, request):
        a = Account.objects.get(id=request.data["account_id"])
        if str(a.customer.id) != request.auth["user_id"]:
            return Response({"detail":"Forbidden"}, status=403)
        amount = Decimal(str(request.data["amount"]))
        if amount <= 0 or a.balance < amount:
            return Response({"detail":"Insufficient balance"}, status=400)
        w = Withdrawal(account=a, amount=amount, method=request.data.get("method","BANK")).save()
        Notification(user=a.customer, title="Withdrawal submitted",
                     message=f"Withdrawal {amount} is pending approval.").save()
        return Response({"id":str(w.id),"status":w.status}, status=201)

class PendingDepositsView(APIView):
    def get(self, request):
        if request.auth.get("role") not in ("ADMIN","STAFF"):
            return Response({"detail":"Forbidden"}, status=403)
        return Response([{"id":str(d.id),"account":d.account.account_number,"amount":str(d.amount),
                         "status":d.status,"created_at":d.created_at.isoformat()} for d in Deposit.objects(status="PENDING")])

class ApproveDepositView(APIView):
    def post(self, request, pk):
        if request.auth.get("role") not in ("ADMIN","STAFF"):
            return Response({"detail":"Forbidden"}, status=403)
        d = Deposit.objects.get(id=pk)
        if d.status != "PENDING":
            return Response({"detail":"Already processed"}, status=400)
        d.status = "APPROVED"; d.approved_at = datetime.utcnow(); d.save()
        d.account.balance = d.account.balance + d.amount; d.account.save()
        Transaction(account=d.account, transaction_type="DEPOSIT", amount=d.amount,
                    reference=d.transaction_id, description="Approved deposit").save()
        Notification(user=d.account.customer, title="Deposit approved",
                     message=f"Deposit {d.amount} was credited.").save()
        return Response({"status":"APPROVED"})

class TransactionListView(APIView):
    def get(self, request):
        qs = Transaction.objects
        if request.auth.get("role") == "CUSTOMER":
            ids = [a.id for a in Account.objects(customer=request.auth["user_id"])]
            qs = qs(account__in=ids)
        return Response([transaction_data(x) for x in qs.order_by("-created_at")])
