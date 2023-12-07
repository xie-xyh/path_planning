import numpy as np
import matplotlib.pyplot as plt

# 初始位置和速度
x0, y0 = 0, 0  # 初始位置
vx, vy = 1, 0  # 初始速度，假设船初始向右

# 外部力方向和大小
force_magnitude = 0.1  # 力的大小
force_angle_degrees = 30  # 力的方向，假设为30度

# 将角度转换为弧度
force_angle_radians = np.radians(force_angle_degrees)

# 模拟时间步长和总时间
dt = 0.01  # 时间步长
total_time = 10  # 总时间

# 初始化轨迹
x_traj, y_traj = [x0], [y0]

# 模拟船只运动
for t in np.arange(0, total_time, dt):
    # 计算力的分量
    force_x = force_magnitude * np.cos(force_angle_radians)
    force_y = force_magnitude * np.sin(force_angle_radians)
    
    # 计算加速度
    ax = force_x
    ay = force_y
    
    # 更新速度
    vx += ax * dt
    vy += ay * dt
    
    # 更新位置
    x0 += vx * dt
    y0 += vy * dt
    
    # 将新位置添加到轨迹中
    x_traj.append(x0)
    y_traj.append(y0)

# 绘制轨迹
plt.plot(x_traj, y_traj)
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Ship Trajectory with External Force')
plt.grid(True)
plt.show()
