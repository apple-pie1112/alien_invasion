import pygame
from pygame.sprite import Sprite
# 通过使用精灵（sprite），可将游戏中相关的元素编组，进而同时操作编组中的所有元素。

class Bullet(Sprite):
    # 管理飞船所发射子弹的类
    def __init__(self,ai_game):
        # 在飞船当前位置创建一个子弹对象
        super().__init__()
        # 调用了super() 来继承Sprite 。
        # super主要用来调用父类方法，显式调用父类，在子类中，一般会定义与父类相同的属性（数据属性，方法），
        # 从而来实现子类特有的行为。
        # 也就是说，子类会继承父类的所有的属性和方法，子类也可以覆盖父类同名的属性和方法。
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 在（0,0）处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        # 将子弹的rect.midtop 设置为飞船的rect.midtop 。
        # 这样子弹将从飞船顶部出发，看起来像是从飞船中射出的。
        self.rect.midtop = ai_game.ship.rect.midtop

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)

    def update(self):
        # 向上移动子弹
        # 更新表示子弹位置的小数值
        self.y -= self.settings.bullet_speed
        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        # 在屏幕上绘制子弹
        pygame.draw.rect(self.screen,self.color,self.rect)