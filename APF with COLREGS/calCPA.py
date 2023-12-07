#使用向量计算CPA

import numpy as np
from Ship import Ship

class calCPA:
    def __init__(self, os, ts):
       
        self.ox = Ship(os).get_x # 我船位置
        self.oy = Ship(os).get_y
        self.tx = Ship(ts).get_x # 他船位置
        self.ty = Ship(ts).get_y
        self.ov = Ship(os).get_spd # 我船速度
        self.tv = Ship(ts).get_spd # 他船速度
        self.oc = Ship(os).get_cor # 我船航向
        self.tc = Ship(ts).get_cor # 他船航向
        
    #计算相对速度
    def cal_vR(self):
        #将航向角度转化为弧度
        phi_0 = np.deg2rad(self.oc) #本船航向
        phi_T = np.deg2rad(self.tc) #他船航向

        #角度是以北为正方向,因此sin和cos是反的
        v0_x = self.ov * np.sin(phi_0)
        v0_y = self.ov * np.cos(phi_0)
        vT_x = self.tv * np.sin(phi_T)
        vT_y = self.tv * np.cos(phi_T)

        vR_x = vT_x - v0_x
        vR_y = vT_y - v0_y
        
        return np.array([vR_x,vR_y])
    
    #求CPA(向量方式)
    def getCPA(self):
        vR = self.cal_vR()

        ships_distance_location = np.array([self.tx - self.ox,
                                            self.ty - self.oy])

        TCPA = -np.dot(ships_distance_location,vR)/ np.linalg.norm(vR)**2
        DCPA = np.linalg.norm(ships_distance_location + vR * TCPA) #缺少DCPA正负的判断
        
        if abs(DCPA) < 1e-10:
            DCPA = 0
        
        return DCPA,TCPA

#测试
if __name__ == '__main__':
    os = [0.0, 0.0, 0.0, 1] 
    ts = [5.0, -5.0, 270.0, 1.5] 
    CPA= calCPA(os,ts).getCPA()
    print(CPA)