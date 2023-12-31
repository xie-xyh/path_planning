import numpy as np
from Ship import Ship

class calAPF():
    def __init__(self,os,ts,goal,apf_values) -> None:
        '''
        计算人工势场法合力
        输入参数:我船信息,
                他船信息,
                目标信息,
                人工势场法参数,
        '''
        self.ox = Ship(os).get_x # 我船位置
        self.oy = Ship(os).get_y
        self.tx = Ship(ts).get_x # 他船位置
        self.ty = Ship(ts).get_y
        self.ov = Ship(os).get_spd # 我船速度
        self.tv = Ship(ts).get_spd # 他船速度
        self.oc = Ship(os).get_cor # 我船角度
        self.tc = Ship(ts).get_cor # 他船角度
        self.r_os = Ship(os).get_r #我船领域半径
        self.r_ts = Ship(ts).get_r #他船领域半径
        
        self.gx = goal[0] #目标位置
        self.gy = goal[1] 

        #人工势场法参数
        self._p = apf_values['_p']
        self._v = apf_values['_v']
        self.eta_d = apf_values['eta_d']
        self.eta_s = apf_values['eta_s']
        self.eta_e = apf_values['eta_e']
        self.d_safe = apf_values['d_safe']
        self.rho_0 = apf_values['rho_0']
        self.tau = apf_values['tau']
        
    def F_total(self):
        '''
        合力
        输入参数:无
        输出参数:合力
        '''
        F = self.F_att() + self.F_req()
        return F
        
    def F_att(self):
        '''
        吸引力(靠近目标点时引力很小,速度很小)
        输入参数:无
        输出参数:吸引力
        '''
        F = self.F_att_p() + self.F_att_v()
        return F 

    def F_att_p(self):
        '''
        目标位置吸引力
        输入参数:无
        输出参数：目标位置吸引力
        '''
        p_os_g = np.array([self.gx - self.ox, self.gy - self.oy]) #船和目标的相对位置
        norm_p = np.linalg.norm(p_os_g) #模长
        if norm_p <= 0.01:
            F = 0
        else:
            F = self._p * p_os_g
        return F 
    
    def F_att_v(self):
        '''
        目标速度吸引力(目标跟踪的情况下)
        输入参数:速度引力因子
        '''
        return np.array([0,0])
    
    ## 应急避碰还没有加
    def F_req(self):
        '''
        斥力
        输入参数:无
        输出参数:斥力大小
        '''
        d = self.distance_ship()
        dm = self.d_m()
        cd = self.CD()
        theta = self.theta()
        theta_m = self.theta_m()
        if d > cd: #未进入避碰局面
            F = np.array([0,0])
        elif self.tv != 0 and dm < d < cd and theta < theta_m: #协商避碰，动态他船
            F = self.F_req_NZ_D()
        elif self.tv == 0 and dm < d < cd and theta < theta_m: #协商避碰，静态障碍物
            F = self.F_req_NZ_S()
        else: #应急避碰
            F = np.array([0,0])
        return F

    def F_req_NZ_D(self):
        '''
        协商避碰区(动态障碍物)
        输入参数:无
        输出参数:斥力大小
        '''
        eta_d = self.eta_d
        R_ts = self.r_ts
        theta_m = np.deg2rad(self.theta_m())
        theta = np.deg2rad(self.theta())
        d = self.distance_ship()
        dm = self.d_m()
        rho_0 = self.rho_0
        dg = self.distance_goal()
        v_ot = self.speed()
        # v_ot_2 = self.relative_speed()
        n_ot = [self.tx - self.ox , self.ty - self.oy] / d
        n_ot_2 = [-(self.ty - self.oy) , self.tx - self.ox] / d
        n_og = [self.gx - self.ox , self.gy - self.oy] / dg
        p_ot = self.distance_ship()
        # U = eta_d * R_ts * (np.exp(theta_m - theta)) * (1 / (d - dm) - 1 / rho_0) * dg * dg
        
        F_rd1 = - eta_d * R_ts * dg * dg * (((1 / (d - dm)) - (1 / rho_0)) * np.exp(theta_m - theta) * (dm / (d * np.sqrt(d * d - dm * dm)) + (np.sin(theta) / v_ot)) 
        + ((np.exp(theta_m - theta) - 1) / np.square(d - dm)) - (1 / (d - dm) - 1 / rho_0) * ((dm / (d * np.sqrt(d * d - dm * dm))) + (np.sin(theta_m) / v_ot))) * n_ot
        F_rd2 = - eta_d * R_ts * dg * dg * (((1 / (d - dm)) - (1 / rho_0)) * np.exp(theta_m - theta) * ( 1 / p_ot + np.cos(theta) / v_ot) + (v_ot * (np.exp(theta_m - theta) - 1) / (d * np.square(d - dm)))
        - (1 / (d - dm) - 1 / rho_0) * (1 / p_ot + np.cos(theta_m) / v_ot)) * n_ot_2
        F_rd3 = eta_d * R_ts * dg * ((1 / (d - dm)) - (1 / rho_0)) *  (np.exp(theta_m - theta) - 1) * n_og
        
        F = (F_rd1 + F_rd2 + F_rd3) 
        
        return F
    
    def F_req_NZ_S(self):
        '''
        协商避碰区(静态障碍物)
        输入参数:无
        输出参数:斥力大小
        '''
        eta_s = self.eta_s
        R_ts = self.r_ts
        d = self.distance_ship()
        tau = self.tau
        rho_0 = self.rho_0
        dg = self.distance_goal()
        n_ot = [self.tx - self.ox , self.ty - self.oy] / d
        n_og = [self.gx - self.ox , self.gy - self.oy] / dg
        # U = 1 / 2 * eta_s * R_ts * (1 / (d - tau) - 1 / rho_0) * dg * dg
        F_rs1 = eta_s * R_ts * (1 / (d - tau) - 1 / rho_0) * (dg * dg / (d * d)) * n_ot
        F_rs3 = eta_s * R_ts * dg * np.square(1 / (d - tau) - 1 / rho_0) * n_og
        F = F_rs1 + F_rs3
        return F
    
    def F_req_EZ(self):
        '''
        应急避碰区
        输入参数:无
        输出参数:斥力大小
        '''
        return
    
    def distance_goal(self):
        '''
        我船和目标之间的距离
        输入参数:无
        输出参数:位置距离大小
        '''
        p_os_g = [self.gx - self.ox,self.gy - self.oy] #船和目标的相对位置
        d = np.linalg.norm(p_os_g) #模长
        return d
    
    def relative_position(self):
        '''
        本船相对他船的位置
        输入参数:无
        输出参数:位置向量
        '''
        p = [self.tx - self.ox,self.ty - self.oy]
        
        return p
    def relative_speed(self):
        '''
        本船相对他船的速度
        输入参数:无
        输出参数:速度向量
        '''
        t_vx = self.tv * np.sin(np.deg2rad(self.tc))
        t_vy = self.tv * np.cos(np.deg2rad(self.tc))
        o_vx = self.ov * np.sin(np.deg2rad(self.oc))
        o_vy = self.ov * np.cos(np.deg2rad(self.oc))
        v = [o_vx - t_vx,o_vy - t_vy]
        
        return v
    
    def relative_speed_2(self):
        '''
        本船相对他船的速度的逆时针旋转90度
        输入参数:无
        输出参数:速度向量
        '''
        v = self.relative_speed()
        v_2 = [-v[1],v[0]] 
        
        return v_2
    
    def distance_ship(self):
        '''
        我船和他船(障碍物)的距离
        输入参数:无
        输出参数:距离
        '''
        d = np.linalg.norm(self.relative_position())
        
        return d
    
    def speed(self):
        '''
        我船和他船的相对速度大小
        输入参数:无
        输出参数:相对速度大小
        '''
        v = np.linalg.norm(self.relative_speed())
        
        return v
    
    def theta(self):
        '''
        相对位置线和相对速度线之间的夹角
        输入参数:无
        输出参数:角度
        '''
        p = self.relative_position()
        v = self.relative_speed()

        norm_p = self.distance_ship()
        norm_v = self.speed()
        
        theta_pot = np.rad2deg(np.arccos(p[0] / norm_p))
        theta_vot = np.rad2deg(np.arccos(v[0] / norm_v))
        angle = abs(theta_vot - theta_pot)
        
        return angle
    
    def theta_m(self):
        '''
        最大相对位置线夹角
        输入参数:无
        输出参数:角度
        '''
        d = self.distance_ship()
        dm = self.d_m()
        angle = np.rad2deg(np.arctan(dm / np.sqrt(d * d - dm * dm)))
        
        return angle
        
    def d_m(self):
        '''
        我船和他船之间的安全距离(领域半径)
        输入参数:无
        输出参数:安全距离
        '''
        R_os = self.r_os
        d_safe = self.d_safe
        R_ts = self.r_ts
        dm = R_os + d_safe + R_ts
        
        return dm
        
    def CD(self):
        '''
        碰撞危险检测距离
        输入参数:无
        输出参数:检测距离
        '''
        dm = self.d_m()
        CD = dm + self.rho_0
        
        return CD
        
    
def main():
    #船舶信息：x,y,航向,速度,膨化圆半径
    os = [5.0, 0.0, 45.0, 0.15, 0.5] # 我船的初始位置和速度
    ts = [9, 0.0, 315.0, 0.1, 0.3]  # 他船的信息，速度为零时视为静态障碍物

    goal = [0,10] #目标点位置

    apf_values = {
        '_p':3, #目标位置引力系数
        '_v':0, #目标速度引力系数
        'eta_d':2, #远距离动态他船的斥力系数
        'eta_s':20, #远距离静态障碍物的斥力系数
        'eta_e':0, #近距离任何障碍物的斥力系数
        'd_safe' :0.5, #我船和他船膨化圆边界之间的距离
        'rho_0':5, #他船或障碍物的斥力势场影响范围半径
        'tau':0.3, #紧急避碰区域大小
    }
    
    apf = calAPF(os,ts,goal,apf_values)
    # F_req = apf.F_req()
    # F_att = apf.F_att()
    # F = apf.F_total()
    # theta = apf.theta_m()
    # d_m = apf.d_m()
    # d = apf.distance_ship()
    v = apf.relative_speed()
    print(v)
    
    
if __name__ == '__main__':
    main()

