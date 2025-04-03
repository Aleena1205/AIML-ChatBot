from fastapi import FastAPI, HTTPException
from gemini_service import get_aiml_response

app = FastAPI()

@app.post("/chat/")
def chat_with_gemini(user_input: dict):
    """
    API endpoint for AIML chatbot.
    """
    if "message" not in user_input:
        raise HTTPException(status_code=400, detail="Missing 'message' in request.")
    
    response = get_aiml_response(user_input["message"])
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
