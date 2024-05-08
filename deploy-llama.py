from fastapi import FastAPI
from pydantic import BaseModel
from huggingface_hub import login
import torch
from transformers import pipeline

class Query(BaseModel):
    prompt: str


app = FastAPI()
pipe = {}
@app.on_event('startup')
def load_model():
    print("loading the model")

    login(token="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")
    pipe["pipe"] = pipeline(
        "text-generation",
        model="meta-llama/Llama-2-7b-chat-hf",
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )
    return pipe


@app.get("/")
async def root():
    return {"message": "Hello!"}


@app.post("/query")
async def root(query: Query):
    res = model_query(query=query.prompt)
    return {"message": f"{res}"}


def model_query(query: str):
    # We use the tokenizer's chat template to format each message - see https://huggingface.co/docs/transformers/main/en/chat_templating
    messages = [
        {
            "role": "system",
            "content": "You are a friendly chatbot. You only reply with the actual answer without repeating my question.",
        },
        {"role": "user", "content": f"{query}"},
    ]
    prompt = pipe["pipe"].tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    outputs = pipe["pipe"](
        prompt,
        max_new_tokens=2048,
        do_sample=True,
        temperature=0.7,
        top_k=2,
        top_p=0.95,
    )
    print(prompt)

    output = outputs[0]["generated_text"].split("[/INST]")[1]
    return output