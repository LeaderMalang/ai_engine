from pydantic import BaseModel
from typing import Dict

class SimulateInput(BaseModel):
    input: str
    ui: Dict  # e.g. {"components": ["text_input", "slider"]}
    user_id: str
    category: str = "career"  # Default category
