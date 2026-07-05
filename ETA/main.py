from fastapi import FastAPI
from routers.category import router as c_router
from routers.transaction import router as t_router
from routers.reports import router as report_router
from routers.custom_range_report import router as range_router
from database import Base, engine
from routers.auth import router as auth_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

app.include_router(c_router)
app.include_router(t_router)
app.include_router(report_router)
app.include_router(range_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Expense Tracker API is running"}