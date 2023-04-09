import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    # 显示得分信息的类

    def __init__(self,ai_game):
        # 初始化显示得分涉及的属性
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)
        # 准备初试得分图像
        self.prep_score()

        # 准备包含最高得分和当前得分的图像
        self.prep_score()
        # 最高得分将与当前得分分开显示，因此需要编写一个新方法prep_high_score() ，用于准备包含最高得分的图像
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        # 将得分装换为一幅渲染的图像
        # 函数round() 通常让小数精确到小数点后某一位，其中小数位数是由第二个实参指定的。
        # 如果将第二个实参指定为负数，round() 将舍入到最近的10的整数倍
        rounded_score = round(self.stats.score, -1)
        # score_str = str(self.stats.score)
        # 使用一个字符串格式设置指令，让Python将数值转换为字符串时在其中插入逗号
        score_str = '{:,}'.format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # 在屏幕右上角显示得分
        # 为确保得分始终锚定在屏幕右边,创建一个名为score_rect的rect
        self.score_rect = self.score_image.get_rect()
        # 让其右边缘与屏幕右边缘相距20像素
        self.score_rect.right = self.screen_rect.right - 20
        # 让其上边缘与屏幕上边缘也相距20像素
        self.score_rect.top = 20

    def show_score(self):
        # 在屏幕上显示得分
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        # 将最高得分转换为渲染的图像
        high_score = round(self.stats.high_score, -1)
        high_score_str = '{:,}'.format(high_score)
        # 根据最高得分生成一幅图像
        self.high_score_image = self.font.render(high_score_str, True,self.text_color, self.settings.bg_color)

        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        # 使其水平居中
        self.high_score_rect.centerx = self.screen_rect.centerx
        # 将其top 属性设置为当前得分图像的top属性
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        # 检查是否诞生了新的最高分
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()


    def prep_level(self):
        # 将等级转换为渲染的图像
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,self.text_color, self.settings.bg_color)

        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        # 将top 属性设置为比得分图像的bottom 属性大10像素
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        # 显示还余下多少艘飞船
        # 方法prep_ships() 创建一个空编组self.ships,用于存储飞船实例
        self.ships = Group()
        # 根据玩家还有多少艘飞船以相应的次数运行一个循环
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            # 在这个循环中，创建新飞船并设置其x坐标，让整个飞船编组都位于屏幕左边
            # 且每艘飞船的左边距都为10像素
            ship.rect.x = 10 + ship_number * ship.rect.width
            # 将y坐标设置为离屏幕上边缘10像素，让所有飞船都出现在屏幕左上角
            ship.rect.y = 10
            # 将每艘新飞船都添加到编组ships 中
            # self.ships.add(ship)

            self.ships.add(ship)

