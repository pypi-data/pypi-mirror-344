import requests
from PIL import Image
import os
import shutil
import warnings

def cur(value, from_currency, to_currency):
    """Конвертирует валюту. Пример: rifcomp.cur(100, 'rub', 'usd')"""
    url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{from_currency.lower()}/{to_currency.lower()}.json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        rate = response.json()[to_currency.lower()]
        return value * rate
    except requests.exceptions.RequestException as e:
        warnings.warn(f"Ошибка API: {e}. Используется фиксированный курс (1 USD = 90 RUB).", RuntimeWarning)
        fixed_rates = {"usd": 90, "eur": 100, "rub": 1}
        return value * (fixed_rates.get(to_currency.lower(), 1) / fixed_rates.get(from_currency.lower(), 1))

def units(value, from_unit, to_unit):
    """Конвертирует единицы. Пример: rifcomp.units(5, 'km', 'm') -> 5000"""
    convert_table = {
        "km": {"m": 1000, "cm": 100000},
        "m": {"km": 0.001, "cm": 100},
        "rub": {"kop": 100},
        "kop": {"rub": 0.01},
        "kg": {"g": 1000},
        "g": {"kg": 0.001},
    }
    try:
        return value * convert_table[from_unit][to_unit]
    except KeyError:
        raise ValueError(f"Неподдерживаемая конвертация: {from_unit} → {to_unit}")

class Files:
    def __init__(self, input_path, output_path):
        """Конвертирует файлы. Пример: rifcomp.Files('img.jpg', 'img.png')"""
        self.input_path = input_path
        self.output_path = output_path
        self.supported_formats = ['jpg', 'jpeg', 'png', 'webp', 'ico', 'bmp']
        
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Файл {input_path} не найден!")
        
        if os.path.abspath(input_path) == os.path.abspath(output_path):
            warnings.warn("Входной и выходной файлы одинаковы. Производится копирование.", UserWarning)
            shutil.copyfile(input_path, output_path)
            return
        
        try:
            self._convert()
        except Exception as e:
            raise ValueError(f"Ошибка конвертации: {e}")

    def _convert(self):
        input_ext = os.path.splitext(self.input_path)[1][1:].lower()
        output_ext = os.path.splitext(self.output_path)[1][1:].lower()
        
        if input_ext not in self.supported_formats or output_ext not in self.supported_formats:
            raise ValueError(f"Неподдерживаемый формат. Доступно: {', '.join(self.supported_formats)}")
        
        if input_ext == output_ext:
            shutil.copyfile(self.input_path, self.output_path)
        else:
            img = Image.open(self.input_path)
            img.save(self.output_path, format=output_ext.upper())