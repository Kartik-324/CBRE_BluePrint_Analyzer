from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import base64
from dotenv import load_dotenv
from typing import Optional
import aiofiles
from datetime import datetime

# Load environment variables
load_dotenv()

# Import AI modules
from ai_processor import BlueprintAnalyzer
from voice_handler import VoiceHandler

# Initialize FastAPI app
app = FastAPI(
    title="CBRE Blueprint Analyzer API",
    description="AI-powered blueprint analysis system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI components
blueprint_analyzer = BlueprintAnalyzer()
voice_handler = VoiceHandler()

# Create uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "CBRE Blueprint Analyzer",
        "version": "1.0.0"
    }


@app.post("/api/analyze-blueprint")
async def analyze_blueprint(
    file: UploadFile = File(...),
    question: Optional[str] = Form(None),
    audio: Optional[UploadFile] = File(None)
):
    """
    Analyze blueprint with text or voice question
    """
    try:
        # Save uploaded blueprint
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = file.filename.split(".")[-1]
        blueprint_path = os.path.join(UPLOAD_DIR, f"blueprint_{timestamp}.{file_extension}")
        
        async with aiofiles.open(blueprint_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Process voice input if provided
        if audio:
            audio_path = os.path.join(UPLOAD_DIR, f"audio_{timestamp}.wav")
            async with aiofiles.open(audio_path, 'wb') as f:
                audio_content = await audio.read()
                await f.write(audio_content)
            
            question = voice_handler.transcribe_audio(audio_path)
            os.remove(audio_path)  # Clean up audio file
        
        # If no question provided, give general analysis
        if not question:
            question = "Please provide a comprehensive analysis of this blueprint including number of rooms, dimensions, layout type, and key features."
        
        # Analyze blueprint
        analysis = await blueprint_analyzer.analyze_blueprint(blueprint_path, question)
        
        return JSONResponse(content={
            "success": True,
            "question": question,
            "analysis": analysis["answer"],
            "confidence": analysis.get("confidence", "high"),
            "timestamp": timestamp
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/ask-followup")
async def ask_followup(
    blueprint_id: str = Form(...),
    question: Optional[str] = Form(None),
    audio: Optional[UploadFile] = File(None)
):
    """
    Ask follow-up questions about previously analyzed blueprint
    """
    try:
        # Find the blueprint file
        blueprint_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(f"blueprint_{blueprint_id}")]
        
        if not blueprint_files:
            raise HTTPException(status_code=404, detail="Blueprint not found")
        
        blueprint_path = os.path.join(UPLOAD_DIR, blueprint_files[0])
        
        # Process voice input if provided
        if audio:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_path = os.path.join(UPLOAD_DIR, f"audio_{timestamp}.wav")
            async with aiofiles.open(audio_path, 'wb') as f:
                audio_content = await audio.read()
                await f.write(audio_content)
            
            question = voice_handler.transcribe_audio(audio_path)
            os.remove(audio_path)
        
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        
        # Analyze with follow-up context
        analysis = await blueprint_analyzer.analyze_blueprint(blueprint_path, question)
        
        return JSONResponse(content={
            "success": True,
            "question": question,
            "analysis": analysis["answer"],
            "confidence": analysis.get("confidence", "high")
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Follow-up analysis failed: {str(e)}")


@app.post("/api/transcribe-audio")
async def transcribe_audio(audio: UploadFile = File(...)):
    """
    Transcribe audio to text
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_path = os.path.join(UPLOAD_DIR, f"audio_{timestamp}.wav")
        
        async with aiofiles.open(audio_path, 'wb') as f:
            content = await audio.read()
            await f.write(content)
        
        transcription = voice_handler.transcribe_audio(audio_path)
        os.remove(audio_path)
        
        return JSONResponse(content={
            "success": True,
            "transcription": transcription
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@app.delete("/api/cleanup")
async def cleanup_uploads():
    """
    Clean up old upload files
    """
    try:
        count = 0
        for filename in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, filename)
            os.remove(file_path)
            count += 1
        
        return JSONResponse(content={
            "success": True,
            "files_deleted": count
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True
    )