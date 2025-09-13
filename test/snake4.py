import pygame
import random
import sys
import time

# 初始化 Pygame
pygame.init()

# 游戏常量
WIDTH, HEIGHT = 700, 600  # 增加宽度以容纳控制面板
GRID_SIZE = 20
GRID_WIDTH = (WIDTH - 100) // GRID_SIZE  # 游戏区域宽度
GRID_HEIGHT = HEIGHT // GRID_SIZE
MIN_FPS = 5
MAX_FPS = 20
INITIAL_FPS = 10

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 120, 255)
GRAY = (40, 40, 40)
LIGHT_GRAY = (200, 200, 200)
DARK_GREEN = (0, 180, 0)
PURPLE = (180, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.dragging = False
        
        # 计算滑块位置
        self.handle_radius = 10
        self.handle_pos = self.value_to_pos(initial_val)
        
    def value_to_pos(self, value):
        # 将值转换为滑块位置
        normalized = (value - self.min_val) / (self.max_val - self.min_val)
        return self.rect.x + normalized * self.rect.width
        
    def pos_to_value(self, pos):
        # 将滑块位置转换为值
        relative_pos = max(0, min(pos - self.rect.x, self.rect.width))
        normalized = relative_pos / self.rect.width
        return int(self.min_val + normalized * (self.max_val - self.min_val))
        
    def draw(self, surface):
        # 绘制滑动条轨道
        pygame.draw.rect(surface, LIGHT_GRAY, self.rect, border_radius=3)
        pygame.draw.rect(surface, BLACK, self.rect, 1, border_radius=3)
        
        # 绘制滑块
        handle_rect = pygame.Rect(
            self.handle_pos - self.handle_radius, 
            self.rect.centery - self.handle_radius,
            self.handle_radius * 2, 
            self.handle_radius * 2
        )
        pygame.draw.circle(surface, BLUE, (self.handle_pos, self.rect.centery), self.handle_radius)
        pygame.draw.circle(surface, BLACK, (self.handle_pos, self.rect.centery), self.handle_radius, 1)
        
    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 检查是否点击了滑块
            handle_rect = pygame.Rect(
                self.handle_pos - self.handle_radius, 
                self.rect.centery - self.handle_radius,
                self.handle_radius * 2, 
                self.handle_radius * 2
            )
            if handle_rect.collidepoint(mouse_pos) or self.rect.collidepoint(mouse_pos):
                self.dragging = True
                self.handle_pos = max(self.rect.left, min(mouse_pos[0], self.rect.right))
                self.value = self.pos_to_value(self.handle_pos)
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
            return False
            
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle_pos = max(self.rect.left, min(mouse_pos[0], self.rect.right))
            self.value = self.pos_to_value(self.handle_pos)
            return True
            
        return False

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.SysFont('microsoftyahei', 20)
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)
        
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def is_hovered(self, pos):
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color
            return True
        self.current_color = self.color
        return False
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class ColorOption:
    def __init__(self, x, y, size, color, selected=False):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.selected = selected
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=3)
        if self.selected:
            pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=3)
        else:
            pygame.draw.rect(surface, BLACK, self.rect, 1, border_radius=3)
            
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.grow_to = 3
        self.color = GREEN
        self.head_color = BLUE
        self.s_shape_bonus_available = True
        self.s_shape_bonus_claimed = False
        self.s_shape_timer = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
    
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        if new_position in self.positions[1:]:
            self.reset()
            return False
        
        self.positions.insert(0, new_position)
        
        if len(self.positions) > self.grow_to:
            self.positions.pop()
            
        # 检查是否形成S形
        self.check_s_shape()
            
        return True
    
    def check_s_shape(self):
        # 检查蛇是否形成了S形
        if len(self.positions) < 7 or not self.s_shape_bonus_available:
            return
            
        # 获取蛇的前7个部分
        head = self.positions[0]
        segments = self.positions[:7]
        
        # 检查是否形成S形模式
        # S形模式: 右-右-下-下-左-左 或类似的变化
        x_coords = [p[0] for p in segments]
        y_coords = [p[1] for p in segments]
        
        # 检查水平S形
        if (x_coords[0] == x_coords[1] == x_coords[2] and 
            x_coords[3] == x_coords[4] and 
            x_coords[5] == x_coords[6] and
            abs(x_coords[0] - x_coords[3]) == 1 and
            abs(x_coords[3] - x_coords[5]) == 1 and
            y_coords[0] == y_coords[1] and
            y_coords[1] != y_coords[2] and
            y_coords[2] == y_coords[3] == y_coords[4] and
            y_coords[4] != y_coords[5] and
            y_coords[5] == y_coords[6]):
            
            self.claim_s_shape_bonus()
            return
            
        # 检查垂直S形
        if (y_coords[0] == y_coords[1] == y_coords[2] and 
            y_coords[3] == y_coords[4] and 
            y_coords[5] == y_coords[6] and
            abs(y_coords[0] - y_coords[3]) == 1 and
            abs(y_coords[3] - y_coords[5]) == 1 and
            x_coords[0] == x_coords[1] and
            x_coords[1] != x_coords[2] and
            x_coords[2] == x_coords[3] == x_coords[4] and
            x_coords[4] != x_coords[5] and
            x_coords[5] == x_coords[6]):
            
            self.claim_s_shape_bonus()
            return
    
    def claim_s_shape_bonus(self):
        if self.s_shape_bonus_available:
            self.score += 100  # S形奖励分数
            self.s_shape_bonus_available = False
            self.s_shape_bonus_claimed = True
            self.s_shape_timer = pygame.time.get_ticks()
    
    def update_s_shape_status(self):
        current_time = pygame.time.get_ticks()
        if self.s_shape_bonus_claimed and current_time - self.s_shape_timer > 3000:  # 3秒后重置
            self.s_shape_bonus_available = True
            self.s_shape_bonus_claimed = False
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            r = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            
            # 蛇头用不同颜色
            if i == 0:
                pygame.draw.rect(surface, self.head_color, r)
                pygame.draw.rect(surface, WHITE, r, 1)
            else:
                pygame.draw.rect(surface, self.color, r)
                pygame.draw.rect(surface, WHITE, r, 1)
                
    def grow(self):
        self.grow_to += 1
        self.score += 10

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        
    def draw(self, surface):
        r = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, GREEN, r)
        pygame.draw.rect(surface, WHITE, r, 1)

