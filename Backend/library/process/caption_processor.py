import torch
from lavis.models import load_model_and_preprocess

from library.process.base_processor import ImageProcessor
from utilities.common import trace_function


class CaptionProcessor(ImageProcessor):
    # ... 其他方法 ...
    # def __init__(self, image_processor):

    def __init__(self, img=None):
        super().__init__(img)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.vis_processors, _ = load_model_and_preprocess(name="blip_caption", model_type="base_coco",
                                                                       is_eval=True,
                                                                       device=self.device)

    @trace_function
    def get(self, *args, **kwargs):
        """
        purpose: 对图片进行简单描述
        params:
            instance: the image django instance
            force: identify whether you need to process this instance even this instance already processed
        return:
            caption: the caption of the image
        """

        device = self.device
        raw_image = self.img_pil.convert("RGB")
        # loads BLIP caption base model, with finetuned checkpoints on MSCOCO captioning dataset.
        # this also loads the associated image processors

        # preprocess the image
        # vis_processors stores image transforms for "train" and "eval" (validation / testing / inference)
        image = self.vis_processors["eval"](raw_image).unsqueeze(0).to(device)
        # generate caption
        caption = self.model.generate({"image": image})

        data = {
            'caption': {'caption': ''.join(caption)}  # 将列表转成字符串
        }

        return data
