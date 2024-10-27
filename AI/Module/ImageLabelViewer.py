import os
import cv2

class ImageLabelViewer:
    '''
        Просмотр изображений с масской

        - path - путь к папке
        - display_size - размер изображения
        -------------------------------------------
        - run_viewer - запуск
    '''

    def __init__(self, path, display_size=(1280, 880)):
        self.images_folder = os.path.join(path, "images")
        self.labels_folder = os.path.join(path, "label")
        
        self.images_files = sorted(os.listdir(self.images_folder))
        self.labels_files = sorted(os.listdir(self.labels_folder))
        
        if len(self.images_files) != len(self.labels_files):
            raise ValueError("Количество файлов в папках не совпадает!")
        
        self.current_index = 0
        self.display_size = display_size

    def _draw_bounding_boxes(self, image, label_file):
        h, w = image.shape[:2]

        with open(label_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                class_id = int(parts[0])
                x_center, y_center, box_width, box_height = map(float, parts[1:])

                # Переводим центр и размеры в абсолютные координаты
                x_min = int((x_center - box_width / 2) * w)
                y_min = int((y_center - box_height / 2) * h)
                x_max = int((x_center + box_width / 2) * w)
                y_max = int((y_center + box_height / 2) * h)

                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)
        return image

    def _show_image_with_boxes(self):
        # Получаем текущее изображение и соответствующий файл меток
        img_file = os.path.join(self.images_folder, self.images_files[self.current_index])
        lbl_file = os.path.join(self.labels_folder, self.labels_files[self.current_index])
        image = cv2.imread(img_file)
        
        cv2.putText(image, f"image-{self.current_index}", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 4)
        cv2.putText(image, "A-back, d-next, esc-exit", (10,120), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 4)

        image_with_boxes = self._draw_bounding_boxes(image, lbl_file)
        image_with_boxes = cv2.resize(image_with_boxes, self.display_size)
        cv2.imshow(f"Image", image_with_boxes)

    def _next_image(self):
        # Переход к следующему изображению
        self.current_index = (self.current_index + 1) % len(self.images_files)
        self._show_image_with_boxes()
    
    def _prev_image(self):
        # Переход к предыдущему изображению
        self.current_index = (self.current_index - 1) % len(self.images_files)
        self._show_image_with_boxes()

    def run_viewer(self):
        # Показать первое изображение
        self._show_image_with_boxes()

        while True:
            # Ожидаем нажатие клавиши
            key = cv2.waitKey(0)

            # Обработка нажатия клавиш
            if key == ord('d'):  # 'n' - следующее изображение
                self._next_image()
            elif key == ord('a'):  # 'p' - предыдущее изображение
                self._prev_image()
            elif key == 27:  # ESC - выход
                break

        # Закрываем окно
        cv2.destroyAllWindows()