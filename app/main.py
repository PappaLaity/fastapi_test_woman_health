import time
from fastapi import FastAPI, File, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.config import settings
from app.routers import predictions,llm_route
# from app.routers.llm_route import Question

# Configuration du logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Initialisation de l'application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API de détection du cancer du sein par IA",
    version=settings.VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware pour logger les requêtes
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.2f}s"
    )
    
    return response

# Gestionnaire d'erreurs global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erreur globale: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Une erreur interne s'est produite"
        }
    )



# Define API endpoints

app.include_router(
    predictions.router,
    prefix=settings.API_V1_STR,
    tags=["prediction"]
)

app.include_router(
    llm_route.router,
    prefix=settings.API_V1_STR,
    tags=["prediction"]
)

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/check")
async def read_root():
    return {"message": "Mangui bakh!"}


@app.on_event("startup")
async def startup_event():
    """Actions au démarrage de l'application"""
    logger.info("Démarrage de l'application Women Health API")
    logger.info(f"Chargement du modèle depuis: {settings.CV_MODEL_PATH}")

@app.on_event("shutdown")
async def shutdown_event():
    """Actions à l'arrêt de l'application"""
    logger.info("Arrêt de l'application Women Health API")



# Ceci est une modification de test pour git pull