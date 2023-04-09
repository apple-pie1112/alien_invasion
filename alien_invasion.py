# 创建一个表示游戏的类，以创建空的pygame窗口
import sys
import pygame
# time-sleep，以便在飞船被外星人撞到后让游戏暂停片刻
from time import sleep


from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源。"""
        # 调用pygame.display.set_mode() 来创建一个显示窗口，游戏的所有图形元素都将在其中绘制。
        # 实参(1200,800) 是一个元组，指定了游戏窗口的尺寸——宽1200像素、高800像素
        # 将这个显示窗赋给属性self.screen ，让这个类中的所有方法都能够使用它
        # display.set_mode()返回的surface(屏幕的一部分，用来显示游戏元素)表示整个游戏窗口。
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        self.settings = Settings()

        # self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # 创建存储游戏统计信息的实例
        # 创建记分牌
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # 导入Ship 类，并在创建屏幕后创建一个Ship 实例
        # self 指向的是当前AlienInvasion 实例
        self.ship = Ship(self)

        # 在AlienInvasion 中创建一个编组（group），用于存储所有有效的子弹，以便管理发射出去的所有子弹。
        # 这个编组是pygame.sprite.Group 类的一个实例。
        # pygame.sprite.Group 类似于列表，但提供了有助于开发游戏的额外功能。
        self.bullets = pygame.sprite.Group()
        self.aliens =pygame.sprite.Group()

        self._create_fleet()

        # 创建play按钮,但没有将其显示在屏幕上
        self.play_button = Button(self,'Play')


        # # 设置背景色
        # self.bg_color = (230, 230, 230)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 监视键盘和鼠标事件。
            # 在主循环中，在任何情况下都需要调用_check_events() ，即便游戏处于非活动状态。
            # 例如，我们需要知道玩家是否按了Q 键以退出游戏，或者是否单击了关闭窗口的按钮。
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()


    # 在Python中，辅助方法的名称以单个下划线打头
    # 新增方法_check_events() 后的AlienInvasion 类，只有run_game() 的代码受到影响
    def _check_events(self):
        # 响应按键和鼠标事件
        # for循环是一个事件的循环
        # 为访问Pygame检测到的事件，使用函数pygame.event.get() 。
        # 这个函数返回一个列表，其中包含它在上一次被调用后发生的所有事件。
        # 所有键盘和鼠标事件都将导致这个for循环运行
        # 当玩家单击游戏窗口的关闭按钮时，将检测到pygame.QUIT 事件，进而调用sys.exit() 来退出游戏
        # 飞船的位置将在检测到键盘事件后（但在更新屏幕前）更新。这样，玩家输入时，飞船的位置将更新，从而确保使用更新后的位置将飞船绘制到屏幕上。
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # 重构
            elif event.type == pygame.KEYDOWN:
                # 调用方法（辅助）
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 使用了pygame.mouse.get_pos() ，它返回一个元组，其中包含玩家单击时鼠标的X坐标和Y坐标
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
        # 在玩家单击play按钮时开始游戏
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        # 使用了rect 的方法collidepoint() 检查鼠标单击位置是否在Play按钮的rect 内
        # if self.play_button.rect.collidepoint(mouse_pos):
        if button_clicked and not self.stats.game_active:
            # 重置游戏统计信息
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人并让飞船居中。
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)


    def _check_keydown_events(self,event):
        # 响应按键
        # KEYDOWN 按下按键
        if event.key == pygame.K_RIGHT:
                # 向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # 飞船上下移动，语句如下
        # elif event.key == pygame.K_UP:
        #     self.ship.moving_up = True
        # elif event.key == pygame.K_DOWN:
        #     self.ship.moving_down = True
        elif event.key == pygame.K_q:
            # self.update_score()
            sys.exit()
            pygame.quit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        # 响应松开
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        # 飞船上下移动，语句如下
        # if event.key == pygame.K_UP:
        #     self.ship.moving_up = False
        # if event.key == pygame.K_DOWN:
        #     self.ship.moving_down = False


    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            # 创建一颗子弹，并将其加入编组bullets中
            # 创建一个Bullet 实例并将其赋给new_bullet
            new_bullet = Bullet(self)
            # 再使用方法add() 将其加入编组bullets
            self.bullets.add(new_bullet)

    # 整理关于管理子弹的代码
    def _update_bullets(self):
        # 更新子弹的位置并删除消失的子弹
        # 更新子弹的位置
        # 原位置在run_game
        self.bullets.update()
        # 删除消失的子弹，因为之前子弹并没有消失，仅仅是看不见了
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        # 响应子弹和外星人的碰撞
        # 删除发生碰撞的子弹和外星人
        # 检查是否有子弹击中了外星人
        # 如果是，就删除相应的子弹和外星人
        # 函数sprite.groupcollide() 将一个编组中每个元素的rect 同另一个编组中每个元素的rect 进行比较。
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
            # 备注：要模拟能够飞行到屏幕顶端、消灭击中的每个外星人的高能子弹，
            # 可将第一个布尔实参设置为False ，并保留第二个布尔参数为True 。
            # 这样被击中的外星人将消失，但所有的子弹都始终有效，直到抵达屏幕顶端后消失。
        )
        # 有子弹击中外星人时，Pygame返回一个字典（collisions ）。
        # 检查这个字典是否存在，如果存在，就将得分加上一个外星人的分数
        if collisions:
        # 与外星人碰撞的子弹都是字典collisions 中的一个键，而与每颗子弹相关的值都是
        # 一个列表，其中包含该子弹击中的外星人。
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points *  len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # 删除现有的子弹并创建一群新的外星人
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        # 更新外星人群众所有外星人的位置
        # 检查是否有外星人位于屏幕边缘
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        # 函数spritecollideany() 接受两个实参：一个精灵和一个编组。
        if pygame.sprite.spritecollideany(self.ship , self.aliens):
            # 它检查编组是否有成员与精灵发生了碰撞，并在找到与精灵发生碰撞的成员后停止遍历编组。
            # print('Ship hit!!!')
            self._ship_hit()

        # 检查是否有外星人到达了屏幕底端
        self._check_aliens_bottom()

    def _create_fleet(self):
        # 创建外星人群
        # 创建一个外星人并计算一行可容纳多少个外星人
        # 外星人的间距为外星人宽度
        alien = Alien(self)
        # 从外星人的rect 属性中获取外星人宽度，并将这个值存储到alien_width 中，以免反复访问属性rect 。
        alien_width , alien_height = alien.rect.size
        # 计算可用于放置外星人的水平空间以及其中可容纳多少个外星人。
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算屏幕可容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # # 创建第一行外星人
        # for alien_number in range(number_aliens_x):
        #     self._creat_alien(alien_number)

        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._creat_alien(alien_number,row_number)


    def _creat_alien(self,alien_number,row_number):
        # 创建一个外星人并将其加入当前行
        alien = Alien(self)
        # alien_width = alien.rect.width
        # 创建一个新的外星人，并通过设置x坐标将
        alien_width, alien_height = alien.rect.size
        # 将每个外星人都往右推一个外星人宽度。接下来，
        # 将外星人宽度乘以2，得到每个外星人占据的空间（其中包括右边的空白区域），再据此计算当前外星人在当前行的位置。
        alien.x = alien_width + 2 * alien_width * alien_number
        # 使用外星人的属性x 来设置其rect 的位置。
        alien.rect.x = alien.x
        # 修改外星人的y坐标并在第一行
        # 外星人上方留出与外星人等高的空白区域。相邻外星人行的y坐标
        # 相差外星人高度的两倍，因此将外星人高度乘以2，再乘以行号。
        # 第一行的行号为0，因此第一行的垂直位置不变，而其他行都沿屏 幕依次向下放置。
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        # 将每个新创建的外星人都添加到编组aliens中。
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        # 有外星人到达边缘时采取相应的措施
        # 遍历外星人群并对其中的每个外星人调用check_edges()
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # 将整群外星人下移，并改变他们的方向
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        # 更新屏幕上的图像，并切换到新屏幕
        # 为进一步简化run_game() ，将更新屏幕的代码移到一个名为_update_screen() 的方法中
        # 每次循环时都重绘屏幕
        # 调用方法fill()用这种背景色填充屏幕
        # 方法fill() 用于处理surface，只接受一个实参：一种颜色。
        # 填充背景后，调用ship.blitme() 将飞船绘制到屏幕上，确保它出现在背景前面
        # 让最近绘制的屏幕可见。
        # 不断绘制一个新的，并擦去旧的
        # 不断更新屏幕，以显示元素的新位置，并在原位置隐藏元素，从而营造平滑移动的效果
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        # 方法bullets.sprites() 返回一个列表，其中包含编组bullets中的所有精灵。
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 对编组调用draw() 时，Pygame将把编组中的每个元素绘制到属性rect 指定的位置。
        # 方法draw() 接受一个参数，这个参数指定了要将编组中的元素绘制到哪个surface上。
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态，就绘制play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


    def _ship_hit(self):
        # 响应飞船被外星人撞到
        if self.stats.ships_left > 0:
            # 将ships_left减一
            # 飞船被外星人撞到时调用prep_ships() ，从而在玩家损失飞船时更新飞船图像
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船放到屏幕底端的中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        # 检查是否有外星人到达了屏幕底端
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样处理。
                self._ship_hit()
                break


    # def update_score(self):
    #     # 更新最高得分
    #     filename = 'score.txt'
    #     highscore = self.stats.high_score
    #     with open(filename,'r+') as file_object:
    #         for score in file_object:
    #             self.highestscore = int(score)
    #         if highscore > self.highestscore:
    #             file_object.write(str(highscore))
    #             self.highestscore = highscore

if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()




