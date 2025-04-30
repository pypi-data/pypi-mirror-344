import os
import cv2
import numpy as np
import random
from tqdm import tqdm
from typing import List, Optional, Union, Tuple
from torchvision.datasets import VisionDataset

class FastAugment:
    def __init__(self, preset: str = "simple"):
        self.preset = preset
        self.augmentations = self._get_augmentations()

    def _get_augmentations(self) -> List[callable]:
        if self.preset == "simple":
            return [
                self._random_horizontal_flip,
                self._random_rotate
            ]
        elif self.preset == "advanced":
            return [
                self._random_horizontal_flip,
                self._random_rotate,
                self._random_cutout,
                self._random_brightness_contrast
            ]
        else:
            raise ValueError(f"Unknown preset: {self.preset}")

    def _random_horizontal_flip(self, image: np.ndarray) -> np.ndarray:
        if random.random() < 0.5:
            return cv2.flip(image, 1)
        return image

    def _random_rotate(self, image: np.ndarray) -> np.ndarray:
        if random.random() < 0.5:
            angle = random.uniform(-30, 30)
            h, w = image.shape[:2]
            M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
            return cv2.warpAffine(image, M, (w, h))
        return image

    def _random_cutout(self, image: np.ndarray) -> np.ndarray:
        if random.random() < 0.5:
            h, w = image.shape[:2]
            for _ in range(8):
                y = random.randint(0, h)
                x = random.randint(0, w)
                size = random.randint(1, 8)
                y1 = max(0, y - size // 2)
                y2 = min(h, y + size // 2)
                x1 = max(0, x - size // 2)
                x2 = min(w, x + size // 2)
                image[y1:y2, x1:x2] = 0
        return image

    def _random_brightness_contrast(self, image: np.ndarray) -> np.ndarray:
        if random.random() < 0.3:
            beta = random.uniform(-0.2, 0.2) * 255
            alpha = random.uniform(0.8, 1.2)
            image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        return image

    def augment_image(self, image: np.ndarray, n: int = 5) -> List[np.ndarray]:
        variants = []
        for _ in range(n):
            img_copy = image.copy()
            selected_augs = random.sample(self.augmentations, k=random.randint(1, len(self.augmentations)))
            for aug in selected_augs:
                img_copy = aug(img_copy)
            variants.append(img_copy)
        return variants

    def augment_dataset(
        self,
        dataset: Union[VisionDataset, List[Tuple[np.ndarray, int]]],
        output_dir: Optional[str] = None,
        target_size: Optional[int] = None
    ) -> List[Tuple[np.ndarray, int]]:
        """
        Args:
            dataset: PyTorch dataset or list of (image, label)
            output_dir: if set, saves images as PNGs
            target_size: total number of augmented samples
        Returns:
            List of (augmented_image, label)
        """
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Convert PIL to numpy if needed
        images = []
        labels = []

        if isinstance(dataset, VisionDataset):
            for img, label in dataset:
                images.append(np.array(img))
                labels.append(label)
        else:
            images = [x[0] for x in dataset]
            labels = [x[1] for x in dataset]

        augmented = []
        original_size = len(images)
        target_size = target_size or original_size

        with tqdm(total=target_size) as pbar:
            while len(augmented) < target_size:
                for i in range(original_size):
                    if len(augmented) >= target_size:
                        break
                    img = images[i].copy()
                    label = labels[i]
                    aug_img = self.augment_n_random_versions(img, n=1)[0]  # Get 1 random variant
                    if output_dir:
                        save_path = os.path.join(output_dir, f"aug_{i}_{len(augmented)}.png")
                        cv2.imwrite(save_path, cv2.cvtColor(aug_img, cv2.COLOR_RGB2BGR))
                    augmented.append((aug_img, label))
                    pbar.update(1)
        return augmented
