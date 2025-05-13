import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
import uuid
import time
from typing import Dict, Optional
from fastapi.middleware.cors import CORSMiddleware

# Import our existing modules
from core.eeg_processor import preprocess_eeg
from core.music_mapper import eeg_to_music_parameters
from core.midi_generator import json_to_midi
from core.midi_visualizer import visualize_midi
from visualization.plots import create_all_visualizations
from utils.config import config
from data import validate_eeg_file

# Import the clear_uploads_directory function
from utils.clear_uploads import clear_uploads_directory

# Initialize FastAPI app
app = FastAPI(
    title="Autism Buddy API",
    description="API for converting EEG data to music for autism therapy",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Wildcard to allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Mount output directory for static file access
app.mount("/output", StaticFiles(directory="output"), name="output")

# In-memory job storage - would use a database in production
uploaded_files: Dict[str, Path] = {}
jobs: Dict[str, Dict] = {}


@app.get("/")
async def ping():
    return {"message": "Autism Buddy API is running"}


# Debug endpoint to see what files are stored
@app.get("/api/debug/files")
async def debug_files():
    """List all uploaded files for debugging"""
    return {
        "uploaded_files": {k: str(v) for k, v in uploaded_files.items()},
        "uploads_dir_contents": [str(f) for f in UPLOAD_DIR.iterdir()] if UPLOAD_DIR.exists() else []
    }


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload an EEG file (.set, .edf, or .bdf)"""
    # Clean up old uploads before processing new ones
    clear_uploads_directory(UPLOAD_DIR)

    # Generate unique file ID
    file_id = str(uuid.uuid4())

    # Verify file extension
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ['.set', '.edf', '.bdf']:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Supported formats: .set, .edf, .bdf")

    # Create file path and save uploaded file
    file_path = UPLOAD_DIR / f"{file_id}{file_extension}"

    try:
        # Ensure upload directory exists
        UPLOAD_DIR.mkdir(exist_ok=True)

        # Save file with proper error handling
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Verify file was saved
        if not file_path.exists():
            raise HTTPException(
                status_code=500, detail="Failed to save uploaded file")

        # Store file path for later processing
        uploaded_files[file_id] = file_path

        print(f"File uploaded successfully: ID={file_id}, Path={file_path}")

        return {
            "file_id": file_id,
            "filename": file.filename,
            "message": "File uploaded successfully"
        }
    except Exception as e:
        print(f"Error during file upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.post("/api/process/{file_id}")
async def process_file(file_id: str, background_tasks: BackgroundTasks):
    """Start processing the uploaded EEG file"""
    # Check if file exists in our dictionary
    if file_id not in uploaded_files:
        print(f"File ID not found in uploaded_files dictionary: {file_id}")
        print(f"Available file IDs: {list(uploaded_files.keys())}")

        # Check if file might exist in uploads directory anyway
        potential_files = list(UPLOAD_DIR.glob(f"{file_id}*"))
        if potential_files:
            file_path = potential_files[0]
            print(f"Found file in directory that matches ID: {file_path}")
            uploaded_files[file_id] = file_path
        else:
            raise HTTPException(status_code=404, detail="File not found")

    file_path = uploaded_files[file_id]

    # Verify file actually exists on disk
    if not file_path.exists():
        print(f"File doesn't exist at path: {file_path}")
        raise HTTPException(
            status_code=404, detail="File not found at {file_path}")

    # Validate the file
    if not validate_eeg_file(file_path):
        raise HTTPException(status_code=400, detail="Invalid EEG file format")

    # Check if the job is already processing
    for job in jobs.values():
        if job["file_id"] == file_id and job["status"] in ["PENDING", "PROCESSING"]:
            raise HTTPException(
                status_code=400, detail="File is already being processed by another job")

    # Create a new job ID
    job_id = str(uuid.uuid4())

    # Initialize job status
    jobs[job_id] = {
        "status": "PENDING",
        "file_id": file_id,
        "file_path": str(file_path),  # Store the file path for debugging
        "start_time": time.time(),
        "progress": 0,
        "output_files": {},
        "error": None
    }

    # Add the task to background tasks queue without awaiting it
    background_tasks.add_task(process_eeg_data, job_id, file_path)

    # Return immediately with job ID and initial status
    return {"job_id": job_id, "status": "PENDING", "file_path": str(file_path)}


@app.get("/api/status/{job_id}")
async def get_job_status(job_id: str):
    """Get the status of a processing job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]

    response = {
        "job_id": job_id,
        "status": job["status"],
        "progress": job["progress"],
    }

    # Add additional info based on status
    if job["status"] == "COMPLETED":
        # Add URLs to output files
        base_url = "/output/"
        output_urls = {}
        for key, path in job["output_files"].items():
            if key != "visualizations":  # Handle standard files
                relative_path = str(Path(path).relative_to("output"))
                output_urls[key] = f"{base_url}{relative_path}"
            else:  # Handle visualization directory
                # Add individual visualization files
                viz_path = Path(path)
                if viz_path.exists():
                    # Add each visualization file with a descriptive key
                    viz_files = {
                        "wave_distribution_plot": f"{base_url}plots/wave_distribution_boxplot.png",
                        "wave_heatmap_plot": f"{base_url}plots/wave_heatmap.png",
                        "music_parameters_plot": f"{base_url}plots/music_parameters.png",
                        "global_parameters_plot": f"{base_url}plots/global_parameters.png"
                    }
                    # Only include files that actually exist
                    for viz_key, viz_file_path in viz_files.items():
                        # if Path("output" + viz_file_path[7:]).exists():
                        output_urls[viz_key] = viz_file_path

        response["output_files"] = output_urls
        response["processing_time"] = round(
            job["end_time"] - job["start_time"], 2)

    elif job["status"] == "FAILED":
        response["error"] = job["error"]

    return response

