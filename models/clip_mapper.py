import pytorch_lightning as pl
from torch import nn
import open_clip
from PIL import Image
import torch
import lpips

percept = lpips.PerceptualLoss(model='net-lin', net='vgg', use_gpu=False)
import torch.nn.functional as F
from torchvision import transforms

device = 'mps' # Yes I use macbook... I know it's bad (:


class mapper_train(pl.LightningModule):
    def __init__(self, decoder):
        super().__init__()
        self.decoder = decoder
        self.decoder.to(device)
        self.decoder.eval()
        self.mapper = nn.Sequential(
            nn.Linear(768, 768), nn.GELU(),
            nn.Linear(768, 768), nn.GELU(),
            nn.Linear(768, 768), nn.GELU(),
        )
        self.mapper.to(device)
        self.head = nn.Sequential(
            nn.Linear(768, 256), nn.GELU(),
        )
        self.head.to(device)
        model, _, _ = open_clip.create_model_and_transforms('ViT-L-14', pretrained='laion2b_s32b_b82k')
        self.model = model.visual
        self.model.eval()
        self.model.to(device)
        self.preprocess = transforms.Compose([
            transforms.Resize(size=224, interpolation=Image.BICUBIC, antialias=True),
            transforms.CenterCrop(size=(224, 224)),
        ])

    def get_image_from_encoding(self, encoding):
        self.mapper.eval()
        self.head.eval()
        self.decoder.eval()
        with torch.no_grad():
            z_predict = self.mapper(encoding) + encoding
            z_predict = self.head(z_predict)
            generated_image = self.decoder(z_predict)[0]
            return generated_image

    def z_from_encoding(self, encoding):
        self.mapper.eval()
        self.head.eval()
        with torch.no_grad():
            z_predict = self.mapper(encoding) + encoding
            z_predict = self.head(z_predict)
            return z_predict

    def z_to_image(self, z):
        self.decoder.eval()
        with torch.no_grad():
            generated_image = self.decoder(z)[0]
            return generated_image

    def training_step(self, batch, batch_idx):
        imgs, _ = batch
        imgs.to(device)
        image_features = self.model(imgs)
        z_predict = self.mapper(image_features) + image_features
        z_predict = self.head(z_predict)
        generated_image = self.decoder(z_predict)[0]
        processed_generated_image = self.preprocess(generated_image)
        processed_image_features = self.model(processed_generated_image)

        if batch_idx % 100 == 0:
            self.logger.log_image(key="recounstraction ,original", images=[processed_generated_image, imgs])

        clip_sim = F.cosine_similarity(processed_image_features, image_features).abs().mean()
        clip_mse = F.mse_loss(processed_image_features, image_features).mean()

        images_mse = F.mse_loss(imgs, processed_generated_image).mean()
        lpips = percept(imgs, processed_generated_image).mean()

        total_loss = images_mse + lpips + clip_mse - clip_sim * 0.6
        if batch_idx % 5 == 0:
            self.log_dict({'total_loss': total_loss,
                           'lpips': lpips, 'images_mse': images_mse, 'clip_mse': clip_mse, 'clip_sim': clip_sim})

        if batch_idx % 50 == 0:
            print({'total_loss': total_loss,
                   'lpips': lpips, 'images_mse': images_mse, 'clip_mse': clip_mse, 'clip_sim': clip_sim})

        return total_loss