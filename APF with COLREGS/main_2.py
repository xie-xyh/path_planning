import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from calAPF2 import calAPF
import Draw
    
def main():
    # 更新船的位置
    def update(frame):

        apf = calAPF(os,ts,goal,apf_values)
        #人工势场法更新船的位置
        F = apf.F_total()
        print(F)
        os[0] += os[3] * F[0] / 10  # 更新我船的X坐标
        os[1] += os[3] * F[1] / 10 # 更新我船的Y坐标
        # 记录轨迹
        os_track.append((os[0], os[1]))
        ts_track.append((ts[0], ts[1]))
        
        ax.clear()
        Draw.draw_ship(os, ax, 'gray', 'our_ship')
        Draw.draw_ship(ts, ax, 'blue', 'target_ship')

        #显示轨迹
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
    ts = [0.2, 0.0, 0.0, 0.0] # 他船的初始位置和速度,速度为0时视为静态障碍物
    os_track = []  # 存储我船的轨迹
    ts_track = []  # 存储他船的轨迹

    goal = [0,10] #目标点位置

    #人工势场参数
    apf_values = {
        '_p':1, #目标位置引力系数
        '_v':0, #目标速度引力系数
        'eta_d':0, #远距离动态他船的斥力系数
        'eta_s':10, #远距离静态障碍物的斥力系数
        'eta_e':0, #近距离任何障碍物的斥力系数
        'R_ts' :0.5, #他船膨化圆半径
        'theta_m':45, #最大相对位置线夹角
        'cd' :6, #碰撞危险检测距离
        'dm' :3, #我船与他船的安全通过距离
        'rho_0':6, #他船或障碍物的斥力势场影响范围半径
        'tau':0.5, #紧急避碰区域大小
    }
        
    # 创建绘图窗口
    fig, ax = plt.subplots()

    # 创建动画对象
    ani = FuncAnimation(fig, update, frames=np.arange(0, 1000, 1), blit=False, repeat=False)

    plt.show()

if __name__ == '__main__':
    main()