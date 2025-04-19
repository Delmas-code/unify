from fastapi import FastAPI
from app.db.init_db import init_db
from app.core.utils.loggers import setup_logger
from fastapi.middleware.cors import CORSMiddleware

#import routers
from app.api.routes import unified

app = FastAPI()
logger = setup_logger("app/main", "logs/app.log")

try:
    @app.on_event("startup")
    async def startup_event():
        await init_db(app)
        logger.info("Unify application started successfully.")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        mongo_client = app.state.mongo_client
        if mongo_client:
            mongo_client.close()
            logger.info("MongoDB client closed.")
        logger.info("Unify application shut down successfully.")  
        # if hasattr(app.state, "db") and app.state.db:
        #     await app.state.db.close()
        #     logger.info("Unify application shut down successfully.")
        
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(
        unified.router,
        prefix="/unified/v1",
        tags=["Unified"],
    )

except Exception as e:
    logger.error(f"Error starting the Unify application: {e}")
    raise e