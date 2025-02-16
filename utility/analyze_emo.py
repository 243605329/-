import pandas as pd
from tqdm import tqdm  # 进度条
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from functools import lru_cache
from multiprocessing import Pool

# 模型准备
model_name = "uer/roberta-base-finetuned-jd-binary-chinese"
tokenizer = AutoTokenizer.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

@lru_cache(maxsize=1)
def load_model():
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.to(device)
    return model

def process_single(text):
    model = load_model()
    inputs = tokenizer(text, 
                      padding=True, 
                      truncation=True, 
                      max_length=128, 
                      return_tensors="pt").to(device)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    label = "积极" if probs.argmax() == 1 else "消极"
    confidence = probs.max().item()
    return (label, confidence)

def local_sentiment_analysis(texts, batch_size=32) -> list:
    """本地批量情感预测"""
    model = load_model()  # 使用缓存模型
    # 批处理分割
    batches:list = [texts[i:i+batch_size] for i in range(0, len(texts), batch_size)]
  
    results = []
    with torch.no_grad():
        for batch in tqdm(batches, desc="情感推理"):
            inputs = tokenizer(batch, 
                             padding=True, 
                             truncation=True, 
                             max_length=128, 
                             return_tensors="pt").to(device)
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            labels = ["积极" if pred.argmax() == 1 else "消极" for pred in probs]
            confidences = [max(pred.tolist()) for pred in probs]
            results.extend(list(zip(labels, confidences)))
  
    return results

def batch_process(texts):
    with Pool(4) as p:  # 使用4个进程
        return p.map(process_single, texts)

def get_emotion_df(df: pd.DataFrame) -> pd.DataFrame:
    """获取情感分析结果的DataFrame"""
    text_list = df["评论内容"].tolist()
    sentiments = local_sentiment_analysis(text_list)
    # 直接使用中文列名
    return df.assign(
        情绪=[s[0] for s in sentiments],
        自信度=[s[1] for s in sentiments]
    )


