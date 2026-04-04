# Peewee Model Creation Guide

## Instructions for Creating Models in this Project

When creating a new Peewee model file in the `app/models/` directory, follow these patterns and best practices:

### 1. Import Structure
```python
from peewee import *
from datetime import datetime
from app.database import BaseModel
```

**Important**: Always import `BaseModel` from `app.database` - this is the base class that integrates with the PostgreSQL database proxy pattern used in this project.

### 2. Model Class Definition
- **Inherit from BaseModel**: All models must inherit from `BaseModel`, not directly from `Model`
- **Naming Convention**: Use singular form for model names (e.g., `User`, not `Users`)

### 3. Standard Fields
Every model should typically include these fields:
```python
id = AutoField()  # Primary key
created_at = DateTimeField(default=datetime.now)
updated_at = DateTimeField(default=datetime.now)
```

### 4. Field Types and Constraints
- Use `CharField` with `max_length` for string fields
- Add `unique=True` for fields that should be unique (like email)
- Use `TextField` for longer text without length limits
- Use `BooleanField` with appropriate defaults
- Use `ForeignKeyField` for relationships (reference the model class, not string)

### 5. Model Meta Configuration
```python
class Meta:
    table_name = "lowercase_plural_name"  # e.g., "users", "events", "urls"
```

### 6. Override Save Method
Always override the save method to update the `updated_at` timestamp:
```python
def save(self, *args, **kwargs):
    self.updated_at = datetime.now()
    return super(ModelName, self).save(*args, **kwargs)
```

### 7. String Representation
Add a `__str__` method that returns a meaningful representation:
```python
def __str__(self):
    return self.name  # or another meaningful field
```

### 8. Common Mistakes to Avoid
- ❌ Don't inherit from undefined classes
- ❌ Don't use `database` directly - use the inherited connection from `BaseModel`
- ❌ Don't forget to import `BaseModel` from `app.database`
- ❌ Don't mix model definitions (e.g., putting Event fields in a User model)

### 9. Example Structure
Here's the pattern used for the User model:
```python
from peewee import *
from datetime import datetime
from app.database import BaseModel


class User(BaseModel):
    id = AutoField()
    name = CharField(max_length=100)
    email = CharField(max_length=255, unique=True)
    password_hash = CharField(max_length=255)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    is_active = BooleanField(default=True)

    class Meta:
        table_name = "users"

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
```

### 10. Project-Specific Database Setup
This project uses:
- PostgreSQL as the database
- Peewee's `DatabaseProxy` pattern for connection management
- Configuration through environment variables
- Automatic connection handling via Flask hooks

Follow these patterns consistently across all models to maintain code quality and compatibility with the existing database infrastructure.
