import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import COLREGs #导入避碰规则
import Ship #导入船舶信息

class Draw_Ship:
    def __init__(self,ship_info,L_or_R,is_moving = True):
        self.x = Ship.Ship(ship_info).get_x()
        self.y = Ship.Ship(ship_info).get_y()
        self.direction = Ship.Ship(ship_info).get_cor()
        self.speed = Ship.Ship(ship_info).get_spd()
        self.L_or_R = L_or_R
        self.is_moving = is_moving #是否移动
        self.turn_rate = 1
        
    #更新船舶位置
    def update_position(self):
        if self.is_moving:
            if self.L_or_R == [True,False]:#左转
                self.direction += self.turn_rate 
            elif self.L_or_R == [False,True]:#右转
                self.direction -= self.turn_rate
            
            # 更新位置
            angle = np.radians(self.direction)
            self.x += np.cos(angle) * self.speed
            self.y += np.sin(angle) * self.speed

    def update_L_or_R(self, new_L_or_R):
            self.L_or_R = new_L_or_R

    def draw(self, ax):
        # 船体尺寸（示例值，可根据需要调整）
        length = 1
        width = 0.8

        # 计算船体四个角的坐标
        angle = np.radians(self.direction)
        dx = np.cos(angle) * length / 2
        dy = np.sin(angle) * length / 2
        corners = np.array([
            [self.x - dx - dy * width / 2, self.y - dy + dx * width / 2],
            [self.x - dx + dy * width / 2, self.y - dy - dx * width / 2],
            [self.x + dx + dy * width / 2, self.y + dy - dx * width / 2],
            [self.x + dx - dy * width / 2, self.y + dy + dx * width / 2]
        ])

        # 绘制船体
        poly = plt.Polygon(corners, edgecolor='black', facecolor='gray')
        ax.add_patch(poly)

        # 标示船头方向
        ax.plot([self.x, self.x + dx], [self.y, self.y + dy], color='red')

# 创建船对象
shipA = [0.0, -10.0, 30.0, 0.1]
shipB = [-1.0, 4.0, 120.0, 0.08]
L_or_R,type,num = COLREGs.COLREGs_byzheng(shipA,shipB).judge()
draw_A = Draw_Ship(shipA,[False,False],is_moving=True)
draw_B = Draw_Ship(shipB,[False,False],is_moving=True)

# 设置绘图
fig, ax = plt.subplots(figsize=(10, 10))#fig是图形容器，ax是坐标轴
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_title('Ship Positions and Headings')
plt.grid(True)

# 初始化轨迹列表
A_trajectory_x, A_trajectory_y = [], []
B_trajectory_x, B_trajectory_y = [], []

# 更新函数
def update(frame):
    #根据船位置来判断转弯方向
    current_L_or_R_A, current_type_A, current_num_A = COLREGs.COLREGs_byzheng([draw_A.x, draw_A.y, draw_A.direction, draw_A.speed], 
                                                      [draw_B.x, draw_B.y, draw_B.direction, draw_B.speed]).judge()
    current_L_or_R_B, current_type_B, current_num_B = COLREGs.COLREGs_byzheng([draw_B.x, draw_B.y, draw_B.direction, draw_B.speed],
                                                      [draw_A.x, draw_A.y, draw_A.direction, draw_A.speed]).judge()
    # 更新L_or_R
    draw_A.update_L_or_R(current_L_or_R_A)
    draw_B.update_L_or_R(current_L_or_R_B)
    #更新位置
    draw_A.update_position()
    draw_B.update_position()

    ax.clear()
    draw_A.draw(ax)
    draw_B.draw(ax)
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_title('Ship Positions and Headings')
    plt.grid(True)

    # 更新轨迹列表并绘制轨迹
    A_trajectory_x.append(draw_A.x)
    A_trajectory_y.append(draw_A.y)
    B_trajectory_x.append(draw_B.x)
    B_trajectory_y.append(draw_B.y)
    ax.plot(A_trajectory_x, A_trajectory_y, color='blue')  # 使用蓝色线条绘制轨迹
    ax.plot(B_trajectory_x, B_trajectory_y, color='green')  # 使用绿色线条绘制轨迹
    print("Ship A - L_or_R:", current_L_or_R_A, "Type:", current_type_A, "Num:", current_num_A)
    print("Ship B - L_or_R:", current_L_or_R_B, "Type:", current_type_B, "Num:", current_num_B)
    print()
# 创建动画
ani = FuncAnimation(fig, update, frames=np.arange(0, 200, 1), blit=False, repeat=False)

plt.show()
