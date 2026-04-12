# FastApi Backend Template

### Clone the repository and navigate to the folder:

**using ssh**
``` bash
git clone git@github.com:mobitrendz/fastapi-backend-template.git

or

**using https**
git clone https://github.com/mobitrendz/fastapi-backend-template.git

cd fastapi-backend-template
```

### Initialize the environment & install dependencies:
``` bash
uv sync
```

### Activate virtual environment 
``` bash
source .venv/bin/activate
```

### Update with Your PostgreSQL Database details(username, password, dbname) in .env
**Assuming postgresql is already running locally with an empty database**
``` bash
POSTGRES_URL="postgresql://username:password@localhost:5432/dbname"
```

### Update Super User credentials in .env
**required minimum 8 characters for password**
``` bash
SUPER_USER_NAME=""
SUPER_USER_EMAIL=""
SUPER_USER_PASSWORD=""    
```

### Generate an HS256 Secret key and update it in .env (used for JWT token generation)
**Don't know how to generate? Try this: https://jwtsecretkeygenerator.com/**
``` bash
SECRET_KEY=
```

### Create all predefined database tables in PostgreSQL
``` bash
uv run alembic upgrade head
```

### Verify the framework by navigating to the following URLs.

http://127.0.0.1:8000/Harry%20Potter

http://127.0.0.1:8000/docs

