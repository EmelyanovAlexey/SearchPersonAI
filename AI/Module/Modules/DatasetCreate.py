import os
import random
import shutil
from tqdm import tqdm

class DatasetCreate:
    '''
        Формирования дата сета для обучения
    '''

    def __init__(self, path_winter, path_summer, path_train, path_valid, path_test):
        self.path_winter = path_winter
        self.path_summer = path_summer
        self.path_train = path_train
        self.path_valid = path_valid
        self.path_test = path_test

        self.data_index = 0

    def get_split_data_for_train(self, data, train = 7, valid = 2, test = 1):
        '''
            Делим на 3 части
        '''
        
        total_length = len(data)
        part1_length = (total_length * 7) // 10 
        part2_length = (total_length * 2) // 10 

        train = data[:part1_length]
        valid = data[part1_length:part1_length + part2_length]
        test = data[part1_length + part2_length:]

        return train, valid, test

    def reset_directory(self, directory):
        '''
            Отчищаем дерикторию
        '''

        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)

    def copy_data(self, data, path_from, path_to, isClear = False, text = ""):
        '''
            Копируем дата данные в нужную папку
        '''

        if isClear:
            self.reset_directory(f'{path_to}/images')
            self.reset_directory(f'{path_to}/label')

        for img in tqdm(data, desc=f"Копирование файлов {text}", unit="файл"):
            src_img = os.path.join(f'{path_from}/images', img)
            dst_img = os.path.join(f'{path_to}/images', f'{self.data_index}.jpg')
            shutil.copy(src_img, dst_img)

            # Находим соответствующую метку
            label_name = img.replace('.jpg', '.txt')
            src_label = os.path.join(f'{path_from}/label', label_name)
            dst_label = os.path.join(f'{path_to}/label', f'{self.data_index}.txt')
            shutil.copy(src_label, dst_label)

            self.data_index += 1

    def create_data_for_dataset(self):
        '''
            Формирвоание данных для обучения
        '''

        files_winter_images = os.listdir(f'{self.path_winter}images')
        files_summer_images = os.listdir(f'{self.path_summer}images')

        # перемешали 
        random.shuffle(files_winter_images)
        random.shuffle(files_summer_images)

        train_w, valid_w, test_w = self.get_split_data_for_train(files_winter_images)
        train_s, valid_s, test_s = self.get_split_data_for_train(files_summer_images)

        self.data_index = 0
        self.copy_data(train_w, self.path_winter, self.path_train, True, text="train зимняя")
        self.copy_data(train_s, self.path_summer, self.path_train, False, text="train зимняя")

        self.data_index = 0
        self.copy_data(valid_w, self.path_winter, self.path_valid, True, text="valid зимняя")
        self.copy_data(valid_s, self.path_summer, self.path_valid, False, text="valid зимняя")

        self.data_index = 0
        self.copy_data(test_w, self.path_winter, self.path_test, True, text="test зимняя")
        self.copy_data(test_s, self.path_summer, self.path_test, False, text="test зимняя")
