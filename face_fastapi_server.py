"""
FastAPI Face Recognition Server
Thay thế Flask với FastAPI để có performance tốt hơn và async support
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import asyncio
import uvicorn
import base64
import logging
import json
from io import BytesIO
from PIL import Image
import numpy as np

# Import existing modules
from face_recognition_system import FaceRecognitionSystem
from database_manager import DatabaseManager

# Pydantic Models
class HealthResponse(BaseModel):
    status: str = "OK"
    message: str = "Face Recognition API is running"
    version: str = "2.0.0-FastAPI"

class FaceRegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    image: str = Field(..., description="Base64 encoded image")
    description: Optional[str] = Field(None, max_length=500)

class FaceRegisterResponse(BaseModel):
    success: bool
    message: str
    face_id: Optional[int] = None
    processing_time: Optional[float] = None

class FaceRecognizeRequest(BaseModel):
    image: str = Field(..., description="Base64 encoded image")
    threshold: Optional[float] = Field(0.6, ge=0.0, le=1.0)

class FaceRecognizeResponse(BaseModel):
    success: bool
    message: str
    name: Optional[str] = None
    face_id: Optional[int] = None
    similarity: Optional[float] = None
    confidence: Optional[float] = None
    processing_time: Optional[float] = None

class FaceCompareRequest(BaseModel):
    image1: str = Field(..., description="Base64 encoded first image")
    image2: str = Field(..., description="Base64 encoded second image")
    threshold: Optional[float] = Field(0.6, ge=0.0, le=1.0)

class FaceCompareResponse(BaseModel):
    success: bool
    message: str
    similarity: Optional[float] = None
    match: Optional[bool] = None
    processing_time: Optional[float] = None

class FaceInfo(BaseModel):
    face_id: int
    name: str
    description: Optional[str] = None
    created_at: str
    updated_at: str

class FaceListResponse(BaseModel):
    success: bool
    message: str
    faces: List[FaceInfo] = []
    count: int = 0

class DeleteFaceResponse(BaseModel):
    success: bool
    message: str
    deleted_face_id: Optional[int] = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Face Recognition API",
    description="Advanced Face Recognition System using YOLOv8 + InsightFace + FastAPI",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
face_system = None
db_manager = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global face_system, db_manager
    
    try:
        logger.info("🚀 Starting Face Recognition FastAPI Server...")
        
        # Initialize database
        db_manager = DatabaseManager()
        logger.info("✅ Database initialized")
        
        # Initialize face recognition system
        face_system = FaceRecognitionSystem()
        logger.info("✅ Face Recognition System initialized")
        
        logger.info("🎉 FastAPI server started successfully!")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global db_manager
    if db_manager and hasattr(db_manager, 'close'):
        db_manager.close()
    logger.info("👋 FastAPI server shutdown complete")

# Helper functions
async def validate_base64_image(base64_string: str) -> bool:
    """Validate base64 image string"""
    try:
        if not base64_string:
            return False
        
        # Remove data URL prefix if present
        if base64_string.startswith('data:image'):
            base64_string = base64_string.split(',')[1]
        
        # Decode and validate
        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data))
        return True
    except Exception:
        return False

async def process_uploaded_file(file: UploadFile) -> str:
    """Convert uploaded file to base64"""
    try:
        contents = await file.read()
        return base64.b64encode(contents).decode('utf-8')
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to process uploaded file: {str(e)}"
        )

# API Endpoints

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint"""
    return HealthResponse(
        message="Face Recognition FastAPI Server is running"
    )

