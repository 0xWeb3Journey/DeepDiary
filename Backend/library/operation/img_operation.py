# img_operation.py
# force on dealing with Img model

import clip
import numpy as np
import torch

from library.models import Img
from library.operation.base_operation import BaseOperation
from utilities.common import trace_function


# from django.core.files import File
# from utils.mcs_storage import upload_file_pay


class ImgOperation(BaseOperation):
    def __init__(self, img_instance=None):
        # 由于Stat是一个独立的模型，这里直接调用父类初始化方法即可
        super().__init__(Img, img_instance)

    @trace_function
    def save(self, data, *args, **kwargs):
        self.img_instance.__dict__.update(data)
        self.img_instance.save()

    @staticmethod
    @trace_function
    def get_processing_imgs(processor_types, force):
        processing_imgs = {}
        imgs_all = Img.objects.all()

        for processor_type in processor_types:
            # Construct the field name for the 'is_get_' flag in the Stat model
            stat_field = f'is_get_{processor_type}'
            imgs = imgs_all.filter(**{f'stats__{stat_field}': False})
            if processor_type == 'exif':
                imgs = imgs.filter(stats__is_has_exif=True)

            if force:
                processing_imgs[processor_type] = imgs_all
            else:
                processing_imgs[processor_type] = imgs

        return processing_imgs

    @staticmethod
    def img_recognition(text):  # 'instance', serializers

        device = "cuda" if torch.cuda.is_available() else "cpu"
        # device = "cpu"  # 使用cpu 貌似就无法运行
        model, preprocess = clip.load("ViT-B/32", device=device)

        text = clip.tokenize(text).to(device)

        image_features = Img.objects.values_list('embedding', flat=True)
        embeddings = [np.frombuffer(embedding, dtype=np.float32) for embedding in image_features if embedding]
        # 将所有的embedding转换为矩阵形式，大小为N* 512
        embeddings = np.stack(embeddings)

        with torch.no_grad():
            text_features = model.encode_text(text)
            image_features = torch.tensor(embeddings, dtype=torch.float16).to(device)
            # print(text_features.shape)
            # print(image_features.shape)
            # print(type(text_features))
            # print(type(image_features))

        # Pick the top 5 most similar labels for the image
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity = (100.0 * text_features @ image_features.T).softmax(dim=-1)
        values, indices = similarity[0].topk(5)

        # 方法一: 使用itemgetter根据索引值获取id列表
        # filtered_data = itemgetter(*indices.cpu().numpy().tolist())(imgs)
        # topk_ids = [img.id for img in filtered_data]
        # print('方法一: 使用itemgetter根据索引值获取id列表', topk_ids)

        imgs = Img.objects.all()
        # 方法二: 根据索引值直接获取id列表
        topk_ids = [imgs[i].id for i in indices.cpu().numpy().tolist()]
        # print('方法二: 根据索引值直接获取id列表', topk_ids)

        from django.db.models import Case, When, IntegerField
        # 创建一个排序表达式
        order_by_expression = Case(
            *[
                When(id=id, then=index)  # 每个 id 对应一个索引值
                for index, id in enumerate(topk_ids)
            ],
            default=len(topk_ids),  # 默认情况下，使用 topk_ids 列表的长度作为排序值
            output_field=IntegerField(),
        )
        # 对 imgs 查询集进行排序
        filtered_data = imgs.filter(id__in=topk_ids).order_by(order_by_expression)

        # Print the result
        print("\nTop predictions:\n")
        for value, id in zip(values, topk_ids):
            print(f"{id}: {100 * value.item():.2f}%")

        return filtered_data

    def get_category_data(self):
        """
        获取分类数据。
        """

        return {
            **self.get_category_data_layout(),
            **self.get_category_data_size()
        }

    def get_category_data_layout(self):
        # 定义布局类型和对应的判断逻辑
        layout_types = {
            'Square': lambda aspect_ratio: aspect_ratio == 1,
            'Wide': lambda aspect_ratio: aspect_ratio < 1,
            'Tall': lambda aspect_ratio: aspect_ratio > 1
        }

        # 判断布局类型
        layout = next((name for name, check in layout_types.items() if check(self.img_instance.aspect_ratio)),
                      'Unknown')

        return {
            'layout': ['layout', layout]
        }

    def get_category_data_size(self):
        """
        获取分类数据。
        """
        # 获取图片最大尺寸
        max_dimension = max(self.img_instance.wid, self.img_instance.height)

        # 定义尺寸分类的阈值
        size_thresholds = {
            'Small': 512,
            'Medium': 1024,
            'Large': 2048
        }

        # 根据阈值判断图片尺寸
        for size, threshold in size_thresholds.items():
            if max_dimension < threshold:
                break
        else:
            size = 'Extra Large'

        return {
            'size': ['size', size]
        }