class SpecialFood:
    def __init__(self):
        self.position = (0, 0)
        self.active = False
        self.spawn_time = 0
        self.duration = 10000  # 10秒
        
    def try_spawn(self):
        if not self.active and random.random() < 0.01:  # 1%的几率每帧尝试生成
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            self.active = True
            self.spawn_time = pygame.time.get_ticks()
            
    def update(self):
        if self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.spawn_time > self.duration:
                self.active = False
                
    def draw(self, surface):
        if self.active:
            r = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GOLD, r)
            pygame.draw.rect(surface, WHITE, r, 1)
            
            # 绘制闪烁效果
            if (pygame.time.get_ticks() // 200) % 2 == 0:
                pygame.draw.circle(surface, ORANGE, r.center, GRID_SIZE // 2, 2)

def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH - 100, GRID_SIZE):
            r = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GRAY, r, 1)

def main():
    # 初始化游戏窗口
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('贪吃蛇游戏')
    clock = pygame.time.Clock()
    
    # 创建蛇和食物
    snake = Snake()
    food = Food()
    special_food = SpecialFood()
    
    # 创建按钮
    pause_button = Button(WIDTH - 90, 20, 70, 30, "暂停P", LIGHT_GRAY, WHITE)
    resume_button = Button(WIDTH - 90, 60, 70, 30, "继续P", LIGHT_GRAY, WHITE)
    restart_button = Button(WIDTH - 90, 100, 70, 30, "重启R", LIGHT_GRAY, WHITE)
    
    # 创建速度滑动条
    speed_slider = Slider(WIDTH - 90, 450, 70, 10, MIN_FPS, MAX_FPS, INITIAL_FPS)
    current_fps = INITIAL_FPS
    
    # 颜色选项
    color_options = [
        ColorOption(WIDTH - 90, 180, 20, GREEN, True),
        ColorOption(WIDTH - 60, 180, 20, BLUE),
        ColorOption(WIDTH - 90, 210, 20, PURPLE),
        ColorOption(WIDTH - 60, 210, 20, YELLOW),
        ColorOption(WIDTH - 90, 240, 20, CYAN),
        ColorOption(WIDTH - 60, 240, 20, DARK_GREEN)
    ]
    
    head_color_options = [
        ColorOption(WIDTH - 90, 300, 20, BLUE, True),
        ColorOption(WIDTH - 60, 300, 20, RED),
        ColorOption(WIDTH - 90, 330, 20, PURPLE),
        ColorOption(WIDTH - 60, 330, 20, YELLOW),
        ColorOption(WIDTH - 90, 360, 20, CYAN),
        ColorOption(WIDTH - 60, 360, 20, GREEN)
    ]
    
    # 字体
    font = pygame.font.SysFont('microsoftyahei', 20)
    title_font = pygame.font.SysFont('microsoftyahei', 16, bold=True)
    bonus_font = pygame.font.SysFont('microsoftyahei', 24, bold=True)
    
    # 游戏状态
    paused = False
    game_over = False
    bonus_message = ""
    bonus_timer = 0
    
    # 游戏主循环
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not paused and not game_over:
                    if event.key == pygame.K_UP:
                        snake.turn(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.turn(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.turn(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.turn(RIGHT)
                    elif event.key == pygame.K_p:  # P键暂停
                        paused = True
                elif event.key == pygame.K_r:  # R键重启
                    snake.reset()
                    food.randomize_position()
                    special_food.active = False
                    game_over = False
                    paused = False
            
            # 检查按钮点击
            if pause_button.is_clicked(mouse_pos, event):
                paused = True
            if resume_button.is_clicked(mouse_pos, event):
                paused = False
            if restart_button.is_clicked(mouse_pos, event):
                snake.reset()
                food.randomize_position()
                special_food.active = False
                game_over = False
                paused = False
                
            # 检查颜色选项点击
            for i, option in enumerate(color_options):
                if option.is_clicked(mouse_pos, event):
                    snake.color = option.color
                    for opt in color_options:
                        opt.selected = False
                    option.selected = True
                    
            for i, option in enumerate(head_color_options):
                if option.is_clicked(mouse_pos, event):
                    snake.head_color = option.color
                    for opt in head_color_options:
                        opt.selected = False
                    option.selected = True
            
            # 处理滑动条事件
            if speed_slider.handle_event(event, mouse_pos):
                current_fps = speed_slider.value
        
        # 更新S形奖励状态
        snake.update_s_shape_status()
        
        # 更新特殊食物
        special_food.update()
        if not paused and not game_over:
            special_food.try_spawn()
        
        # 移动蛇（如果没有暂停且游戏没有结束）
        if not paused and not game_over:
            if not snake.move():
                game_over = True
        
        # 检查是否吃到普通食物
        if not paused and not game_over and snake.get_head_position() == food.position:
            snake.grow()
            food.randomize_position()
            # 确保食物不出现在蛇身上
            while food.position in snake.positions:
                food.randomize_position()
        
        # 检查是否吃到特殊食物
        if not paused and not game_over and special_food.active and snake.get_head_position() == special_food.position:
            snake.score += 50  # 特殊食物奖励
            special_food.active = False
            bonus_message = "特殊食物 +50分!"
            bonus_timer = pygame.time.get_ticks()
        
        # 检查奖励消息显示时间
        current_time = pygame.time.get_ticks()
        if bonus_message and current_time - bonus_timer > 2000:  # 2秒后消失
            bonus_message = ""
        
        # 绘制游戏界面
        screen.fill(BLACK)
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)
        special_food.draw(screen)
        
        # 绘制控制面板背景
        panel_rect = pygame.Rect(WIDTH - 100, 0, 100, HEIGHT)
        pygame.draw.rect(screen, (50, 50, 50), panel_rect)
        pygame.draw.line(screen, WHITE, (WIDTH - 100, 0), (WIDTH - 100, HEIGHT), 2)
        
        # 显示分数和长度
        score_surface = font.render(f'得分: {snake.score}', True, WHITE)
        score_rect = score_surface.get_rect()
        score_rect.topleft = (10, 10)
        screen.blit(score_surface, score_rect)
        
        length_surface = font.render(f'长度: {snake.grow_to}', True, WHITE)
        length_rect = length_surface.get_rect()
        length_rect.topleft = (10, 40)
        screen.blit(length_surface, length_rect)
        
        # 显示S形奖励状态
        s_shape_status = "可用" if snake.s_shape_bonus_available else "冷却中"
        s_shape_color = GREEN if snake.s_shape_bonus_available else RED
        s_shape_surface = font.render(f'S形奖励: {s_shape_status}', True, s_shape_color)
        s_shape_rect = s_shape_surface.get_rect()
        s_shape_rect.topleft = (10, 70)
        screen.blit(s_shape_surface, s_shape_rect)
        
        # 绘制按钮
        pause_button.is_hovered(mouse_pos)
        resume_button.is_hovered(mouse_pos)
        restart_button.is_hovered(mouse_pos)
        
        pause_button.draw(screen)
        resume_button.draw(screen)
        restart_button.draw(screen)
        
        # 绘制颜色选择标题
        color_title = title_font.render("身体颜色:", True, WHITE)
        screen.blit(color_title, (WIDTH - 90, 160))
        
        head_color_title = title_font.render("头部颜色:", True, WHITE)
        screen.blit(head_color_title, (WIDTH - 90, 280))
        
        # 绘制颜色选项
        for option in color_options:
            option.draw(screen)
            
        for option in head_color_options:
            option.draw(screen)
        
        # 绘制速度滑动条和标签
        speed_title = title_font.render("游戏速度:", True, WHITE)
        screen.blit(speed_title, (WIDTH - 90, 430))
        
        speed_slider.draw(screen)
        
        speed_text = font.render(f"{current_fps} FPS", True, WHITE)
        screen.blit(speed_text, (WIDTH - 90, 470))
        
        # 显示S形奖励说明
        s_shape_help = title_font.render("S形奖励100分", True, GOLD)
        screen.blit(s_shape_help, (WIDTH - 90, 500))
        
        special_food_help = title_font.render("金色食物50分", True, ORANGE)
        screen.blit(special_food_help, (WIDTH - 90, 520))
        
        # 如果游戏暂停，显示暂停文本
        if paused and not game_over:
            pause_text = font.render("游戏已暂停", True, WHITE)
            pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(pause_text, pause_rect)
        
        # 如果游戏结束，显示游戏结束文本
        if game_over:
            game_over_font = pygame.font.SysFont('microsoftyahei', 40)
            game_over_text = game_over_font.render("游戏结束!", True, RED)
            game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
            screen.blit(game_over_text, game_over_rect)
            
            score_text = font.render(f"最终得分: {snake.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            screen.blit(score_text, score_rect)
            
            restart_text = font.render("按R键或点击重启按钮重新开始", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
            screen.blit(restart_text, restart_rect)
        
        # 显示奖励消息
        if bonus_message:
            bonus_surface = bonus_font.render(bonus_message, True, GOLD)
            bonus_rect = bonus_surface.get_rect(center=(WIDTH // 2, 50))
            screen.blit(bonus_surface, bonus_rect)
        
        # 显示S形奖励消息
        if snake.s_shape_bonus_claimed:
            s_bonus_surface = bonus_font.render("S形奖励 +100分!", True, GOLD)
            s_bonus_rect = s_bonus_surface.get_rect(center=(WIDTH // 2, 50 if not bonus_message else 80))
            screen.blit(s_bonus_surface, s_bonus_rect)
        
        pygame.display.update()
        clock.tick(current_fps)

if __name__ == "__main__":
    main()