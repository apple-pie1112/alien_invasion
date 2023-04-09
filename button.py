# 导入模块pygame.font ，它让Pygame能够将文本渲染到屏幕上。
import pygame.font
class Button:
    # msg 是要在按钮中显示的文本
    def __init__(self , ai_game , msg):
        # 初始化按钮的属性
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width , self.height = 200 , 50
        self.button_color = (0 , 255 , 0)
        self.text_color = (255 , 255 , 255)
        # 指定使用什么字体来渲染文本。实参None 让Pygame使用默认字体，而48 指定了文本的字号。
        self.font = pygame.font.SysFont(None , 48)

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需创建一次
        self._prep_msg(msg)

    # 方法_prep_msg() 接受实参self 以及要渲染为图像的文本msg
    def _prep_msg(self,msg):
        # 将msg渲染为图像，并使其在按钮上居中
        # 调用font.render() 将存储在msg 中的文本转换为图像，再将该图像存储在self.msg_image 中
        # 方法font.render() 还接受一个布尔实参，该实参指定开启还是关闭反锯齿功能（反锯齿让文本的边缘更平滑）。
        # 余下的两个实参分别是文本颜色和背景色。
        self.msg_image = self.font.render(msg, True, self.text_color,self.button_color)
        # 让文本图像在按钮上居中：根据文本图像创建一个rect ，并将其center 属性设置为按钮的center 属性。
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制一个用颜色填充的按钮，再绘制文本
        # 调用screen.fill() 来绘制表示按钮的矩形
        self.screen.fill(self.button_color, self.rect)
        # 调用screen.blit() 并向它传递一幅图像以及与该图像相关联的rect ，从而在屏幕上绘制文本图像。
        self.screen.blit(self.msg_image, self.msg_image_rect)