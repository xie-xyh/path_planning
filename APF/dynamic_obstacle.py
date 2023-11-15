import numpy as np
import matplotlib.pyplot as plt

# 初始化障碍物的数量和初始位置
num_obstacles = 1
obstacle_positions = np.random.uniform(0.9,1,(1, 2)) * 10  # 随机生成初始位置，假设地图大小是10x10
# 模拟动态障碍物的运动
num_steps = 50  # 模拟步数
for step in range(num_steps):
    # 障碍物按随机方向移动，可以根据需要修改移动规则
    x_range = np.random.uniform(-0.35, 0, size=(num_obstacles, 1))  # 生成 x 坐标
    y_range = np.random.uniform(-0.5, 0.25, size=(num_obstacles, 1))  # 生成 y 坐标
    obstacle_positions = obstacle_positions + np.hstack((x_range,y_range))
    
    # 确保障碍物在地图范围内，假设地图大小是10x10
    obstacle_positions = np.clip(obstacle_positions, 0, 10)

    grid_map = np.zeros((10, 10))

    # 可视化障碍物的移动
    plt.imshow(grid_map,cmap='cool')
    plt.plot(obstacle_positions[:, 0], obstacle_positions[:, 1], marker = '.',color='red')
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Dynamic Obstacle Movement')
    # plt.show(block=False)  # 显示动态变化的图像，不阻塞程序继续运行
    plt.pause(0.1)  # 暂停0.1秒，控制图像刷新的速度
    # plt.close()  # 关闭当前图像，准备绘制下一帧
plt.show()
# 如果需要保存动态图像，可以在循环结束后加上保存操作
# plt.savefig('dynamic_obstacle_movement.gif', dpi=80, writer='imagemagick')
