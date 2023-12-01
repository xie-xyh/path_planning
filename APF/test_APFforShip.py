import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from matplotlib.animation import FuncAnimation
import COLREGs #导入避碰规则
import Ship #导入船舶信息
import calAPF #导入计算APF

class Draw_Ship:
    def __init__(self,ship_info,L_or_R,is_moving = True):
        self.x = Ship.Ship(ship_info).get_x()
        self.y = Ship.Ship(ship_info).get_y()
        self.direction = Ship.Ship(ship_info).get_cor()
        self.speed = Ship.Ship(ship_info).get_spd() 
        self.L_or_R = L_or_R
        self.is_moving = is_moving #是否允许转弯
        self.turn_updated = False #转向标志位
        self.turn_rate = 10
        # self.delta_x,self.delta_y = calAPF.calAPF().gradient_U_total()
    #更新船舶位置
    def update_position(self):
        if self.is_moving: #转弯
            if self.turn_updated:#转弯结束
                if self.L_or_R == [True,False]:#左转
                    self.direction -= self.turn_rate 
                elif self.L_or_R == [False,True]:#右转
                    self.direction += self.turn_rate
            
        # 更新位置
        angle = np.radians(self.angle_change())
        self.x += np.cos(angle) * self.speed
        self.y += np.sin(angle) * self.speed

    #转化为以北为正方向
    def angle_change(self):
        draw_direction = np.where(self.direction <= 90,90-self.direction,450 - self.direction)
        return draw_direction
    
    #更新转弯方向
    def update_L_or_R(self, new_L_or_R):
        if not self.turn_updated:
            self.L_or_R = new_L_or_R
            self.turn_updated = True #更新标志位

    def draw(self, ax):
        # 船体尺寸（示例值，可根据需要调整）
        length = 0.1
        width = 0.08

        # 计算船体四个角的坐标
        angle = np.radians(self.angle_change())
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
# shipA = [0.0, -5.0, 45.0, 0.1] #对遇
# shipB = [10.0, 5.0, 219.0, 0.1]
# shipA = [0.0, 0.0, 45.0, 0.1]  #交叉相遇
# shipB = [3.0, 3.0, 180.0, 0.1] 
shipA = [-3.0, -8.0, 15.0, 0.1] #追越
shipB = [2.0, -3.0, 40.0, 0.08] 
# shipB = [-3.0, -8.0, 15.0, 0.2] #被追越
# shipA = [1.0, 5.0, 10.0, 0.05]

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
    print()
    

# 创建动画
ani = FuncAnimation(fig, update, frames=np.arange(0, 200, 1), blit=False, repeat=False)
plt.show()
