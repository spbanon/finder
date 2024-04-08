from PIL import Image
import requests
import open_clip
from transformers import CLIPProcessor, CLIPModel
import torch
import os
class ClipPipeline:
    def __init__(self) -> None: 
        self.device = 'cpu'
        self.model, _, self.preprocess = open_clip.create_model_and_transforms('ViT-L-14', pretrained='datacomp_xl_s13b_b90k')
        self.tokenizer = open_clip.get_tokenizer('ViT-L-14')
    
    def __call__(self, dir: str, describe: str) -> dict:
        print(f'dir = {dir}, describe = {describe}')
        res = {}
        for paths in os.listdir(dir):
            print(paths)
            image = self.preprocess(Image.open(f'{dir}/{paths}')).unsqueeze(0).to(self.device)
            text = self.tokenizer([f'the photo is a {describe}', f'the photo is of not a {describe}']).to(self.device)

            with torch.no_grad():
                image_features = self.model.encode_image(image)
                text_features = self.model.encode_text(text)

            # Нормализация признаков
            image_features /= image_features.norm(dim=-1, keepdim=True)
            text_features /= text_features.norm(dim=-1, keepdim=True)

            # Вычисление сходства между изображением и текстом
            similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
            print(similarity)
            # Получение процента соответствия
            percent_match = similarity[0, 0].item()
            if similarity[0][0] > similarity[0][1] or len(describe) < 5 or describe == None:
                res[paths] = percent_match
        return res
