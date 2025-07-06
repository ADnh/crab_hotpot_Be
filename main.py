from fastapi import FastAPI
# from routes.nlp import router as nlp_router
from routes.ips import router as ips_router
from routes.crud import router as crud_router
from routes.crawl import router as crawl_router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title="Back-end")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(nlp_router, prefix="/nlp_apis")
app.include_router(ips_router, prefix="/ips_apis")
app.include_router(crud_router, prefix="/crud_apis")
app.include_router(crawl_router, prefix="/crawl_apis")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)