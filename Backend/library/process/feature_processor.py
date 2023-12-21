import clip
import torch

from library.process.base_processor import ImageProcessor
from utilities.common import trace_function


class FeatureProcessor(ImageProcessor):
    # ... 其他方法 ...
    # def __init__(self, image_processor):

    def __init__(self, img=None):
        super().__init__(img)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    @trace_function
    def get(self, *args, **kwargs):
        device = self.device
        raw_image = self.img_pil

        image = self.preprocess(raw_image).unsqueeze(0).to(device)

        with torch.no_grad():
            image_features = self.model.encode_image(image)
            print("Image features:", image_features.shape)
            # text_features = model.encode_text(text)
            # print("Text features:", text_features.shape)

        #     logits_per_image, logits_per_text = model(image, text)
        #     probs = logits_per_image.softmax(dim=-1).cpu().numpy()
        # print("Label probs:", probs)

        # save the feature to the database
        embedding = image_features.cpu().numpy().tobytes()
        data={
            'feature': {'embedding': embedding}
        }
        return data
