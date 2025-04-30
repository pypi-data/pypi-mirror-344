import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import os
import shutil
import json
from typing import List, Dict, Any, Optional, Callable, Union

class DataEnv:
    def __init__(self, filename='dataenv.json'):
        self.filename = filename
        self.load()

    def load(self):
        """Загружает данные из файла в переменные окружения."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    os.environ[key] = value

    def save(self):
        """Сохраняет текущие переменные окружения в файл."""
        data = {key: os.environ[key] for key in os.environ if key.startswith('DATAENV_')}
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def set_variable(self, key: str, value: str):
        """Устанавливает переменную в окружение."""
        os.environ[key] = value
        self.save()

    def get_variable(self, key: str) -> Union[str, None]:
        """Получает значение переменной из окружения."""
        return os.environ.get(key)

    def delete_variable(self, key: str):
        """Удаляет переменную из окружения."""
        if key in os.environ:
            del os.environ[key]
            self.save()

    def sort_data(self, data: List[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
        """Сортирует список словарей по заданному ключу."""
        return sorted(data, key=lambda x: x.get(key))

    def search_data(self, data: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Ищет данные по заданному запросу."""
        return [item for item in data if query.lower() in json.dumps(item).lower()]

    def format_data(self, data: List[Dict[str, Any]]) -> str:
        """Форматирует данные в виде JSON строки."""
        return json.dumps(data, indent=4)

    def group_data(self, data: List[Dict[str, Any]], key: str) -> Dict[Any, List[Dict[str, Any]]]:
        """Группирует данные по заданному ключу."""
        grouped = {}
        for item in data:
            grouped.setdefault(item[key], []).append(item)
        return grouped


class DataGroup:
    def __init__(self, name: str, data: List[Dict[str, Any]]):
        self.name = name
        self.data = data

    def delete_group(self):
        """Удаляет группу данных."""
        self.data.clear()
        self.name = None

    def count_unique(self, key: str) -> int:
        """Подсчитывает уникальные значения по заданному ключу."""
        return len(set(item[key] for item in self.data if key in item))

    def filter_data(self, condition: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        """Фильтрует данные по заданному условию."""
        return [item for item in self.data if condition(item)]

    def save_to_file(self, filename: str):
        """Сохраняет группу данных в JSON файл."""
        with open(filename, 'w') as f:
            json.dump(self.data, f)

    @staticmethod
    def load_from_file(filename: str) -> 'DataGroup':
        """Загружает группу данных из JSON файла."""
        with open(filename, 'r') as f:
            data = json.load(f)
        return DataGroup(name=filename, data=data)

    def aggregate(self, key: str, func: Callable[[List[Any]], Any]) -> Any:
        """Выполняет агрегирующую функцию по числовому полю."""
        values = [item[key] for item in self.data if key in item]
        return func(values)

    def export_to_csv(self, filename: str):
        """Экспортирует данные в CSV файл."""
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)

    def visualize(self, x_key: str, y_key: str):
        """Создает график на основе двух ключей."""
        df = pd.DataFrame(self.data)
        plt.figure(figsize=(10, 6))
        plt.scatter(df[x_key], df[y_key])
        plt.title(f'График {y_key} против {x_key}')
        plt.xlabel(x_key)
        plt.ylabel(y_key)
        plt.show()

    def inherit(self, keys: Optional[List[str]] = None) -> 'DataGroup':
        """Создает новую группу с унаследованными данными и/или ключами."""
        if keys is None:
            return DataGroup(name=f"{self.name}_inherited", data=self.data.copy())
        
        inherited_data = [{key: item[key] for key in keys if key in item} for item in self.data]
        return DataGroup(name=f"{self.name}_inherited", data=inherited_data)


class DataClass:
    def __init__(self, name: str):
        self.name = name
        self.groups: List[DataGroup] = []

    def add_group(self, group: DataGroup):
        """Добавляет новую группу данных в класс."""
        self.groups.append(group)

    def remove_group(self, group_name: str):
        """Удаляет группу данных по имени."""
        self.groups = [group for group in self.groups if group.name != group_name]

    def get_group(self, group_name: str) -> Optional[DataGroup]:
        """Получает группу данных по имени."""
        for group in self.groups:
            if group.name == group_name:
                return group
        return None

    def summarize(self) -> Dict[str, Any]:
        """Возвращает сводную информацию по всем группам."""
        summary = {}
        for group in self.groups:
            summary[group.name] = {
                "count": len(group.data),
                "unique_values": {key: group.count_unique(key) for key in group.data[0].keys() if group.data}
            }
        return summary

    def visualize_all(self):
        """Создает графики для всех групп в классе."""
        for group in self.groups:
            print(f"Визуализация для группы: {group.name}")
            if group.data:
                keys = list(group.data[0].keys())
                if len(keys) >= 2:
                    group.visualize(keys[0], keys[1])

    def inherit_groups(self, keys: Optional[List[str]] = None) -> 'DataClass':
        """Создает новый класс с унаследованными группами и/или ключами."""
        new_class = DataClass(name=f"{self.name}_inherited")
        for group in self.groups:
            new_group = group.inherit(keys)
            new_class.add_group(new_group)
        return new_class


