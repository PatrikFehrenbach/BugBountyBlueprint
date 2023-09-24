from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Dict

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "tpls")

class MarkdownTemplate(BaseModel):
    name: str
    content: str

class ProcessMarkdownRequest(BaseModel):
    template_name: str
    params: Dict[str, str]

def get_secure_path(base_path: str, user_input: str) -> str:
    result_path = os.path.abspath(os.path.join(base_path, user_input))
    if not result_path.startswith(base_path):
        raise HTTPException(status_code=400, detail="Invalid file name")
    return result_path

@app.get("/templates/")
def list_templates():
    return {"list": [f for f in os.listdir(TEMPLATE_PATH) if f.endswith('.md')]}

@app.get("/template/{template_name}")
def get_template(template_name: str):
    file_path = get_secure_path(TEMPLATE_PATH, template_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Template not found")
    with open(file_path, 'r') as f:
        return {"data": f.read()}

@app.post("/process_markdown/")
def process_markdown(request: ProcessMarkdownRequest):
    file_path = get_secure_path(TEMPLATE_PATH, request.template_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Template not found")
    with open(file_path, 'r') as f:
        template = f.read()
    for key, value in request.params.items():
        placeholder = f"{{{{{key}}}}}"
        template = template.replace(placeholder, value)
    return {"markdown": template}

@app.post("/template/")
def create_template(template: MarkdownTemplate):
    file_path = get_secure_path(TEMPLATE_PATH, template.name)
    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="Template already exists")
    with open(file_path, 'w') as f:
        f.write(template.content)
    return {"message": "Template created successfully"}

@app.put("/template/{template_name}")
def update_template(template_name: str, template: MarkdownTemplate):
    file_path = get_secure_path(TEMPLATE_PATH, template_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Template not found")
    with open(file_path, 'w') as f:
        f.write(template.content)
    return {"message": "Template updated successfully"}

@app.delete("/template/{template_name}")
def delete_template(template_name: str):
    file_path = get_secure_path(TEMPLATE_PATH, template_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Template not found")
    os.remove(file_path)
    return {"message": "Template deleted successfully"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
