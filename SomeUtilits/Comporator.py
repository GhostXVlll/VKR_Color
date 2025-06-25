import os
from PIL import Image
import numpy as np


def load_images(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img = Image.open(os.path.join(folder, filename))
            images.append(img)
    return images

def resize_images(images, size=(320, 200)):
    resized_images = []
    for img in images:
        resized_img = img.resize(size)
        resized_images.append(resized_img)
    return resized_images

def convert_to_LAB(images):
    LAB_images = []
    for img in images:
        LAB_img = img.convert("LAB")
        LAB_images.append(LAB_img)
    return LAB_images

def compare_images(original, images):
    results_psnr = []
    results_mse = []
    original_array = np.array(original)
    for img in images:
        img_array = np.array(img)
        #print("orig: ", original_array)
        #print("colored: ", img_array)
        diff1 = np.abs(original_array - img_array)
        MSE = np.mean(diff1**2)
        PSNR = 10 * np.log10(255**2 / MSE)
        results_psnr.append(PSNR)
        results_mse.append(MSE)
    return results_psnr, results_mse

def main():
    folder = "E:/Study/Magister 2 course/Magister VKR/Results_photos/"
    paths = os.listdir(folder)
    images = load_images(folder)
    resized_images = resize_images(images)
    LAB_images = convert_to_LAB(resized_images)

    original = LAB_images[0]
    results_psnr, results_mse = compare_images(original, LAB_images[0:])

    for i, result in enumerate(results_psnr):
        print(f"PSNR {paths[i]}: {result}, MSE: {results_mse[i]}")

if __name__ == "__main__":
    main()
