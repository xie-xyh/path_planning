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


def corss_B():
    #交叉相遇情况B
    os = [0.0, 0.0, 45.0, 0.15, 0.5] # 我船的初始位置和速度 
    ts = [9, 0.0, 315.0, 0.12, 0.3] # 他船的初始位置和速度,速度为0时视为静态障碍物
    return os,ts

def corss_A():
    #交叉相遇情况A
    os = [0.0, 0.0, 45.0, 0.15, 0.5] # 我船的初始位置和速度 
    ts = [0, 9.0, 135.0, 0.12, 0.3] # 他船的初始位置和速度,速度为0时视为静态障碍物
    return os,ts

def overtake():
    #追越情况
    os = [0.0, 0.0, 45.0, 0.15, 0.5] # 我船的初始位置和速度 
    ts = [5.0, 2.6, 0.0, 0.025, 0.3] # 他船的初始位置和速度,速度为0时视为静态障碍物
    return os,ts

def head_on():
    #迎头相遇情况
    os = [0.0, 0.0, 45.0, 0.15, 0.5] # 我船的初始位置和速度 
    ts = [7.3, 7.3, 225.0, 0.12, 0.3] # 他船的初始位置和速度,速度为0时视为静态障碍物
    return os,ts

def main():
    #参数设置
    os,ts = head_on()
    os_track = []  # 存储我船的轨迹
    ts_track = []  # 存储我船的轨迹
    goal = [10,10] #目标点位置

    #人工势场参数
    apf_values = {
        '_p':1, #目标位置引力系数
        '_v':0, #目标速度引力系数
        'eta_d':10, #远距离动态他船的斥力系数
        'eta_s':10, #远距离静态障碍物的斥力系数
        'eta_e':0, #近距离任何障碍物的斥力系数
        'd_safe' :0.5, #我船和他船膨化圆边界之间的距离
        'rho_0':5, #他船或障碍物的斥力势场影响范围半径
        'tau':0.5, #紧急避碰区域大小
    }
    
    time_step= 1 #时间步长
    total_time = 50 #总时间
    
    for t in np.arange(0,total_time,time_step):
        
        print('time_step = ',t)
        apf = calAPF(os,ts,goal,apf_values)
        dg = apf.distance_goal()
        if dg < 0.1: #如果到达终点就停止
            break
        CD = apf.CD()
        dm = apf.d_m()
        theta = apf.theta()
        theta_m = apf.theta_m()
        v = apf.relative_speed()
        position = apf.relative_position()
        #人工势场法更新船的位置    
        F = apf.F_total()
        print('theta = ',theta)
        print('theta_m = ',theta_m)
        print('os2 = ',os[2])
        
        F_direction = np.rad2deg(np.arctan2(F[0], F[1]))
        delta_direction = F_direction - os[2]
        print('F_direction = ',F_direction)
        #限定我船每步向左和向右转向不超过180
        if delta_direction > 180:
            delta_direction -= 360
        elif delta_direction < -180:
            delta_direction += 360
        
        #确定我船每步转向角度
        if delta_direction >= 0:
            delta_direction = min(delta_direction, 2.5)
        elif delta_direction < 0:
            delta_direction = max(delta_direction, -2.5)
            
        print('delta_direction = ',delta_direction)
        print()
        os[2] += delta_direction  # 逐步调整航向
        
        #更新速度
        o_vx = get_vx(os) 
        o_vy = get_vy(os) 
        t_vx = get_vx(ts)
        t_vy = get_vy(ts)

        #更新位置
        os[0] += o_vx * time_step # 更新我船的X坐标
        os[1] += o_vy * time_step # 更新我船的Y坐标
        ts[0] += t_vx * time_step   # 更新他船的X坐标
        ts[1] += t_vy * time_step   # 更新他船的Y坐标
        
        # 记录轨迹
        os_track.append((os[0], os[1]))
        ts_track.append((ts[0], ts[1]))

    x_y = 12 #坐标轴长度
    ax = Draw.draw_fig(x_y)
    Draw.draw_ship(os, ax, 'green', 'our_ship')
    Draw.draw_ship(ts, ax, 'blue', 'target_ship')
    Draw.draw_track(os_track)
    Draw.draw_track(ts_track)
    Draw.draw_circle(ts,ax,'green','CD',CD)
    Draw.draw_circle(ts,ax,'red','dm',dm)
    
    plt.show()

if __name__ == '__main__':
    main()