class DataAnalyzer:
    def __init__(self, data):
        self.data = pd.DataFrame(data)
        self.metadata = {
            'columns': self.data.columns.tolist(),
            'dtypes': self.data.dtypes.to_dict(),
            'missing_values': self.data.isnull().sum().to_dict(),
            'statistics': {},
            'creation_time': datetime.now(),
            'last_updated': datetime.now(),
            'encoding': 'utf-8',
            'data_weight': self.calculate_data_weight()
        }
        self.update_statistics()

    def update_statistics(self):
        self.metadata['statistics'] = {
            'mean': self.data.mean().to_dict(),
            'median': self.data.median().to_dict(),
            'mode': self.data.mode().iloc[0].to_dict(),
            'std_dev': self.data.std().to_dict()
        }
        self.metadata['last_updated'] = datetime.now()

    def calculate_data_weight(self):
        return self.data.memory_usage(deep=True).sum()

    def normalize(self):
        self.data = (self.data - self.data.min()) / (self.data.max() - self.data.min())

    def standardize(self):
        self.data = (self.data - self.data.mean()) / self.data.std()

    def fill_missing(self, method='mean'):
        if method == 'mean':
            self.data.fillna(self.data.mean(), inplace=True)
        elif method == 'median':
            self.data.fillna(self.data.median(), inplace=True)
        elif method == 'ffill':
            self.data.fillna(method='ffill', inplace=True)

        self.metadata['missing_values'] = self.data.isnull().sum().to_dict()
        self.update_statistics()

    def calculate_statistics(self):
        return self.metadata['statistics']

    def plot_histogram(self, column):
        plt.figure(figsize=(10, 6))
        sns.histplot(self.data[column], bins=30, kde=True)
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.show()

    def plot_correlation_matrix(self):
        plt.figure(figsize=(12, 8))
        sns.heatmap(self.data.corr(), annot=True, fmt=".2f", cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.show()

    def plot_interactive_scatter(self, x_col, y_col):
        fig = px.scatter(self.data, x=x_col, y=y_col, title=f'Scatter plot of {x_col} vs {y_col}')
        fig.show()

    def filter_data(self, column, condition):
        return self.data[self.data[column] == condition]

    def aggregate_data(self, column, agg_func):
        return self.data.groupby(column).agg(agg_func)

    def save_to_csv(self, filename):
        self.data.to_csv(filename, index=False)

    def save_to_excel(self, filename):
        self.data.to_excel(filename, index=False)

    def encode_categorical(self, column):
        self.data = pd.get_dummies(self.data, columns=[column], drop_first=True)
        self.metadata['columns'] = self.data.columns.tolist()
        self.metadata['dtypes'] = self.data.dtypes.to_dict()

    def detect_outliers(self, column):
        Q1 = self.data[column].quantile(0.25)
        Q3 = self.data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return self.data[(self.data[column] < lower_bound) | (self.data[column] > upper_bound)]

    def plot_time_series(self, time_column, value_column):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data[time_column], self.data[value_column])
        plt.title(f'Time Series of {value_column}')
        plt.xlabel(time_column)
        plt.ylabel(value_column)
        plt.xticks(rotation=45)
        plt.grid()
        plt.show()

    def compare_datasets(self, other_data_analyzer):
        stats_self = self.calculate_statistics()
        stats_other = other_data_analyzer.calculate_statistics()
        
        comparison_df = pd.DataFrame({'Self': stats_self['mean'], 'Other': stats_other['mean']})
        return comparison_df

    @classmethod
    def from_csv(cls, filename):
        data = pd.read_csv(filename)
        return cls(data)

    @classmethod
    def from_excel(cls, filename):
        data = pd.read_excel(filename)
        return cls(data)

    # Методы для работы с файлами
    def save_file(self, file_path):
        """Сохранение любого файла по указанному пути."""
        if os.path.isfile(file_path):
            shutil.copy(file_path, os.path.join(os.getcwd(), os.path.basename(file_path)))
            print(f"Файл {file_path} успешно сохранен.")
        else:
            print(f"Файл {file_path} не найден.")

    def load_file(self, file_path):
        """Загрузка любого файла по указанному пути."""
        if os.path.isfile(file_path):
            shutil.copy(file_path, os.path.join(os.getcwd(), os.path.basename(file_path)))
            print(f"Файл {file_path} успешно загружен.")
            return os.path.basename(file_path)
        else:
            print(f"Файл {file_path} не найден.")
            return None
