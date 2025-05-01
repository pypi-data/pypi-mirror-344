import logging
import sys
import os
import inspect

# Настраиваем стандартный логгер Python
# Определение цветов для различных уровней логирования в терминале
RESET = '\033[0m'
GREEN = '\033[32m'
CYAN = '\033[36m'
YELLOW = '\033[33m'
RED = '\033[31m'
BOLD_RED = '\033[31;1m'

# Создаём кастомный форматтер с цветами
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': CYAN,
        'INFO': GREEN,
        'WARNING': YELLOW,
        'ERROR': RED,
        'CRITICAL': BOLD_RED,
    }

    def format(self, record):
        # Сохраняем исходные значения
        levelname = record.levelname
        name = record.name
        funcName = record.funcName
        lineno = record.lineno
        message = record.getMessage()

        # Форматируем с цветами
        date_fmt = GREEN + '%(asctime)s' + RESET
        level_fmt = '%(color)s%(levelname)-8s' + RESET
        name_fmt = CYAN + '%(name)s' + RESET + ':' + CYAN + '%(funcName)s' + RESET + ':' + CYAN + '%(lineno)d' + RESET
        msg_fmt = ' - %(color)s%(message)s' + RESET

        # Финальный формат
        fmt = f"{date_fmt} | {level_fmt}| {name_fmt}{msg_fmt}"
        
        formatter = logging.Formatter(fmt, datefmt='%Y-%m-%d %H:%M:%S')
        
        # Добавляем цвет в зависимости от уровня логирования
        record.color = self.COLORS.get(record.levelname, RESET)
        
        return formatter.format(record)

# Удаляем все стандартные обработчики
root_logger = logging.getLogger()
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Настраиваем консольный вывод с цветами
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(ColoredFormatter())
root_logger.addHandler(console_handler)
root_logger.setLevel(logging.INFO)

# Создаем экземпляр логгера для модуля shadowstep.utils
logger = logging.getLogger('shadowstep.utils')

# Экспортируем logger на уровень пакета
__all__ = ['logger']

# Функция получения логгера для других модулей
def get_logger(name=None):
    """
    Получить настроенный логгер для модуля.
    Если имя не указано, определяется автоматически.
    
    Args:
        name (str, optional): Имя логгера или None для автоопределения
        
    Returns:
        logging.Logger: Настроенный экземпляр логгера
    """
    if name is None:
        # Автоматически определить имя вызывающего модуля
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get('__name__')
    
    return logging.getLogger(name)
