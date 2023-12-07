import numpy as np
import matplotlib.pyplot as plt
from calAPF2 import calAPF
import Draw
def get_vx(info):
    '''
    获得x方向上的速度
    '''
    vx = info[3] * np.sin(np.deg2rad(info[2]))
    return vx

def get_vy(info):
    '''
    获得y方向上的速度
    '''
    vy = info[3] * np.cos(np.deg2rad(info[2]))  
    return vy

def main():
    
    #参数设置
    os = [0.0, -8.0, 0.0, 0.1] # 我船的初始位置和速度
    ts = [4, 5.0, 270.0, 0.5] # 他船的初始位置和速度,速度为0时视为静态障碍物
    os_track = []  # 存储我船的轨迹
    ts_track = []  # 存储我船的轨迹
    goal = [0,10] #目标点位置

    #人工势场参数
    apf_values = {
        '_p':1, #目标位置引力系数
        '_v':0, #目标速度引力系数
        'eta_d':20, #远距离动态他船的斥力系数
        'eta_s':10, #远距离静态障碍物的斥力系数
        'eta_e':0, #近距离任何障碍物的斥力系数
        'R_ts' :0.5, #他船膨化圆半径
        'theta_m':90, #最大相对位置线夹角
        'cd' :6, #碰撞危险检测距离
        'dm' :3, #我船与他船的安全通过距离
        'rho_0':6, #他船或障碍物的斥力势场影响范围半径
        'tau':0.5, #紧急避碰区域大小
    }
    
    time_step= 0.1 #时间步长
    total_time = 8 #总时间
    
    for t in np.arange(0,total_time,time_step):
        
        apf = calAPF(os,ts,goal,apf_values)
        d = apf.distance_ship()
        theta = apf.theta()
        v = apf.relative_speed()
        position = apf.relative_position()
        #人工势场法更新船的位置    
        F = apf.F_total()
        # print('F = ',F)
        #计算加速度
        a_x = F[0]
        a_y = F[1]
        new_direction = np.rad2deg(np.arctan2(F[0], F[1]))
        
        #更新速度
        o_vx = get_vx(os) + a_x * time_step
        o_vy = get_vy(os) + a_y * time_step
        t_vx = get_vx(ts)
        t_vy = get_vy(ts)
        print(o_vx)
        #更新位置
        os[0] += o_vx * time_step  # 更新我船的X坐标
        os[1] += o_vy * time_step  # 更新我船的Y坐标
        ts[0] += t_vx * time_step   # 更新他船的X坐标
        ts[1] += t_vy * time_step   # 更新他船的Y坐标
        
        # 记录轨迹
        os_track.append((os[0], os[1]))
        ts_track.append((ts[0], ts[1]))

    x_y = 12
    ax = Draw.draw_fig(x_y)
    Draw.draw_ship(os, ax, 'green', 'our_ship')
    Draw.draw_ship(ts, ax, 'blue', 'target_ship')
    Draw.draw_track(os_track)
    Draw.draw_track(ts_track)
    Draw.draw_circle(ts,ax,6)
    Draw.draw_circle(ts,ax,3)
    
    plt.show()

if __name__ == '__main__':
    main()