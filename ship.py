import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    # 管理飞船的类
    def __init__(self,ai_game):
        # 初始化飞船并设置其初试位置
        # 需要让Ship 继承Sprite ，以便创建飞船编组
        super().__init__()
        # 处理矩形（rect 对象）
        self.screen = ai_game.screen
        # 给Ship 类添加属性settings ，以便能够在update() 中使用它
        self.settings = ai_game.settings
        # 使用方法get_rect() 访问屏幕的属性rect ，并将其赋给了self.screen_rect ，这让我们能够将飞船放到屏幕的正确位置。
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其外接矩形
        # 调用pygame.image.load() 加载图像
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 对于每艘新飞船，都将其放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 在飞船的属性x中存储小数值。
        # 使用函数float() 将self.rect.x 的值转换为小数，并将结果赋给self.x
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        # 根据移动标志调整飞船位置
        # 更新飞船而不是rect对象的x值。
        # self.rect.right 返回飞船外接矩形右边缘的x坐标
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # if self.moving_up and self.rect.top < self.screen_rect.top:
        #     self.y += self.settings.ship_speed
        # if self.moving_down and self.rect.bottom > 0 :
        #     self.y -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        # 根据self.x更新rect对象。
        self.rect.x = self.x
        self.rect.y = self.y
        # if self.moving_right:
        #     self.rect.x += 1
        # # elif将会使当左右同时按下时，使得右键一直会处于优先状态
        # if self.moving_left:
        #     self.rect.x -= 1

    def blitme(self):
        # 在指定位置绘制飞船
        # 定义了方法blitme() ，它将图像绘制到self.rect 指定的位置。
        # blit：位块传送; 位块传输
        self.screen.blit(self.image ,self.rect )

    def center_ship(self):
        # 让飞船在屏幕底端居中
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)