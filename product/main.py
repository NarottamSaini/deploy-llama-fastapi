from fastapi import FastAPI, status, Response, HTTPException ## status : for adding status of api response, Response: For raising exception
from product.routers import signin
from fastapi.params import Depends
from .import schemas
from .import models
# from pydantic import BaseModel
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
# from typing import List
from passlib.context import CryptContext
from .database import get_db
from .routers import signin,  user, query #product,
# from starlette.status import HTTP_404_NOT_FOUND

from huggingface_hub import login
import torch
from transformers import pipeline

app = FastAPI(

    title="OpenSource Chatbot API",
    description="Get details of all Chatbot API",
    terms_of_service="http://www.google.com",
    contact={
        "Developer name": "Narottam Saini",
        "website": "http://www.google.com",
        "email": "Narottam.Saini@ymail.com"
    },
    license_info={
        "name":"XYZ",
        "url":"http://www.google.com"
    },
    #docs_url="/documentation", redoc_url=None ## parameter for changing default url link for docs
)
# app.include_router(product.router)
app.include_router(signin.router)
app.include_router(user.router)
app.include_router(query.router)

models.Base.metadata.create_all(engine)
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

pipe = {}

@app.on_event('startup')
def load_model():
    print("loading the model")

    login(token="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") ## huggingface token
    print("Func:: load_model - laoding llama model!!!")
    pipe["pipe"] = pipeline(
        "text-generation",
        model="meta-llama/Llama-2-7b-chat-hf",
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )
    return pipe


# @app.get("/")
# async def root():
#     return {"message": "Hello!"}


# @app.post("/query")
# async def root(instruction: schemas.Instruction):
#     res = model_query(instruction=instruction)
#     return {"message": f"{res}"}


# def model_query(instruction: schemas.Instruction):
#     # We use the tokenizer's chat template to format each message - see https://huggingface.co/docs/transformers/main/en/chat_templating
#     chat_temperature = instruction.temperature
#     chat_len = instruction.maxlen
#     messages = [
#         {
#             "role": "system",
#             "content": instruction.sysmessage,
#         },
#         {
#             "role": "user",
#             "content": f"{instruction.promptmessage}"},
#     ]
#     prompt = pipe["pipe"].tokenizer.apply_chat_template(
#         messages, tokenize=False, add_generation_prompt=True
#     )
#     outputs = pipe["pipe"](
#         prompt,
#         max_new_tokens=chat_len,
#         do_sample=True,
#         temperature=chat_temperature,
#         top_k=2,
#         top_p=0.95,
#     )
#     print(prompt)

#     output = outputs[0]["generated_text"].split("[/INST]")[1]
#     print(output)
#     return output

