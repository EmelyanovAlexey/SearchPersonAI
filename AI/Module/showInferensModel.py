import matplotlib.pyplot as plt

def load_labels(label_path):
    """
    Загружает метки из текстового файла (формат YOLO: class x_center y_center width height)
    """
    boxes = []
    with open(label_path, 'r') as f:
        for line in f.readlines():
            parts = line.strip().split()
            cls = int(parts[0])  # Класс
            x_center, y_center, w, h = map(float, parts[1:])
            boxes.append((cls, x_center, y_center, w, h))
    return boxes

def plot_image_with_boxes(img, boxes, ax, title):
    """
    Отображает изображение с прямоугольниками вокруг объектов.
    """
    ax.imshow(img)
    ax.set_title(title)
    for box in boxes:
        cls, x_center, y_center, w, h = box
        x1 = (x_center - w / 2) * img.width
        y1 = (y_center - h / 2) * img.height
        x2 = (x_center + w / 2) * img.width
        y2 = (y_center + h / 2) * img.height
        ax.add_patch(plt.Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, edgecolor='red', linewidth=2))
