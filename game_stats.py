class GameStats:
    # 跟踪游戏的统计信息
    def __init__(self,ai_game):
        # 初始化统计信息
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.reset_stats()
        # 游戏刚启动时处于活动状态
        self.game_active = False

        # 任何情况下都不应重置最高得分。
        # 因为在任何情况下都不会重置最高得分，所以在__init__() 而不是reset_stats() 中初始化high_score 。
        self.high_score = 0


        # 历史最高分
        # # 读取历史最高得分，初始化历史最高得分
        # filename = 'score.txt'
        # with open(filename,'r+') as file_object:
        #     for score in file_object:
        #         self.highestscore = int(score)
        # self.high_score = self.highestscore

    def reset_stats(self):
        # 初始化在游戏运行期间可能变化的统计信息
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
