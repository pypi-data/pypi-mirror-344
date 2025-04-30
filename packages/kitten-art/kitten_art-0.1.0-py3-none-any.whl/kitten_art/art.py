from .data import KITTENS
import random

def draw_kitten():
    """Рисует стандартного котика"""
    kitten_art = r"""
 /\_/\  
( o.o ) 
 > ^ <
    """
    print(kitten_art)

def get_random_kitten():
    """Возвращает случайного котика"""
    return random.choice(KITTENS)