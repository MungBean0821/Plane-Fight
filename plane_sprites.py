import random
import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新的帧率
FRAME_PER_SEC = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 主角移动速度
HERO_SPEED = 2
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""
    def __init__(self, image_name, speed=1):

        # 调用父类的初始化方法
        super().__init__()

        # 定义对象的属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):

        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):
        super().__init__("./images/background.png")
        # 判断背景精灵是否是默认替代的那张背景图
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        # 1.调用父类的方法实现
        super().update()
        # 2.判断是否移出屏幕，如果移出屏幕，将图像设置到屏幕的上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """敌机精灵"""

    def __init__(self):
        super().__init__("./images/enemy1.png")
        # 设置敌机随机飞行速度
        self.speed = random.randint(2, 4)
        # 设置敌机初始位置
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    # def __del__(self):
    #     print("敌机已销毁...")

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            # 将飞出屏幕的敌机进行销毁
            self.kill()


class Hero(GameSprite):
    """英雄类精灵"""

    def __init__(self):
        super().__init__("./images/me1.png", 0)
        # 设置主角初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 40
        # 创建子弹精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):
        # 设置主角不能飞出屏幕范围
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        elif self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom
        elif self.rect.top < 0:
            self.rect.top = 0

    def fire(self):
        for i in (0, 1, 2):
            bullet = Bullet()

            bullet.rect.bottom = self.rect.y - i * 15
            bullet.rect.centerx = self.rect.centerx

            self.bullets.add(bullet)


class Bullet(GameSprite):
    """子弹精灵"""

    def __init__(self):
        super().__init__("./images/bullet2.png", -2)

    def update(self):
        super().update()
        # 销毁飞出屏幕的子弹
        if self.rect.bottom < 0:
            self.kill()

    # def __del__(self):
    #     print("子弹被销毁...")


