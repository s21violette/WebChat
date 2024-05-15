# WebChat
## WIP

alembic revision --autogenerate -m "init migration"
alembic upgrade head
cd src
uvicorn main:app --reload