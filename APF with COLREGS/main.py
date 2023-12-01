import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import Ship
import calAPF
import calCPA
import COLREGs
import Draw

# 全局变量存储初始遭遇状态
encounter = None
count = 0

# 更新船的位置
def update(frame):
    global encounter, count, apf_values,os_track
    type = COLREGs.COLREGs_byzheng(os,ts).get_encounter()
    num = COLREGs.COLREGs_byzheng(os,ts).get_num()
    if type is not None and count == 0:
        encounter = type
        count = 1
    elif type is None:
        encounter = None
        
    apf = calAPF.calAPF(os,ts,goal,apf_values,encounter)
    delta_x,delta_y = apf.gradient_U_total()
    delta_x = np.float64(delta_x)
    delta_y = np.float64(delta_y)
    a = apf.cal_ds_2()
    print(a)
    #人工势场法更新船的位置
    os[0] += os[3] * delta_x /20  # 更新我船的X坐标
    os[1] += os[3] * delta_y /20  # 更新我船的Y坐标
    ts[0] += ts[3] * np.cos(np.deg2rad(Draw.angle_change(ts[2]))) # 更新他船的X坐标
    ts[1] += ts[3] * np.sin(np.deg2rad(Draw.angle_change(ts[2]))) # 更新他船的Y坐标
    
    # 记录轨迹
    os_track.append((os[0], os[1]))
    ts_track.append((ts[0], ts[1]))
    
    ax.clear()
    Draw.draw_ship(os, ax, 'gray', 'our_ship')
    Draw.draw_ship(ts, ax, 'blue', 'target_ship')

    os_x, os_y = zip(*os_track)
    ts_x, ts_y = zip(*ts_track)
    ax.plot(os_x, os_y, 'gray')
    ax.plot(ts_x, ts_y, 'blue')
    
    ax.set_xlim(-10, 10) # 设置X轴范围
    ax.set_ylim(-10, 10) # 设置Y轴范围

    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_title('Ship Positions and Headings')
    plt.grid(True)
    
# 创建船对象
os = [0.0, -8.0, 0.0, 0.1] # 我船的初始位置和速度
ts = [4.0, -1.0, 270.0, 0.08] # 他船的初始位置和速度
os_track = []  # 存储我船的轨迹
ts_track = []  # 存储他船的轨迹

goal = [0,10] #目标点位置

#人工势场参数
apf_values = {
    'k_att': 5, #吸引力势场系数
    'k_rep': 200, #排斥势场系数
    'd1': 6, #预设的迎头情况参考距离
    'd2': 6, #预设的交叉情况参考距离
    'd3': 2, #预设的超车情况参考距离
    'l_t': 10, #TS的影响半径
    'l_0': 10, #TS的影响半径
}
    
# 创建绘图窗口
fig, ax = plt.subplots()

# 创建动画对象
ani = FuncAnimation(fig, update, frames=np.arange(0, 200, 1), blit=False, repeat=False)

plt.show()

