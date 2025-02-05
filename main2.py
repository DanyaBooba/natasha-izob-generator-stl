import numpy as np
from stl import mesh
import trimesh
import pybraille

# Карта точек Брайля (6 точек в каждой букве)
BRAILLE_DOTS = {
    "⠁": [1, 0, 0, 0, 0, 0], "⠃": [1, 1, 0, 0, 0, 0], "⠉": [1, 0, 0, 1, 0, 0],
    "⠙": [1, 0, 0, 1, 1, 0], "⠑": [1, 0, 0, 0, 1, 0], "⠋": [1, 1, 0, 1, 0, 0],
    "⠛": [1, 1, 0, 1, 1, 0], "⠓": [1, 1, 0, 0, 1, 0], "⠊": [0, 1, 0, 1, 0, 0],
    "⠚": [0, 1, 0, 1, 1, 0], "⠅": [1, 0, 1, 0, 0, 0], "⠇": [1, 1, 1, 0, 0, 0],
}

def generate_braille_plaque(width, depth, height, text, filename):
    dot_radius = 1.2
    dot_height = 1.5
    dot_spacing = 2.5
    margin = 5

    # Создание плашки
    base = trimesh.creation.box(extents=[width, depth, height])

    # Преобразование текста в Брайль
    braille_text = pybraille.convertText(text)

    dots = []
    x_offset = -width / 2 + margin
    y_offset = depth / 2 - margin

    for char in braille_text:
        braille_dots = BRAILLE_DOTS.get(char, [0, 0, 0, 0, 0, 0])  # Поиск символа Брайля

        for i in range(3):
            for j in range(2):
                index = i * 2 + j
                if braille_dots[index]:
                    dot = trimesh.creation.cylinder(radius=dot_radius, height=dot_height, sections=16)
                    dot.apply_translation([x_offset + j * dot_spacing, y_offset - i * dot_spacing, height])
                    dots.append(dot)

        x_offset += dot_spacing * 3

        if x_offset + margin > width / 2:
            x_offset = -width / 2 + margin
            y_offset -= dot_spacing * 4

    # Объединение объектов
    model = trimesh.util.concatenate([base] + dots)

    # Сохранение в STL
    model.export(filename + ".stl")
    print(f"Файл {filename}.stl создан.")

if __name__ == "__main__":
    width = 100
    depth = 50
    height = 5
    text = "hello"
    filename = "braille_plaque"

    generate_braille_plaque(width, depth, height, text, filename)
    print("Пример входных данных:")
    print(f"Ширина: {width}, Глубина: {depth}, Высота: {height}, Текст: '{text}', Имя файла: '{filename}'")
