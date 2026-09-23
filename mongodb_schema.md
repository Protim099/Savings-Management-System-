# MongoDB collections

The Django/MongoEngine models create these collections:

- user
- savings_plan
- account
- deposit
- withdrawal
- transaction
- interest_record
- monthly_saving
- notification
- audit_log

MongoDB does not use relational SQL tables. References are stored using MongoEngine DBRefs.

Example:
```js
use savings_management
show collections
db.account.find()
db.transaction.find().sort({created_at:-1})
```
