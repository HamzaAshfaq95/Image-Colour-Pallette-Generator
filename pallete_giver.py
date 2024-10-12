import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

class PalleteGiver:
    def __init__(self, img):
        self.img = img

    def get_pallete(self):
        try:
            # Open the image
            img = Image.open(self.img)
            # Convert to RGB if not already in that mode
            img.convert("RGB")
            # Convert the image to a NumPy array
            img_array = np.array(img)
            # Reshape the array to a 2D array of pixels
            pixels = img_array.reshape(-1, 3)
            # Use K-means clustering to find the dominant colors
            kmeans = KMeans(n_clusters=10)
            kmeans.fit(pixels)
            # Get the RGB values of the cluster centers
            pallete = kmeans.cluster_centers_
            # Convert the palette to integers
            pallete = pallete.astype(int)
            return pallete
        except Exception as e:
            print(f"An error occurred: {e}")
            return None