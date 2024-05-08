from fastapi import APIRouter
from fastapi import FastAPI, status, Response, HTTPException ## status : for adding status of api response, Response: For raising exception
from fastapi.params import Depends
from ..import schemas
from ..import models
# from .import login
from .signin import get_current_user
# from product.routers.login import get_current_user
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db

router = APIRouter(tags=['Query'],
                   ) ## prefix="/product"


pipe = {}
## response_model : parameter is used to limit the field/values to be displayed in api response. Only thosefield defined in DisplayProduct class will be dispalyed
## List[schemas.DisplayProduct] : List required as output will be multiple records
# @router.get('/', response_model=List[schemas.DisplayProduct])

def model_query(instruction: schemas.Instruction):
    # We use the tokenizer's chat template to format each message - see https://huggingface.co/docs/transformers/main/en/chat_templating
    chat_temperature = instruction.temperature
    chat_len = instruction.maxlen
    messages = [
        {
            "role": "system",
            "content": instruction.sysmessage,
        },
        {
            "role": "user",
            "content": f"{instruction.promptmessage}"},
    ]
    prompt = pipe["pipe"].tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    outputs = pipe["pipe"](
        prompt,
        max_new_tokens=chat_len,
        do_sample=True,
        temperature=chat_temperature,
        top_k=2,
        top_p=0.95,
    )
    print("Func :: model_query - prompt : ", prompt)

    output = outputs[0]["generated_text"].split("[/INST]")[1]
    print("Func :: model_query - output : ", output)
    return output

@router.post("/query")
# async def root(instruction: Instruction):
def query_llmModel(instruction: schemas.Instruction, db:Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    res = model_query(instruction=instruction)
    return {"message": f"{res}"}