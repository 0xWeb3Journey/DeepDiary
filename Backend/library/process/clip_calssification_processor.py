import torch
from lavis.models import load_model_and_preprocess

from library.process.base_processor import ImageProcessor
from utilities.common import trace_function


# from django.core.files import File
# from utils.mcs_storage import upload_file_pay


# from django.core.files import File
# from utils.mcs_storage import upload_file_pay


class ClipClassificationProcessor(ImageProcessor):
    # ... 其他方法 ...
    # def __init__(self, image_processor):

    def __init__(self, img=None):
        super().__init__(img)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.cls_names = [
                "interior objects",
                "nature landscape",
                "beaches seaside",
                "events parties",
                "food drinks",
                "paintings art",
                "pets animals",
                "text visuals",
                "sunrises sunsets",
                "cars vehicles",
                "macro flowers",
                "streetview architecture",
                "people portraits",
            ]


    @trace_function
    def get(self, *args, **kwargs):
        data={}

        raw_image = self.img_pil.convert("RGB")
        # Load CLIP feature extractor model,
        # vis_processors, txt_processors = load_model_and_preprocess(
        # "clip_feature_extractor", model_type="ViT-B-32", is_eval=True, device=device)
        model, vis_processors, txt_processors = load_model_and_preprocess("clip_feature_extractor",
                                                                          model_type="ViT-B-32", is_eval=True,
                                                                          device=self.device)
        # Optional to use prompts to guide the model
        cls_names = [txt_processors["eval"](cls_nm) for cls_nm in self.cls_names]

        image = vis_processors["eval"](raw_image).unsqueeze(0).to(self.device)
        #  Extract image embedding and class name embeddings
        sample = {"image": image, "text_input": cls_names}
        clip_features = model.extract_features(sample)
        image_features = clip_features.image_embeds_proj
        text_features = clip_features.text_embeds_proj

        # Matching image embeddings with each class name embeddings
        sims = (image_features @ text_features.t())[0] / 0.01
        probs = torch.nn.Softmax(dim=0)(sims).tolist()

        prob_max = max(probs)
        cla_name = cls_names[probs.index(prob_max)]
        for cls_nm, prob in zip(cls_names, probs):
            if prob > 0.25:
                print(f"{cls_nm}: \t {prob:.3%}")
                # 3. save the result
                field_list = [
                    'clip_categories',
                    cls_nm,
                ]
        data = [['clip_classification', cls_nm] for cls_nm, prob in zip(cls_names, probs) if prob > 0.25]
        return {'clip_classification': data}
