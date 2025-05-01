"""
Shadowstep - UI Testing Framework powered by Appium Python Client
"""

# Импортируем функцию для получения логгера из utils
from shadowstep.utils import get_logger

# Основной класс фреймворка
from shadowstep.shadowstep import Shadowstep

# Базовые классы для страниц и элементов
from shadowstep.page_base import PageBaseShadowstep
from shadowstep.element.element import Element

# Экспортируем публичные классы и объекты
__all__ = ['Shadowstep', 'PageBaseShadowstep', 'Element', 'get_logger']

# Версия фреймворка
__version__ = '0.16.44'
