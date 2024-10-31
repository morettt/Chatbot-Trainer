from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware  # 导入 CORS 中间件
from transformers import AutoTokenizer, AutoModel, StoppingCriteria, StoppingCriteriaList, TextIteratorStreamer
import uvicorn
import json
import torch
from threading import Thread

MODEL_PATH = "/root/autodl-tmp/glm-4-9b-chat"
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    trust_remote_code=True,
    encode_special_tokens=True
)
model = AutoModel.from_pretrained(
    MODEL_PATH, 
    trust_remote_code=True,
    device_map="auto").eval()

class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        stop_ids = model.config.eos_token_id
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False

app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源。可以根据需要调整为指定的域名。
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

async def generate_stream(model_inputs, generate_kwargs):
    streamer = generate_kwargs["streamer"]
    thread = Thread(target=model.generate, kwargs=generate_kwargs)
    thread.start()
    
    for new_token in streamer:
        if new_token:
            yield f"data: {json.dumps({'response': new_token})}\n\n"
    
    yield f"data: {json.dumps({'end_of_stream': True})}\n\n"

@app.post("/")
async def create_item(request: Request):
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    prompt = json_post_list.get('prompt')
    history = json_post_list.get('history')
    max_length = json_post_list.get('max_length')
    top_p = json_post_list.get('top_p')
    temperature = json_post_list.get('temperature')
    stop = StopOnTokens()
    
    messages = []
    for user_msg, model_msg in history:
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if model_msg:
            messages.append({"role": "assistant", "content": model_msg})
    messages.append({"role": "user", "content": prompt})
    
    model_inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True, 
        tokenize=True,
        return_tensors="pt"
    ).to(model.device)
    
    streamer = TextIteratorStreamer(
        tokenizer=tokenizer,
        timeout=60,
        skip_prompt=True,
        skip_special_tokens=True  
    )
    
    generate_kwargs = {
        "input_ids": model_inputs,
        "streamer": streamer,
        "max_new_tokens": max_length if max_length else 2048,
        "do_sample": True,
        "top_p": top_p if top_p else 0.8,
        "temperature": temperature if temperature else 0.6,
        "stopping_criteria": StoppingCriteriaList([stop]),
        "repetition_penalty": 1.2,
        "eos_token_id": model.config.eos_token_id,
    }
    
    return StreamingResponse(generate_stream(model_inputs, generate_kwargs), media_type="text/event-stream")

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=6006, workers=1)
