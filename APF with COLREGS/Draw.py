import matplotlib.pyplot as plt
import numpy as np
import Ship # 导入船舶信息

def draw_ship(ship_info, ax, color, label):
    x = Ship.Ship(ship_info).get_x()
    y = Ship.Ship(ship_info).get_y()
    direction = Ship.Ship(ship_info).get_cor()

    # 船体尺寸（示例值，可根据需要调整）
    length = 0.5
    width = 0.3

    # 计算船体四个角的坐标
    angle = np.radians(angle_change(direction))
    dx = np.cos(angle) * length / 2
    dy = np.sin(angle) * length / 2
    corners = np.array([
        [x - dx - dy * width / 2, y - dy + dx * width / 2],
        [x - dx + dy * width / 2, y - dy - dx * width / 2],
        [x + dx + dy * width / 2, y + dy - dx * width / 2],
        [x + dx - dy * width / 2, y + dy + dx * width / 2]
    ])

    # 绘制船体
    poly = plt.Polygon(corners, edgecolor='black', facecolor=color)
    ax.add_patch(poly)

    # 标示船头方向
    ax.plot([x, x + dx], [y, y + dy], color='red')

    # 添加文字标签
    ax.text(x, y-1, label, color='black', fontsize=12, ha='center')

#画图
def draw_fig():
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_title('Ship Positions and Headings')
    ax.grid(True)
    return ax

#转化为以北为正方向
def angle_change(direction):
    draw_direction = np.where(direction <= 90,90-direction,450 - direction)
    return draw_direction

if __name__ == '__main__':
    # 创建船对象
    shipA = [-3.0, -8.0, 15.0, 0.1] # 船A
    shipB = [2.0, -3.0, 40.0, 0.08] # 船B

    ax = draw_fig()
    draw_ship(shipA, ax, 'gray', 'our_ship')
    draw_ship(shipB, ax, 'blue', 'target_ship')

    plt.show()
