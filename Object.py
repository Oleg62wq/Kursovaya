import math
import numpy as np
import matplotlib.pyplot as plt

class Rectangle:
    def __init__(self, center_x, center_y, width=3, height=2, angle=0):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.angle = angle

    def get_corners(self):
        half_width = self.width / 2
        half_height = self.height / 2

        corners = [
            (-half_width, half_height),   # Верхний левый
            (half_width, half_height),    # Верхний правый
            (half_width, -half_height),   # Нижний правый
            (-half_width, -half_height)   # Нижний левый
        ]

        angle_rad = math.radians(self.angle)

        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        rotated_corners = []
        for x, y in corners:
            rotated_x = self.center_x + (x * cos_a - y * sin_a)
            rotated_y = self.center_y + (x * sin_a + y * cos_a)
            rotated_corners.append((rotated_x, rotated_y))

        return rotated_corners

    def __repr__(self):
        return f"Rectangle(center=({self.center_x}, {self.center_y}), width={self.width}, height={self.height}, angle={self.angle})"
