import numpy as np
import trimesh
from stl import mesh
from pybraille import convertText

def create_braille_slab(width, depth, height, text, filename):
    # Преобразуем текст в шрифт Брайля
    braille_text = convertText(text)

    # Параметры символа Брайля
    dot_radius = 1.0
    dot_height = 2.0
    spacing = 4.0

    # Создаем пустую сцену
    scene = trimesh.Scene()

    # Создаем базовую плашку
    slab = trimesh.creation.box((width, depth, height))
    scene.add_geometry(slab)

    # Позиционируем точки Брайля на плашке
    for i, char in enumerate(braille_text):
        for j, dot in enumerate(char):
            if dot == '1':
                # Вычисляем позицию точки
                x = (i % (width // spacing)) * spacing + spacing / 2
                y = (i // (width // spacing)) * spacing + spacing / 2
                z = height / 2 + dot_height / 2

                # Создаем сферу для точки Брайля
                dot_sphere = trimesh.creation.uv_sphere(dot_radius)
                dot_sphere.apply_translation([x, y, z])

                # Добавляем сферу в сцену
                scene.add_geometry(dot_sphere)

    # Экспортируем сцену в STL файл
    scene.export(filename, file_type='stl')

if __name__ == "__main__":
    # Ввод параметров плашки
    width = float(input("Введите ширину плашки (мм): "))
    depth = float(input("Введите глубину плашки (мм): "))
    height = float(input("Введите высоту плашки (мм): "))
    text = input("Введите текст для преобразования в шрифт Брайля: ")
    filename = input("Введите имя файла для сохранения (без расширения): ") + ".stl"

    # Создаем плашку
    create_braille_slab(width, depth, height, text, filename)
    print(f"Плашка сохранена в файл {filename}")
