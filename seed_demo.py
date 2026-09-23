from django.core.management.base import BaseCommand
from core.models import User, SavingsPlan, Account
from core.auth import hash_password
from decimal import Decimal

class Command(BaseCommand):
    help = "Create demo users, plans and accounts"

    def handle(self, *args, **kwargs):
        users = [
            ("admin@example.com","Admin User","ADMIN","Admin@123"),
            ("staff@example.com","Staff User","STAFF","Staff@123"),
            ("customer@example.com","Demo Customer","CUSTOMER","Customer@123"),
        ]
        made = {}
        for email,name,role,password in users:
            u = User.objects(email=email).first()
            if not u:
                u = User(email=email,name=name,role=role,password_hash=hash_password(password)).save()
            made[role] = u

        plan = SavingsPlan.objects(name="Monthly Saver").first()
        if not plan:
            plan = SavingsPlan(name="Monthly Saver", plan_type="MONTHLY", duration_months=12,
                               minimum_deposit=Decimal("1000"), interest_rate=Decimal("6.5")).save()

        if not Account.objects(customer=made["CUSTOMER"]).first():
            Account(customer=made["CUSTOMER"], account_number="SA-DEMO001",
                    plan=plan, interest_rate=plan.interest_rate,
                    balance=Decimal("25000")).save()
        self.stdout.write(self.style.SUCCESS("Demo data created."))
