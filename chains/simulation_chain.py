# simulation_chain.py

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_pinecone import PineconeVectorStore
from utils.memory import get_memory
from utils.db import templates
import os

# Load API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX")

# Initialize the Chat LLM
llm = ChatOpenAI(
    model_name="gpt-4o",
    openai_api_key=OPENAI_API_KEY,
    temperature=0.0
)

# GPT Dynamic UI-Aware Prompt Template using simulation template from DB
def build_dynamic_prompt(user_input: str, ui_context: dict, template: dict) -> str:
    ui_components_str = "\n- " + "\n- ".join(ui_context.get("components", []))
    steps = template.get("steps", [])
    step_summary = "\n".join([
        f"Step ID: {step['id']} | Label: {step['label']} | Type: {step['type']} | Expected: {step['ai_response']}"
        for step in steps
    ])
    
    return f"""
        You are an AI simulation assistant.

        Simulation Title: {template.get("title", "")}
        Category: {template.get("category", "")}

        Steps:
        {step_summary}

        User's latest input: "{user_input}"

        Available UI components:
        {ui_components_str}

        🎯 Generate a response for the next step based on the simulation logic.

        🔁 Output format:
        Respond in clean HTML with proper tags. No explanation. Use semantic tags like:
        <p>, <h3>, <ul>, <li>, <label>, <input type='text'>, <select>, etc.

        Keep it minimal, clean, and directly usable in a React component with dangerouslySetInnerHTML.

        """




# Get memory retriever (namespaced per user)
def run_simulation(user_input: str, ui_context: dict, user_id: str,category: str = "career") -> dict:
    try:
        # Get user-specific retriever
        memory = get_memory(user_id)

        # Fetch simulation template from MongoDB
        template = templates.find_one({"category": category}, {"_id": 0})

        # Build dynamic prompt with UI context and template
        prompt = build_dynamic_prompt(user_input, ui_context, template)

        # Initialize QA Chain with memory and retrieval
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=memory,
            return_source_documents=True
        )

        # Run the chain with the dynamic prompt
        result = qa_chain.invoke({"query": prompt})

        return {
            "answer": result.get("result"),
            "sources": [doc.metadata for doc in result.get("source_documents", [])]
        }

    except Exception as e:
        return {"error": str(e)}
