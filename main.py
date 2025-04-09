from fastapi import FastAPI, Request,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from chains.simulation_chain import run_simulation
from auth import authenticate_user, create_access_token, get_current_user
from models.template_model import Template
from utils.db import templates
from utils.memory import get_chat_history
from models.simulate_input import SimulateInput
import uvicorn
from datetime import timedelta
from fastapi.responses import JSONResponse

app = FastAPI(title="Simulation Ai Engine", version="2")
# Allow all origins (dev mode)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def serialize_template(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# Token endpoint
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(form_data.username, form_data.password):
        return {"error": "Invalid credentials"}
    token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=timedelta(minutes=60)
    )
    return {"access_token": token, "token_type": "bearer"}


@app.post("/simulate/")
async def simulate(payload: SimulateInput, user: str = Depends(get_current_user)):
    user_input = payload.input
    ui_context = payload.ui
    user_id = payload.user_id
    category = payload.category


    result = run_simulation(user_input, ui_context, user_id,category)
    return {"output": result}



@app.post("/admin/template/create/")
def create_template(template: Template,user: str = Depends(get_current_user)):
    templates.insert_one(template.dict())
    return {"message": "Template created successfully"}

@app.get("/template/{category}")
def get_template(category: str):
    data = templates.find_one({"category": category}, {"_id": 0})
    if not data:
        return {"error": "Template not found"}
    return data

# 🧠 Helper to serialize ObjectId
def serialize_template(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

# 🚀 Get all templates by category
@app.get("/templates/{category}")
def get_templates_by_category(category: str):
    cursor = templates.find({"category": category})
    data = [serialize_template(doc) for doc in cursor]

    if not data:
        return JSONResponse(status_code=404, content={"error": "No templates found for this category"})

    return data



@app.get("/templates")
def get_templates_by_category():
    cursor = templates.find()
    data = [serialize_template(doc) for doc in cursor]

    if not data:
        return JSONResponse(status_code=404, content={"error": "No templates found for this category"})

    return data

@app.get("/user/{user_id}/history")
def get_user_chat_history(user_id: str):
    history = get_chat_history(user_id)
    
    if not history or not history.get("vectors"):
        return {"message": f"No chat history found for user ID: {user_id}"}
    
    # Optional: extract just the values/texts
    chat_logs = []
    for item in history["vectors"].values():
        metadata = item.get("metadata", {})
        if "text" in metadata:
            chat_logs.append(metadata["text"])
    
    return {
        "user_id": user_id,
        "total": len(chat_logs),
        "chat_history": chat_logs
    }



if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")