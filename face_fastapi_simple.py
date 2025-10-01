"""
FastAPI Face Recognition Server (Simplified Version)
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import base64
import uvicorn

# Import existing modules
from face_recognition_system import FaceRecognitionSystem
from database_manager import DatabaseManager

# Pydantic Models
class HealthResponse(BaseModel):
    status: str = "OK"
    message: str = "FastAPI Face Recognition is running"

class FaceRegisterRequest(BaseModel):
    name: str
    image: str
    description: Optional[str] = None

class FaceRegisterResponse(BaseModel):
    success: bool
    message: str
    face_id: Optional[int] = None

class FaceRecognizeRequest(BaseModel):
    image: str
    threshold: Optional[float] = 0.6

class FaceRecognizeResponse(BaseModel):
    success: bool
    message: str
    name: Optional[str] = None
    face_id: Optional[int] = None
    similarity: Optional[float] = None

# Initialize FastAPI app
app = FastAPI(title="Face Recognition API", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
print("🔄 Initializing Face Recognition System...")
face_system = FaceRecognitionSystem()
db_manager = DatabaseManager()
print("✅ System initialized!")

@app.get("/", response_model=HealthResponse)
async def root():
    return HealthResponse(message="FastAPI Face Recognition Server")

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(message="System operational")

@app.post("/api/face/register", response_model=FaceRegisterResponse)
async def register_face(request: FaceRegisterRequest):
    try:
        result = face_system.register_face(
            name=request.name,
            image_base64=request.image,
            description=request.description
        )
        
        return FaceRegisterResponse(
            success=result["success"],
            message=result["message"],
            face_id=result.get("face_id")
        )
    except Exception as e:
        return FaceRegisterResponse(
            success=False,
            message=f"Error: {str(e)}"
        )

@app.post("/api/face/recognize", response_model=FaceRecognizeResponse)
async def recognize_face(request: FaceRecognizeRequest):
    try:
        result = face_system.recognize_face(
            image_base64=request.image,
            threshold=request.threshold
        )
        
        return FaceRecognizeResponse(
            success=result["success"],
            message=result["message"],
            name=result.get("name"),
            face_id=result.get("face_id"),
            similarity=result.get("similarity")
        )
    except Exception as e:
        return FaceRecognizeResponse(
            success=False,
            message=f"Error: {str(e)}"
        )

@app.get("/api/face/list")
async def list_faces():
    try:
        faces = db_manager.get_all_faces()
        face_list = []
        
        for face in faces:
            face_info = {
                "face_id": face[0],
                "name": face[1],
                "description": face[2] if face[2] else None,
                "created_at": str(face[3]) if face[3] else ""
            }
            face_list.append(face_info)
        
        return {
            "success": True,
            "message": f"Retrieved {len(face_list)} faces",
            "faces": face_list,
            "count": len(face_list)
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "faces": [],
            "count": 0
        }

if __name__ == "__main__":
    print("🚀 FASTAPI FACE RECOGNITION SERVER")
    print("=" * 40)
    print("🌐 Server: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("=" * 40)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)