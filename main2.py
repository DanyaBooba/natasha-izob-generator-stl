import numpy as np
import trimesh
from stl import mesh
from pybraille import convertText

def create_braille_dots(text, dot_height, dot_radius, dot_spacing):
    """
    Создает 3D модели точек Брайля для заданного текста.
    """
    braille = convertText(text)
    dots = []

    for row_idx, row in enumerate(braille.split('\n')):
        for col_idx, char in enumerate(row):
            if char == '1':
                x = col_idx * (dot_spacing + 2 * dot_radius)
                y = row_idx * (dot_spacing + 2 * dot_radius)
                z = 0
                dot = trimesh.creation.uv_sphere(radius=dot_radius)
                dot.apply_translation([x, y, z])
                dots.append(dot)

    if dots:
        return trimesh.util.concatenate(dots)
    else:
        return None

def create_base_plate(width, depth, height):
    """
    Создает базовую плашку с заданными размерами.
    """
    return trimesh.creation.box((width, depth, height))

def main():
    # Ввод параметров плашки
    width = float(input("Введите ширину плашки (мм): "))
    depth = float(input("Введите глубину плашки (мм): "))
    height = float(input("Введите высоту плашки (мм): "))

    # Ввод текста для преобразования в шрифт Брайля
    text = input("Введите текст для преобразования в шрифт Брайля: ")

    # Параметры точек Брайля
    dot_height = 0.5  # Высота точки (мм)
    dot_radius = 1.0  # Радиус точки (мм)
    dot_spacing = 2.5  # Расстояние между точками (мм)

    # Создание базовой плашки
    base_plate = create_base_plate(width, depth, height)

    # Создание точек Брайля
    braille_dots = create_braille_dots(text, dot_height, dot_radius, dot_spacing)

    if braille_dots is not None:
        # Смещение точек Брайля на плашку
        braille_dots.apply_translation([dot_radius, dot_radius, height])

        # Объединение плашки и точек Брайля
        final_mesh = trimesh.util.concatenate([base_plate, braille_dots])
    else:
        final_mesh = base_plate

    # Ввод имени файла для сохранения
    filename = input("Введите имя файла для сохранения (без расширения): ") + ".stl"

    # Экспорт модели в STL
    final_mesh.export(filename)
    print(f"Модель сохранена в файл {filename}")

if __name__ == "__main__":
    main()
