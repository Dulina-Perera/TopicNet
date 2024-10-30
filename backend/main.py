# %%
import warnings; warnings.filterwarnings("ignore")  # Ignore warnings.
import os, sys; sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Add the current directory to the system path.

# %%
# Import the required modules.
import os
import sys
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.controllers import destroy_router, download_router_, generate_router_, summarize_router, update_router, upload_router_
from app.core_ import load_env_vars, setup_logging

# %%
load_env_vars() # Load the environment variables.
setup_logging() # Setup logging.

# %%
# Define the FastAPI application.
topicnet: FastAPI = FastAPI(
	debug=True,
	title="TopicNet API",
	version="0.1.0",
)

# Allow localhost:5173 to make requests to the API.
topicnet.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:5173"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Register the routers.
topicnet.include_router(destroy_router, prefix="/api/v1/destroy")
topicnet.include_router(download_router_, prefix="/api/v1/download")
topicnet.include_router(generate_router_, prefix="/api/v1/generate")
topicnet.include_router(summarize_router, prefix="/api/v1/summarize")
topicnet.include_router(update_router, prefix="/api/v1/update")
topicnet.include_router(upload_router_, prefix="/api/v1/upload")

# %%
if __name__ == "__main__":
  # Run the FastAPI application using Uvicorn.
  uvicorn.run(
  	"main:topicnet",
    host="127.0.0.1",
    port=5000,
    reload=True,
    workers=4,
    log_level="info"
  )
