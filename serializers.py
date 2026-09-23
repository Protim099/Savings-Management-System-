def user_data(u):
    return {"id":str(u.id),"email":u.email,"name":u.name,"phone":u.phone,"role":u.role}

def plan_data(p):
    return {"id":str(p.id),"name":p.name,"plan_type":p.plan_type,
            "duration_months":p.duration_months,"minimum_deposit":str(p.minimum_deposit),
            "interest_rate":str(p.interest_rate),"is_active":p.is_active}

def account_data(a):
    return {"id":str(a.id),"account_number":a.account_number,"customer":a.customer.name,
            "customer_id":str(a.customer.id),"plan":a.plan.name if a.plan else None,
            "balance":str(a.balance),"interest_rate":str(a.interest_rate),"status":a.status}

def transaction_data(t):
    return {"id":str(t.id),"account":t.account.account_number,
            "transaction_type":t.transaction_type,"amount":str(t.amount),
            "reference":t.reference,"description":t.description,
            "created_at":t.created_at.isoformat()}
