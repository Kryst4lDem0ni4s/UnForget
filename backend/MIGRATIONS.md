# AI Planner Backend - Migration Guide

## Database Migration with Alembic

This guide explains how to manage database schema changes using Alembic.

## Initial Setup

After setting up your environment and database, create the initial migration:

```powershell
# Navigate to backend directory
cd backend

# Generate initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

## Common Migration Commands

### Create a new migration
```powershell
alembic revision --autogenerate -m "Description of changes"
```

### Apply all pending migrations
```powershell
alembic upgrade head
```

### Downgrade one version
```powershell
alembic downgrade -1
```

### View migration history
```powershell
alembic history
```

### View current version
```powershell
alembic current
```

## Migration Workflow

1. **Modify Models**: Make changes to SQLAlchemy models in `app/models/`
2. **Generate Migration**: Run `alembic revision --autogenerate -m "description"`
3. **Review Migration**: Check the generated file in `alembic/versions/`
4. **Apply Migration**: Run `alembic upgrade head`
5. **Test**: Verify the schema changes worked as expected

## Troubleshooting

### "Target database is not up to date"
```powershell
alembic stamp head
```

### Start fresh (⚠️ This will delete all data)
```powershell
# Downgrade all migrations
alembic downgrade base

# Drop all tables manually if needed
# Then re-run migrations
alembic upgrade head
```

### Manual Migration
If autogenerate doesn't detect your changes:
```powershell
alembic revision -m "Manual migration"
# Edit the generated file in alembic/versions/
# Add your custom SQL or SQLAlchemy operations
alembic upgrade head
```