@app.get("/api/v1/simple-face/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        if db_manager:
            db_manager.get_all_faces()
        
        return HealthResponse(
            message="All systems operational"
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unhealthy"
        )

@app.get("/api/v1/simple-face/test", response_model=HealthResponse)
async def test_endpoint():
    """Test endpoint - Compatible with Spring Boot /api/v1/simple-face/test"""
    return HealthResponse(
        status="success", 
        message="Face Recognition FastAPI Server is working!"
    )

@app.post("/api/v1/simple-face/register", response_model=FaceRegisterResponse)
async def register_face(request: FaceRegisterRequest):
    """Register a new face"""
    import time
    start_time = time.time()
    
    try:
        # Validate base64 image
        if not await validate_base64_image(request.image):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid base64 image format"
            )
        
        # Register face from base64
        result = face_system.register_face_from_base64(
            base64_image=request.image,
            person_name=request.name,
            description=request.description
        )
        
        processing_time = time.time() - start_time
        
        if result["success"]:
            return FaceRegisterResponse(
                success=True,
                message=result["message"],
                face_id=result["face_id"],
                processing_time=processing_time
            )
        else:
            return FaceRegisterResponse(
                success=False,
                message=result["message"],
                processing_time=processing_time
            )
    
    except Exception as e:
        logger.error(f"Face registration error: {str(e)}")
        processing_time = time.time() - start_time
        return FaceRegisterResponse(
            success=False,
            message=f"Registration failed: {str(e)}",
            processing_time=processing_time
        )

@app.post("/api/v1/simple-face/register-file")
async def register_face_file(
    name: str = Form(...),
    file: UploadFile = File(...),
    description: Optional[str] = Form(None)
):
    """Register face from uploaded file"""
    try:
        # Convert file to base64
        base64_image = await process_uploaded_file(file)
        
        # Create request object
        request = FaceRegisterRequest(
            name=name,
            image=base64_image,
            description=description
        )
        
        # Use existing register endpoint
        return await register_face(request)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File registration failed: {str(e)}"
        )

@app.post("/api/v1/simple-face/recognize", response_model=FaceRecognizeResponse)
async def recognize_face(request: FaceRecognizeRequest):
    """Recognize a face"""
    import time
    start_time = time.time()
    
    try:
        # Validate base64 image
        if not await validate_base64_image(request.image):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid base64 image format"
            )
        
        # Recognize face from base64
        result = face_system.recognize_face_from_base64(
            base64_image=request.image,
            threshold=request.threshold
        )
        
        processing_time = time.time() - start_time
        
        return FaceRecognizeResponse(
            success=result["success"],
            message=result["message"],
            name=result.get("name"),
            face_id=result.get("face_id"),
            similarity=result.get("similarity"),
            confidence=result.get("confidence"),
            processing_time=processing_time
        )
    
    except Exception as e:
        logger.error(f"Face recognition error: {str(e)}")
        processing_time = time.time() - start_time
        return FaceRecognizeResponse(
            success=False,
            message=f"Recognition failed: {str(e)}",
            processing_time=processing_time
        )

@app.post("/api/v1/simple-face/recognize-file")
async def recognize_face_file(
    file: UploadFile = File(...),
    threshold: float = Form(0.6)
):
    """Recognize face from uploaded file"""
    try:
        # Convert file to base64
        base64_image = await process_uploaded_file(file)
        
        # Create request object
        request = FaceRecognizeRequest(
            image=base64_image,
            threshold=threshold
        )
        
        # Use existing recognize endpoint
        return await recognize_face(request)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File recognition error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File recognition failed: {str(e)}"
        )

@app.post("/api/v1/simple-face/compare", response_model=FaceCompareResponse)
async def compare_faces(request: FaceCompareRequest):
    """Compare two faces"""
    import time
    start_time = time.time()
    
    try:
        # Validate both images
        if not await validate_base64_image(request.image1):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid first image format"
            )
        
        if not await validate_base64_image(request.image2):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid second image format"
            )
        
        # Compare faces from base64
        result = face_system.compare_faces_from_base64(
            base64_image1=request.image1,
            base64_image2=request.image2,
            threshold=request.threshold
        )
        
        processing_time = time.time() - start_time
        
        return FaceCompareResponse(
            success=result["success"],
            message=result["message"],
            similarity=result.get("similarity"),
            match=result.get("match"),
            processing_time=processing_time
        )
    
    except Exception as e:
        logger.error(f"Face comparison error: {str(e)}")
        processing_time = time.time() - start_time
        return FaceCompareResponse(
            success=False,
            message=f"Comparison failed: {str(e)}",
            processing_time=processing_time
        )

