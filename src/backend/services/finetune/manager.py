from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid

router = APIRouter(prefix="/finetune", tags=["finetune"])

class FineTuneJob(BaseModel):
    id: str
    model_name: str
    dataset_path: str
    status: str
    epochs: int = 3
    batch_size: int = 4

jobs = {}

@router.post("/jobs")
async def create_finetune_job(model_name: str, dataset_path: str, epochs: int = 3):
    job_id = str(uuid.uuid4())
    job = FineTuneJob(
        id=job_id,
        model_name=model_name,
        dataset_path=dataset_path,
        status="pending",
        epochs=epochs
    )
    jobs[job_id] = job
    # TODO: Trigger background training task
    return job

@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

@router.get("/jobs")
async def list_jobs():
    return list(jobs.values())
