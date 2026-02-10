# TODO: Connect Database "webD" to the Project

## Status: COMPLETED ✅

### Steps Completed:
- [x] 1. Analyze current database configuration
- [x] 2. Create plan and get user confirmation
- [x] 3. Update config.py - Changed DB_NAME to 'webD'
- [x] 4. Update docker-compose.yml - Changed MYSQL_DATABASE to 'webD'
- [x] 5. Update db_setup.py - Changed database name in setup script

## Files Modified:
1. **config.py** - DB_NAME changed from `flask_auth` to `webD`
2. **docker-compose.yml** - MYSQL_DATABASE and DB_NAME changed from `flask_auth` to `webD`
3. **db_setup.py** - Database name changed from `flask_auth` to `webD`

## Next Steps (Required to Apply Changes):

Run the following commands to restart Docker and create the new database:

```bash
docker-compose down
docker-compose up -d
```

The `db_setup.py` script will automatically:
1. Create the database `webD` if it doesn't exist
2. Create all tables: users, customers, courses, sessions

## Connection Details:
- Database: webD
- User: webd
- Password: Web123
- Host: mysql (from Flask app)
- Port: 3306

