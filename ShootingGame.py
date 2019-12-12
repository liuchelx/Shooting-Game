from enum import Enum, unique
from math import sqrt
from random import randint

import pygame


@unique
class Color(Enum):
    """Color Variables"""

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (242, 242, 242)

    @staticmethod
    def random_color():
        """
            获得随机颜色
            Color.random_color()
        """
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return (r, g, b)


class Ball(object):
    """球"""

    def __init__(self, x, y, radius, sx, sy, color=Color.RED):
        """初始化方法"""
        self.x = x
        self.y = y
        self.radius = radius
        self.sx = sx
        self.sy = sy
        self.color = color
        self.alive = True  # show/hide current circle

    def setXY(self, x, y):
        self.x = x
        self.y = y

    def move(self, screen):
        """移动"""
        self.x += self.sx
        self.y += self.sy

        # rebounce if touch the edge of screen
        if self.x - self.radius <= 0 or \
                self.x + self.radius >= screen.get_width():
            # self.sx = -self.sx
            self.alive = False

        if self.y - self.radius <= 0 or \
                self.y + self.radius >= screen.get_height():
            # self.sy = -self.sy
            self.alive = False

    def moveWithRebouce(self, screen):
        """移动"""
        self.x += self.sx
        self.y += self.sy

        # rebounce if touch the edge of screen
        if self.x - self.radius <= 0 or \
                self.x + self.radius >= screen.get_width():
            self.sx = -2*self.sx

        if self.y - self.radius <= 0 or \
                self.y + self.radius >= screen.get_height():
            self.sy = -2*self.sy

    def randomMove(self, screen):

        self.sx = randint(-25, 25)
        self.sy = randint(-25, 25)
        self.moveWithRebouce(screen)

    def _printObject(self):
        print(self.x, self.y, self.color)

    def hit(self, other):
        """吃其他球"""
        if self.alive and other.alive and self != other:
            dx, dy = self.x - other.x, self.y - other.y
            distance = sqrt(dx ** 2 + dy ** 2)
            if distance < self.radius + other.radius:
                other.alive = False
                self.alive = False

    def draw(self, screen):
        """在窗口上绘制球"""
        pygame.draw.circle(screen, self.color,
                           (self.x, self.y), self.radius, 0)


def main():

    # 定义用来装所有球的容器
    balls = []

    bullets = []

    # 初始化导入的pygame中的模块
    pygame.init()
    # 初始化用于显示的窗口并设置窗口尺寸
    screen = pygame.display.set_mode((800, 600))
    color = Color.random_color()
    playerX = 400
    playerY = 520
    player = Ball(playerX, playerY, 15, 10, 10, color)

    # 设置当前窗口的标题
    pygame.display.set_caption('Python Game - airPlane Fight')
    running = True

    screen.fill((255, 255, 255))

    player.draw(screen)

    pygame.display.flip()
    pygame.time.delay(50)

    enemies = []
    enemeiesNum = 10
    # generate 3 random enemeis
    for i in range(enemeiesNum):
        x, y = randint(50, 750), randint(0, 50)
        radius = 25

        # todo: enable this later
        # sx, sy = randint(-10, 10), randint(-10, 10)
        sx, sy = 0, 10
        color = Color.random_color()
        # 创建一个enemy(球)(大小= 25. 速度 = 10. 颜色随机)
        enemy = Ball(x, y, radius, sx, sy, color)
        # 将球添加到列表容器中
        enemies.append(enemy)
        enemy.draw(screen)
        pygame.display.flip()
        pygame.time.delay(50)

    while running:
        # 从消息队列中获取事件并对事件进行处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # 处理鼠标事件的代码

            # every time mouse click, shoot on bullet upwards
            if event.type == pygame.MOUSEMOTION:
                # 获得点击鼠标的位置
                x, y = event.pos
                player.setXY(x, y)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                radius = 1
                # sx, sy = randint(-10, 10), randint(-10, 10)
                sx, sy = 0, -10
                color = Color.random_color()

                # 在点击鼠标的位置创建一个球(大小、速度和颜色随机)
                bullet = Ball(x, y, radius, sx, sy, color)
                # 将球添加到列表容器中
                bullets.append(bullet)

        # redraw everything
        screen.fill((255, 255, 255))

        # 取出容器中的球 如果没被吃掉就绘制 被吃掉了就移除
        for bullet in bullets:
            if bullet.alive:
                bullet.draw(screen)
            else:
                bullets.remove(bullet)

        # 取出容器中的球 如果没被吃掉就绘制 被吃掉了就移除
        for enemy in enemies:
            if enemy.alive:
                enemy.draw(screen)
            else:
                enemies.remove(enemy)

        player.draw(screen)

        # 每隔50毫秒就改变球的位置再刷新窗口
        pygame.display.flip()
        pygame.time.delay(50)
        for enemy in enemies:
            enemy.randomMove(screen)

        for bullet in bullets:
            bullet.move(screen)
            # 检查球有没有吃到其他的球
            for other in enemies:
                bullet.hit(other)


if __name__ == '__main__':
    main()
