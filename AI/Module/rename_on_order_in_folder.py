import os

# Переименовать изображения и метки по порядку
def rename_on_order_in_folder(path, nweName = "img_"):
    '''
        Переименовать все файлы в папке попорядку

        - path - путь
        - nweName - имя для переименования
    '''
    images_folder = f"{path}images"
    labels_folder = f"{path}label"

    images_files = sorted(os.listdir(images_folder))
    labels_files = sorted(os.listdir(labels_folder))

    if len(images_files) != len(labels_files):
        print("Количество файлов в папках не совпадает!")
    else:
        # Переименовываем файлы в обоих папках
        for i, (img_file, lbl_file) in enumerate(zip(images_files, labels_files), start=1):
            # Новый формат имени
            new_name = f"{nweName}{i}"
            
            # Определяем расширения файлов
            img_ext = os.path.splitext(img_file)[1]
            lbl_ext = os.path.splitext(lbl_file)[1]

            # Полные пути к старым и новым файлам
            old_img_path = os.path.join(images_folder, img_file)
            new_img_path = os.path.join(images_folder, f"{new_name}{img_ext}")
            
            old_lbl_path = os.path.join(labels_folder, lbl_file)
            new_lbl_path = os.path.join(labels_folder, f"{new_name}{lbl_ext}")

            # Переименовываем файлы
            os.rename(old_img_path, new_img_path)
            os.rename(old_lbl_path, new_lbl_path)

        print("Файлы успешно переименованы!")