# Background processing function


async def process_eeg_data(job_id: str, file_path: Path):
    """Process EEG data in the background"""
    job = jobs[job_id]
    # Get paths from config
    output_paths = config.get('paths', 'output')

    try:
        # Setup directories
        for path in output_paths.values():
            Path(path).mkdir(parents=True, exist_ok=True)

        # Set status to processing to indicate work has started
        job["status"] = "PROCESSING"
        job["progress"] = 10

        # Add a delay to simulate processing time
        await asyncio.sleep(10)

        # Step 1: Preprocess EEG data
        preprocessed_eeg_path = Path(
            output_paths['json']) / 'wave_analysis.json'
        await asyncio.get_event_loop().run_in_executor(
            None, preprocess_eeg, file_path
        )
        job["output_files"]["preprocessed_eeg"] = str(preprocessed_eeg_path)
        job["progress"] = 30

        # Step 2: Generate music parameters
        eeg_music_params_path = Path(
            output_paths['json']) / 'music_parameters.json'
        eeg_global_music_params_path = Path(
            output_paths['json']) / 'global_parameters.json'
        await asyncio.get_event_loop().run_in_executor(
            None, eeg_to_music_parameters, preprocessed_eeg_path
        )
        job["output_files"]["music_parameters"] = str(eeg_music_params_path)

        # Add a delay to simulate processing time
        await asyncio.sleep(10)

        # Add global parameters to output files
        global_params_path = Path(
            output_paths['json']) / 'global_parameters.json'
        if global_params_path.exists():
            job["output_files"]["global_parameters"] = str(global_params_path)

        job["progress"] = 50

        # Add a delay to simulate processing time
        await asyncio.sleep(10)

        # Step 3: Create MIDI file
        midi_path = Path(output_paths['midi']) / 'midi_out.mid'
        await asyncio.get_event_loop().run_in_executor(
            None, json_to_midi, eeg_music_params_path, eeg_global_music_params_path
        )
        job["output_files"]["midi_file"] = str(midi_path)
        job["progress"] = 65

        # Add a delay to simulate processing time
        await asyncio.sleep(10)

        # Step 4: Create MIDI visualization
        await asyncio.get_event_loop().run_in_executor(
            None, lambda: visualize_midi(str(midi_path), output_paths['midi'])
        )
        csv_path = Path(output_paths['midi']) / \
            'midi_visualization.csv'  # Corrected path
        job["output_files"]["midi_visualization"] = str(csv_path)
        job["progress"] = 75

        # Add a delay to simulate processing time
        await asyncio.sleep(10)

        # Step 5: Generate visualizations
        await asyncio.get_event_loop().run_in_executor(
            None, create_all_visualizations, preprocessed_eeg_path, eeg_music_params_path
        )
        job["output_files"]["visualizations"] = output_paths['plots']
        job["progress"] = 90

        # Complete job
        job["status"] = "COMPLETED"
        job["progress"] = 100
        job["end_time"] = time.time()

    except Exception as e:
        # Handle failure
        job["status"] = "FAILED"
        job["error"] = str(e)
        job["end_time"] = time.time()
        print(f"Error during processing: {str(e)}")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8005, reload=True)
