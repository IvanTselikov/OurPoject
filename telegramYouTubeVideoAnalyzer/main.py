import cv2
import numpy

import pafy


# Функция загрузки изображения по переданному названию файла:
import sift as sift


def loading(filename: str) -> numpy.ndarray:  # Параметр с подсказкой типа.
    data = numpy.fromfile(filename, dtype=numpy.uint8)  # Загрузка файла как последовательности байт.
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)  # Разбор последовательности байт как изображения.
    if img is None:  # В случае некорректного распаривания изображения.
        raise IOError("Invalid image format.")
    return img


def get_video_by_url(url: str):
    pafy_video = pafy.new(url)
    best = pafy_video.getbest(preftype='mp4')
    insert = cv2.VideoCapture(best.url)
    return insert


video = get_video_by_url('https://www.youtube.com/watch?v=pDvx0CY0ghg')

# # Создаются с параметрами по умолчанию:
sift = cv2.SIFT.create()  # Создание детектора.
matcher = cv2.BFMatcher(cv2.NORM_L2)  # Создание сопоставителя.
#
sample = loading("google_icon.jpg")  # Загрузка образа для последующего поиска.
sample_gray = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)  # Преобразование загруженного образа в оттенки серого.

# Поиск списка точек и их дескрипторов для изображения - образа:
sample_pts, sample_descriptions = sift.detectAndCompute(sample_gray, None)

# Формирование массива углов по изображению - образу:
sample_corners = numpy.array([
    (0, 0),
    (sample.shape[1], 0),
    (sample.shape[1], sample.shape[0]),
    (0, sample.shape[0])
], dtype=numpy.float32).reshape(-1, 1, 2)

counter = 0

while True:
    # success, scene = scene_video.read()  # Покадровое чтение файла с признаком успешности/неудачи прочтение.
    success, scene = video.read()
    if not success:  # В случае неудачного прочтения кадра:
        print("Video ended")
        break
    scene_gray = cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY)  # Преобразование прочтенного кадра сцены в оттенки серого.

    # Поиск списка точек и их дескрипторов для прочтенного кадра - сцены:
    scene_pts, scene_descriptions = sift.detectAndCompute(scene_gray, None)

    # Возвращение коллекции - кортежа совпадений:
    matches = matcher.knnMatch(sample_descriptions, scene_descriptions, k=2)
    good_matches = []  # Объявления списка для "удачных" совпадений:

    # Перебор совпадений:
    for m1, m2 in matches:
        # Применение критерия Лёве:
        if m1.distance < 0.9 * m2.distance:  # Если разница между первым и вторым совпадением составляет хотя бы 10%:
            good_matches.append(m1)  # Добавление точки в список "удачных" совпадений.

    # Строим списки пар точек - прообраз-образ:
    points_sample = []
    points_scene = []

    # Заполнение списков парами точек:
    for m in good_matches:
        points_sample.append(sample_pts[m.queryIdx].pt)  # Добавление точки в список точек для изображения - образа.
        points_scene.append(scene_pts[m.trainIdx].pt)  # Добавление точки в список точек для кадра - сцены.

    # Формирование массивов из сформировавшихся списков:
    points_sample = numpy.array(points_sample, dtype=numpy.float32).reshape(-1, 1, 2)
    points_scene = numpy.array(points_scene, dtype=numpy.float32).reshape(-1, 1, 2)

    # Формирование матриц проективного преобразования и успешных точек:
    matrix, point_mask = cv2.findHomography(points_sample, points_scene, cv2.RANSAC)

    # Применение преобразования к углам исходного объекта
    scene_corners = cv2.perspectiveTransform(sample_corners, matrix)
    scene_corners = scene_corners.reshape(1, -1, 2).astype(numpy.int32)

    # Рисуем многоугольник-рамку по этим углам:
    copy = scene.copy()  # Создание копии кадра - сцены.
    cv2.polylines(copy, scene_corners, True, (64, 255, 64), 2)

    # Демонстрируем результат:

    cv2.imshow("Detection", copy)  # Вывод результирующего кадра.
    counter += 1
    print(counter)
    if cv2.waitKeyEx(10) == 27:  # Если нажата клавиша ESC:
        print("Stopped by user")
        break

# scene_video.release()  # Закрытие видео файла.
video.release()