@app.post("/api/v1/simple-face/compare-files")
async def compare_faces_files(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    threshold: float = Form(0.6)
):
    """Compare two faces from uploaded files"""
    try:
        # Convert files to base64
        base64_image1 = await process_uploaded_file(file1)
        base64_image2 = await process_uploaded_file(file2)
        
        # Create request object
        request = FaceCompareRequest(
            image1=base64_image1,
            image2=base64_image2,
            threshold=threshold
        )
        
        # Use existing compare endpoint
        return await compare_faces(request)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File comparison error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File comparison failed: {str(e)}"
        )

@app.get("/api/v1/simple-face/list", response_model=FaceListResponse)
async def list_faces():
    """Get all registered faces"""
    try:
        faces = db_manager.get_all_faces()
        
        face_info_list = []
        for face in faces:
            face_info = FaceInfo(
                face_id=face[0],
                name=face[1],
                description=face[2] if face[2] else None,
                created_at=str(face[3]) if face[3] else "",
                updated_at=str(face[4]) if face[4] else ""
            )
            face_info_list.append(face_info)
        
        return FaceListResponse(
            success=True,
            message=f"Retrieved {len(face_info_list)} faces",
            faces=face_info_list,
            count=len(face_info_list)
        )
    
    except Exception as e:
        logger.error(f"Face list error: {str(e)}")
        return FaceListResponse(
            success=False,
            message=f"Failed to retrieve faces: {str(e)}",
            faces=[],
            count=0
        )

@app.delete("/api/v1/simple-face/delete/{face_id}", response_model=DeleteFaceResponse)
async def delete_face(face_id: int):
    """Delete a face by ID"""
    try:
        if face_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid face ID"
            )
        
        # Check if face exists
        face = db_manager.get_face_by_id(face_id)
        if not face:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Face not found"
            )
        
        # Delete face
        success = db_manager.delete_face(face_id)
        
        if success:
            return DeleteFaceResponse(
                success=True,
                message="Face deleted successfully",
                deleted_face_id=face_id
            )
        else:
            return DeleteFaceResponse(
                success=False,
                message="Failed to delete face"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Face deletion error: {str(e)}")
        return DeleteFaceResponse(
            success=False,
            message=f"Deletion failed: {str(e)}"
        )

# Development server
if __name__ == "__main__":
    print("🚀 FACE RECOGNITION FASTAPI SERVER")
    print("=" * 50)
    print("📡 API endpoints (Spring Boot Compatible):")
    print("  • GET  /                              - Root endpoint")
    print("  • GET  /api/v1/simple-face/test       - Test endpoint")
    print("  • GET  /api/v1/simple-face/health     - Health check")
    print("  • POST /api/v1/simple-face/register   - Register face (JSON)")
    print("  • POST /api/v1/simple-face/register-file - Register face (file)")
    print("  • POST /api/v1/simple-face/recognize  - Recognize face (JSON)")
    print("  • POST /api/v1/simple-face/recognize-file - Recognize face (file)")
    print("  • POST /api/v1/simple-face/compare    - Compare faces (JSON)")
    print("  • POST /api/v1/simple-face/compare-files - Compare faces (files)")
    print("  • GET  /api/v1/simple-face/list       - List all faces")
    print("  • DEL  /api/v1/simple-face/delete/<id> - Delete face")
    print("=" * 50)
    print("🌐 Server URL: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")
    print("=" * 50)
    
    uvicorn.run(
        "face_fastapi_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )