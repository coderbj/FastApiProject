# APIRouter 路由模块
import aiofiles
import os
import uuid
from fastapi import APIRouter, UploadFile, HTTPException, File
from pydantic import WithJsonSchema
from typing import Annotated

router = APIRouter(
    prefix="/upload",  # 所有路由自动加上前缀
    tags=["文件上传"],  # Swagger 文档中的分组标签
)

UPLOAD_DIR = "uploads"
MAX_SIZE = 10 * 1024 * 1024 * 1024  # 10GB
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".pdf"}
CHUNK_SIZE = 1024 * 64  # 64KB

# 解决FastAPI上传文件时，Swagger UI无法正确显示文件上传控件的问题
UploadFile = Annotated[UploadFile, WithJsonSchema({"type": "string", "format": "binary"})]

@router.post("/single")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(400, "文件名不能为空")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(400, f"不支持的文件类型: {ext}")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    safe_name = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, safe_name)
    tmp_path = path + ".tmp"

    size = 0
    try:
        async with aiofiles.open(tmp_path, "wb") as f:
            while chunk := await file.read(CHUNK_SIZE):
                size += len(chunk)
                if size > MAX_SIZE:
                    raise HTTPException(413, "文件超过大小限制")
                await f.write(chunk)
        os.replace(tmp_path, path)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise
    finally:
        await file.close()

    return {"filename": safe_name, "size": size, "message": "上传成功"}

@router.post("/multiple")
async def upload_multiple_files(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(400, "文件列表不能为空")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    results = []

    for file in files:
        if not file.filename:
            results.append({"filename": None, "size": 0, "message": "文件名不能为空"})
            continue

        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXT:
            results.append({"filename": file.filename, "size": 0, "message": f"不支持的文件类型: {ext}"})
            continue

        safe_name = f"{uuid.uuid4().hex}{ext}"
        path = os.path.join(UPLOAD_DIR, safe_name)
        tmp_path = path + ".tmp"

        size = 0
        try:
            async with aiofiles.open(tmp_path, "wb") as f:
                while chunk := await file.read(CHUNK_SIZE):
                    size += len(chunk)
                    if size > MAX_SIZE:
                        raise HTTPException(413, f"文件 {file.filename} 超过大小限制")
                    await f.write(chunk)
            os.replace(tmp_path, path)
            results.append({"filename": safe_name, "size": size, "message": "上传成功"})
        except Exception as e:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            results.append({"filename": file.filename, "size": 0, "message": f"上传失败: {str(e)}"})
        finally:
            await file.close()

    return results
