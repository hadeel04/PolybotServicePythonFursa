from pathlib import Path
from matplotlib.image import imread, imsave
import random


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class Img:

    def __init__(self, path):
        """
        Do not change the constructor implementation
        """
        self.path = Path(path)
        self.data = rgb2gray(imread(path)).tolist()

    def save_img(self):
        """
        Do not change the below implementation
        """
        new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
        imsave(new_path, self.data, cmap='gray')
        return new_path

    def blur(self, blur_level=16):

        height = len(self.data)
        width = len(self.data[0])
        filter_sum = blur_level ** 2

        result = []
        for i in range(height - blur_level + 1):
            row_result = []
            for j in range(width - blur_level + 1):
                sub_matrix = [row[j:j + blur_level] for row in self.data[i:i + blur_level]]
                average = sum(sum(sub_row) for sub_row in sub_matrix) // filter_sum
                row_result.append(average)
            result.append(row_result)

        self.data = result

    def contour(self):
        for i, row in enumerate(self.data):
            res = []
            for j in range(1, len(row)):
                res.append(abs(row[j-1] - row[j]))

            self.data[i] = res

    def rotate(self):
        height = len(self.data)
        width = len(self.data[0])

        rotated_data = [[0 for j in range(height)] for i in range(width)]

        for i in range(height):
            for j in range(width):
                rotated_data[j][height - i - 1] = self.data[i][j]

        self.data = rotated_data

    def salt_n_pepper(self):
        height = len(self.data)
        width = len(self.data[0])

        for i in range(height):
            for j in range(width):
                random_value = random.random()
                if random_value < 0.2:
                    self.data[i][j] = 255  # Salt (maximum intensity)
                elif random_value > 0.8:
                    self.data[i][j] = 0  # Pepper (minimum intensity)

    def concat(self, other_img, direction='horizontal'):
        if direction == 'horizontal':
            if len(self.data) != len(other_img.data):
                raise RuntimeError("Images have different heights, cannot concatenate horizontally.")

            height = len(self.data)
            width1 = len(self.data[0])
            width2 = len(other_img.data[0])

            concatenated_data = [[0 for j in range(width1 + width2)] for i in range(height)]

            for i in range(height):
                for j in range(width1):
                    concatenated_data[i][j] = self.data[i][j]
                for j in range(width2):
                    concatenated_data[i][j + width1] = other_img.data[i][j]

            self.data = concatenated_data

        elif direction == 'vertical':
            if len(self.data[0]) != len(other_img.data[0]):
                raise RuntimeError("Images have different widths, cannot concatenate vertically.")

            height1 = len(self.data)
            height2 = len(other_img.data)
            width = len(self.data[0])

            concatenated_data = [[0 for j in range(width)] for i in range(height1 + height2)]

            for i in range(height1):
                for j in range(width):
                    concatenated_data[i][j] = self.data[i][j]
            for i in range(height2):
                for j in range(width):
                    concatenated_data[i + height1][j] = other_img.data[i][j]

            self.data = concatenated_data

        else:
            raise ValueError("Invalid direction. Must be 'horizontal' or 'vertical'.")

    def segment(self):
        height = len(self.data)
        width = len(self.data[0])

        for i in range(height):
            for j in range(width):
                if self.data[i][j] > 100:
                    self.data[i][j] = 255  # White pixel
                else:
                    self.data[i][j] = 0  # Black pixel