# import io
# import mimetypes
# from operator import itemgetter
#
# import clip
# import numpy as np
# import torch
# from django.test import TestCase
# import django
#
# # Create your tests here.
# import os



# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deep_diary.settings')
# django.setup()
# from library.models import Img




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

#
# def update_graph_node_id(nodes, prefix):
#     """
#     目的： 考虑到不同模块节点的id可能会一样，因此需要更新图谱中的id，将原来的id替换成新的id， 可以实现模块前缀+id的形式
#           e.g. img node 中有 id = 1， profile中也有id= 1, 那对应的edge中的from_id 和 to_id 都需要更新
#     param: nodes:更新前的 nodes 列表
#     param: prefix: 模块前缀
#     return: nodes 更新后的nodes
#     example: nodes = self.update_graph_node_id(nodes, prefix='img')
#     """
#     nodes_updated = [{**node, 'id': prefix + str(node['id'])} for node in nodes]
#     # nodes_updated = [{**node, 'id': 'img'} for node in nodes]
#     return nodes_updated
#
#
# nodes=[
#     {
#         "id": 538,
#     },
#     {
#         "id": 537,
#     }
# ]
#
# nodes_updated = update_graph_node_id(nodes, 'img')
# print(nodes_updated)