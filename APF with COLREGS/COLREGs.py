import numpy as np
from Ship import Ship
from calCPA import calCPA
#不考虑经纬度转换

#theta_T,phi_T,phi_0,R_T,DCPA

#所有角度均是以北为正方向
#ship_info包括坐标信息，以北为正方向的航向和速度信息

class COLREGs_byzheng(Ship):
    
    def __init__(self,os,ts):
        
        # 船舶信息
        self.os = os #我船
        self.ts = ts #他船
        self.ox = Ship(os).get_x # 我船位置
        self.oy = Ship(os).get_y
        self.tx = Ship(ts).get_x # 他船位置
        self.ty = Ship(ts).get_y
        self.ov = Ship(os).get_spd # 我船速度
        self.tv = Ship(ts).get_spd # 他船速度
        self.oc = Ship(os).get_cor # 我船航向
        self.tc = Ship(ts).get_cor # 他船航向

        self.num = None #遭遇种类
        self.encounter = None #遭遇类型
        # self.flag = 0 #是否进入遭遇标志位
    
    def judge(self):
        angle = abs(self.oc - self.tc) #航向夹角的绝对值
        R_T = self.cal_distance() #两船距离
        theta_T = self.angle_normalization(self.get_alpha_T() - self.oc)#他船位于本船的舷角
        theta_0 = self.angle_normalization(self.get_alpha_0() - self.tc)#本船位于他船的舷角
        
        DCPA,TCPA = calCPA(self.os,self.ts).getCPA()
        
        L_or_R = [False,False] #FT右转,TF左转,TT直航
        
        if R_T <= 6: #6海里是遭遇类型判断条件
            if 0 <= theta_T <= 5:
                L_or_R[0] = False
                L_or_R[1] = True
                if abs(180 - angle) <= 5:
                    self.num = 1
                    self.encounter = 'HEAD_ON'  # (1) 对遇，让路，右转
                else:
                    self.num = 2
                    self.encounter = 'CROSS'  # (2) 交叉，让路，右转
            elif 5 < theta_T <= 67.5:
                if abs(180 - angle) > 5:
                    L_or_R[0] = False
                    L_or_R[1] = True
                    self.num = 3
                    self.encounter = 'CROSS' # (3) 交叉，让路，右转
            elif 67.5 < theta_T <= 112.5:
                if abs(180 - angle) > 5:
                    L_or_R[0] = True
                    L_or_R[1] = False
                    self.num = 4
                    self.encounter = 'CROSS'  # (4) 交叉，让路，左转
            elif 112.5 < theta_T < 247.5:
                L_or_R[0] = True
                L_or_R[1] = True 
                self.num = 5
                self.encounter = 'OVERTAKE'  # (5)被追越，直航
            elif 247.5 < theta_T < 355:
                if abs(180 - angle) > 5:
                    L_or_R[0] = True
                    L_or_R[1] = True 
                    self.num = 6
                    self.encounter = 'CROSS'  # (6) 交叉，直航
            elif 355 <= theta_T <= 360:
                if abs(180 - angle) <= 5:
                    L_or_R[0] = False
                    L_or_R[1] = True
                    self.num = 7
                    self.encounter = 'HEAD_ON'  # (7) 对遇，让路，右转
                else:
                    L_or_R[0] = False
                    L_or_R[1] = True
                    self.num = 8
                    self.encounter = 'CROSS'  # (8) 交叉，让路，右转
            
            if R_T <= 3 and angle <= 67.5:#进入本船追越的判断
                if 112.5 <= theta_0 <= 180:
                    if DCPA < 0:
                        L_or_R[0] = True
                        L_or_R[1] = False
                        self.num = 9
                        self.encounter = 'OVERTAKE'  # (9) 追越，让路，左转
                    else:
                        L_or_R[0] = False
                        L_or_R[1] = True
                        self.num = 10
                        self.encounter = 'OVERTAKE'  # (10) 追越，让路，右转
                elif 180 < theta_0 <= 210:
                    if DCPA < 0:
                        L_or_R[0] = True
                        L_or_R[1] = False
                        self.num = 11
                        self.encounter = 'OVERTAKE'  # (11) 追越，让路，左转
                    else:
                        L_or_R[0] = False
                        L_or_R[1] = True
                        self.num = 12
                        self.encounter = 'OVERTAKE'  # (12) 追越，让路，右转
                elif 210 < theta_0 < 247.5:
                    if DCPA <= 0:
                        L_or_R[0] = True
                        L_or_R[1] = False
                        self.num = 14
                        self.encounter = 'OVERTAKE'  # (14) 追越，让路，左转
                    else:
                        L_or_R[0] = False
                        L_or_R[1] = True
                        self.num = 13
                        self.encounter = 'OVERTAKE'  # (13) 追越，让路，右转
                
        return L_or_R,self.encounter,self.num
    
    #计算距离
    def cal_distance(self):
        ox = self.ox
        oy = self.oy
        tx = self.tx
        ty = self.ty
        d = np.linalg.norm(np.array([ox, oy]) - 
                           np.array([tx, ty]))
        return d
    
    #转化为正北为正方向
    def angle_change(self, rad):
        deg = np.rad2deg(rad)
        if deg < 0:
            deg += 360
        if deg < 90:
            return 90 - deg
        else:
            return 450 - deg
    
    #他船相对本船的位置
    def get_alpha_T(self):
        theta = np.arctan2(self.ty - self.oy,
                           self.tx - self.ox)

        return self.angle_change(theta)

    #本船相对他船的位置
    def get_alpha_0(self):
        theta = np.arctan2(self.oy - self.ty,
                           self.ox - self.tx)

        return self.angle_change(theta)

    def angle_normalization(self, deg):
        if deg < 0:
            deg += 360
        elif deg > 360:
            deg -= 360
        return deg
    
    #遭遇类型
    def get_encounter(self):
        self.judge()
        return self.encounter
    
    #遭遇种类
    def get_num(self):
        self.judge()
        return self.num         

if  __name__ == '__main__':
    os = [0.0, 0.0, 0.0, 1] 
    ts = [2, 2.0, 270.0, 1.5] 
    a = COLREGs_byzheng(os,ts).judge()
    print(a)
