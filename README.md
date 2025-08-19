# ATM System API

## Overview

This project implements an ATM System API using Python and FastAPI. The API allows basic account operations, including:

- Viewing account balances

- Depositing funds

- Withdrawing funds

The system uses in-memory sample accounts.


## Design Decisions

1. **Language Choice - Python:**
I chose Python due to familiarity and proficiency with the language. Its simplicity allows fast prototyping while maintaining readability and maintainability.

2. **Framework - FastAPI:**
I chose FastAPI due to it's high practical usage and the fact it's built on Starlette and Pydantic for asynchronous, high-performance APIs.  
Moreover, it provides automatic documentation - /docs (Swagger UI) and /redoc (ReDoc).
In addition, it preforms type validation - Input data is validated automatically, reducing boilerplate.

3. **Project Structure:**
```bash
atm-api/
├── app/
│   ├── main.py            # Entry point of the API
│   ├── routers/           # API route definitions
│   │   ├── health.py
│   │   └── accounts.py
│   └── services.py        # Business logic and account services
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker build configuration
└── README.md              # Project documentation
```

4. **Logging:**
Used Python’s built-in logging to track API startup, requests, and sample account data.

5. **Error Handling:**
Carefully designed API responses to return clear error messages (e.g., insufficient funds, invalid account).

6. **Modular Code Structure:**
Split code into main.py, routers, and services to improve maintainability ans scalability.

7. **Deployment Considerations:**
Used Docker for reproducible environments.
Ensured the app respects dynamic $PORT variables for hosting platforms.


## Challenges Faced

- **Circular Imports**: Initial attempts to import constants and services across modules led to circular import errors. This was resolved by refactoring imports and using local imports where necessary.

- **Deployment**: Had some trouble finding the best fit cloud service for deployment. using docker, Heroku had some trouble while Google Cloud demended payment. 

- **Logging**: Ensuring logs are visible in both local and deployed environments. Resolved by using standard Python logging that outputs to stdout, which is captured by hosting platforms like Render.

- **Validation**: Some operations (like deposit/withdraw) need JSON payloads; ensured proper validation via Pydantic models.
