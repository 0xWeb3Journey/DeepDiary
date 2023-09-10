import io
import mimetypes
from operator import itemgetter

import clip
import numpy as np
import torch
from django.test import TestCase
import django

# Create your tests here.
import os



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deep_diary.settings')
django.setup()
from library.models import Img




# class MyModelTestCase(TestCase):
#     def setUp(self):
#         # 设置测试环境
#         # 创建测试数据
#         pass
#
#     def test_something(self):
#         # 编写测试代码
#         pass
#
#     def test_another_thing(self):
#         # 编写测试代码
#         pass


# search_params = 'allison is standing on the ground in Ningbo province, China.'
#
#
# from transformers import AutoTokenizer, AutoModelForTokenClassification
# from transformers import pipeline
#
# tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
# model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
# nlp = pipeline("ner", model=model, tokenizer=tokenizer)
#
# text = "Blue was standing on the ground in Ningbo province, China in year 2023."
#
# device = "cuda" if torch.cuda.is_available() else "cpu"
# model, preprocess = clip.load("ViT-B/32", device=device)
#
# text_token = clip.tokenize(text).to(device)
#
# preds = nlp(text)
# preds = [
#     {
#         "entity": pred["entity"],
#         "score": round(pred["score"], 4),
#         "index": pred["index"],
#         "word": pred["word"],
#         "start": pred["start"],
#         "end": pred["end"],
#     }
#     for pred in preds
# ]
# print(*preds, sep="\n")