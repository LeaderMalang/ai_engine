from pydantic import BaseModel
from typing import List, Optional, Union

class Step(BaseModel):
    id: str
    label: str
    type: str  # text_input, multiple_choice, slider, etc.
    options: Optional[List[str]] = None  # for multiple_choice
    range: Optional[List[int]] = None  # for sliders
    ai_response: str  # e.g. "suggestion", "feedback"

class Template(BaseModel):
    title: str
    category: str
    steps: List[Step]
