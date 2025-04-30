import os
import cv2
import numpy as np
import random
from typing import List

class FastAugment:
    def __init__(self, preset: str = "simple"):
        self.preset = preset
        self.augmentations = self._get_augmentations()

    def _get_augmentations(self) -> List[callable]:
        """Returns list of augmentation functions based on preset"""
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
        """Random horizontal flip with 50% probability"""
        if random.random() < 0.5:
            return cv2.flip(image, 1)
        return image

    def _random_rotate(self, image: np.ndarray) -> np.ndarray:
        """Random rotation between -30 and 30 degrees"""
        if random.random() < 0.5:
            angle = random.uniform(-30, 30)
            h, w = image.shape[:2]
            M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
            return cv2.warpAffine(image, M, (w, h))
        return image

    def _random_cutout(self, image: np.ndarray) -> np.ndarray:
        """Random cutout with 8 holes of max size 8x8 (50% probability)"""
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
        """Random brightness/contrast adjustment (30% probability)"""
        if random.random() < 0.3:
            beta = random.uniform(-0.2, 0.2) * 255  # Brightness
            alpha = random.uniform(0.8, 1.2)         # Contrast
            image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        return image

    def augment_n_random_versions(self, image: np.ndarray, n: int = 5) -> List[np.ndarray]:
        """
        Generate `n` randomly augmented versions of the input image.
        Each version applies a random subset (1 or more) of augmentations.
        """
        variants = []
        for _ in range(n):
            img_copy = image.copy()
            selected_augs = random.sample(self.augmentations, k=random.randint(1, len(self.augmentations)))
            for aug in selected_augs:
                img_copy = aug(img_copy)
            variants.append(img_copy)
        return variants
