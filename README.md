# CHATBOT-SERVER

## Env

```bash
conda create -n chatbotserver python=3.11
conda activate chatbotserver
```

```bash
pip install -e .
```

## Run

```bash
app-run
```

## Alembic

### Initialize

```bash
alembic init alembic
```

### alembic.ini

```plaintext
sqlalchemy.url = sqlite:///db/chat-server.sqlite
```

### alembic/env.py

```python
from app import models
target_metadata = models.Base.metadata
```

### Migration

```bash
alembic revision --autogenerate -m "Initialize"
alembic upgrade head
```

## Streaming Test

On browser

```
http://127.0.0.1:8000/api/chat/stream?query=What+is+Fokker+Planck+Equation
```

## Reference

- [Opengpts Schema](https://github.com/langchain-ai/opengpts/blob/main/backend/app/schema.py)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [with_structured_output-method](https://python.langchain.com/docs/how_to/structured_output/#the-with_structured_output-method)
- [MultiRouteChain](https://python.langchain.com/api_reference/langchain/chains/langchain.chains.router.base.MultiRouteChain.html)

## Data Folder Structure

fastapi_app/
│── pyproject.toml
│── .env
│── alembic/
│── tests/
│ ├── test_main.py
│ ├── test_users.py
│ ├── test_ai.py
│ ├── conftest.py
│── src/
│ ├── app/
│ │ ├── main.py
│ │ ├── database.py
│ │ ├── models.py
│ │ ├── schemas.py
│ │ ├── crud.py
│ │ ├── dependencies.py
│ │ ├── core/
│ │ │ ├── **init**.py
│ │ │ ├── config.py # <-- Core app config
│ │ ├── routers/
│ │ │ ├── **init**.py
│ │ │ ├── users.py
│ │ │ ├── items.py
│ │ │ ├── ai.py
│ │ ├── ai_engine/
│ │ │ ├── **init**.py
│ │ │ ├── ai_service.py
│ │ │ ├── prompt_templates.py
│ │ ├── utils/ # <-- Utility functions
│ │ │ ├── **init**.py
│ │ │ ├── config.py # <-- Config utility module
│ │ │ ├── logging.py # <-- (Optional) Logging utilities
