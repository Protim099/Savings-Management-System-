from mongoengine import (
    Document, StringField, EmailField, DateTimeField, DecimalField,
    BooleanField, ReferenceField, ListField, IntField
)
from datetime import datetime
from decimal import Decimal

class User(Document):
    email = EmailField(unique=True, required=True)
    password_hash = StringField(required=True)
    role = StringField(choices=("ADMIN","STAFF","CUSTOMER"), default="CUSTOMER")
    name = StringField(max_length=120, required=True)
    phone = StringField(max_length=30)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)

class SavingsPlan(Document):
    name = StringField(required=True, unique=True)
    plan_type = StringField(choices=("MONTHLY","FIXED","GENERAL"), default="GENERAL")
    duration_months = IntField(default=12)
    minimum_deposit = DecimalField(precision=2, default=Decimal("0"))
    interest_rate = DecimalField(precision=4, default=Decimal("0"))
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)

class Account(Document):
    customer = ReferenceField(User, required=True)
    account_number = StringField(required=True, unique=True)
    plan = ReferenceField(SavingsPlan)
    balance = DecimalField(precision=2, default=Decimal("0"))
    interest_rate = DecimalField(precision=4, default=Decimal("0"))
    status = StringField(choices=("ACTIVE","BLOCKED","CLOSED"), default="ACTIVE")
    created_at = DateTimeField(default=datetime.utcnow)

class Deposit(Document):
    account = ReferenceField(Account, required=True)
    amount = DecimalField(precision=2, required=True)
    payment_method = StringField(default="CASH")
    transaction_id = StringField()
    status = StringField(choices=("PENDING","APPROVED","REJECTED"), default="PENDING")
    created_at = DateTimeField(default=datetime.utcnow)
    approved_at = DateTimeField()

class Withdrawal(Document):
    account = ReferenceField(Account, required=True)
    amount = DecimalField(precision=2, required=True)
    method = StringField(default="BANK")
    status = StringField(choices=("PENDING","APPROVED","REJECTED"), default="PENDING")
    created_at = DateTimeField(default=datetime.utcnow)
    approved_at = DateTimeField()

class Transaction(Document):
    account = ReferenceField(Account, required=True)
    transaction_type = StringField(choices=("DEPOSIT","WITHDRAWAL","INTEREST","TRANSFER","FEE"))
    amount = DecimalField(precision=2, required=True)
    reference = StringField()
    description = StringField()
    created_at = DateTimeField(default=datetime.utcnow)

class InterestRecord(Document):
    account = ReferenceField(Account, required=True)
    principal = DecimalField(precision=2, required=True)
    rate = DecimalField(precision=4, required=True)
    interest_amount = DecimalField(precision=2, required=True)
    calculation_type = StringField(default="SIMPLE")
    credited_at = DateTimeField(default=datetime.utcnow)

class MonthlySaving(Document):
    account = ReferenceField(Account, required=True)
    month = StringField(required=True)
    target_amount = DecimalField(precision=2, required=True)
    paid_amount = DecimalField(precision=2, default=Decimal("0"))
    status = StringField(default="PENDING")

class Notification(Document):
    user = ReferenceField(User, required=True)
    title = StringField(required=True)
    message = StringField(required=True)
    is_read = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)

class AuditLog(Document):
    user = ReferenceField(User)
    action = StringField(required=True)
    entity = StringField()
    entity_id = StringField()
    details = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
