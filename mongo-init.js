// Optional MongoDB initialization script
db = db.getSiblingDB('savings_management');

db.createCollection('user');
db.createCollection('savings_plan');
db.createCollection('account');
db.createCollection('deposit');
db.createCollection('withdrawal');
db.createCollection('transaction');
db.createCollection('interest_record');
db.createCollection('monthly_saving');
db.createCollection('notification');
db.createCollection('audit_log');

db.user.createIndex({email:1},{unique:true});
db.account.createIndex({account_number:1},{unique:true});
db.savings_plan.createIndex({name:1},{unique:true});

print('Savings Management MongoDB collections and indexes initialized.');
