import numpy as np
from Ship import Ship
#不考虑经纬度转换

#theta_T,phi_T,phi_0,R_T,DCPA

#所有角度均是以北为正方向
#ship_info包括坐标信息，以北为正方向的航向和速度信息

#计算CPA
class calCPA:
    def __init__(self,my_ship,target_ship):
        self.my_ship = my_ship#我船信息
        self.target_ship = target_ship#他船信息
        
    #位置
    def location(self):
        xA = self.my_ship.get_x()
        yA = self.my_ship.get_y()
        xB = self.target_ship.get_x()
        yB = self.target_ship.get_y()
        
        return xA,xB,yA,yB
    
       #他船与本船的速度分量差
    def calculate_relative_velocity(self):
        #必须要将radCor(使用弧度是因为三角函数是对弧度进行计算的)的值赋予变量
        #否则会重复对角度进行转换
        shipA_radCor = np.deg2rad(self.my_ship.get_cor())
        shipB_radCor = np.deg2rad(self.target_ship.get_cor())
        
        vA = self.my_ship.get_spd()
        vB = self.target_ship.get_spd()
        
        vA_x = vA * np.cos(shipA_radCor)
        vA_y = vA * np.sin(shipA_radCor)
        vB_x = vB * np.cos(shipB_radCor)
        vB_y = vB * np.sin(shipB_radCor)
        
        #相对速度分量差
        vR_x = vB_x - vA_x
        vR_y = vB_y - vA_y

        return vR_x,vR_y
    
    #alpha（角度）
    def calculate_alpha(self):
        vR_x,vR_y = self.calculate_relative_velocity()
        if vR_x >= 0 and vR_y >= 0:
            return 0
        elif vR_x > 0 and vR_y < 0:
            return 360
        else:
            return 180

    #他船相对本船的相对速度航向phi(角度)
    def calculate_phi(self):
        vR_x, vR_y = self.calculate_relative_velocity()
        alpha = self.calculate_alpha()
        phi = np.rad2deg(np.arctan(vR_y/vR_x)) + alpha

        return phi
    
    #计算距离
    def cal_distance(self):
        d = np.linalg.norm(np.array([self.target_ship.get_x(),self.target_ship.get_y()]) - 
                           np.array([self.my_ship.get_x(),self.my_ship.get_y()]))
        return d
    
    #方位alpha_t（角度）
    def calculate_alpha_t(self):
        delta_y = self.target_ship.get_y() - self.my_ship.get_y()
        delta_x = self.target_ship.get_x() - self.my_ship.get_x()
        alpha = self.calculate_alpha()
        alpha_t = np.rad2deg(np.arctan(delta_y / delta_x)) + alpha

        return alpha_t
    
    def getCPA(self):
        
        #速度分量差
        vR_x,vR_y = self.calculate_relative_velocity()
        
        #相对速度
        vR = np.sqrt(np.square(vR_x) + np.square(vR_y))
        
        #相对速度航向
        phi = self.calculate_phi()
        
        #他船相对于本船的相对距离
        R_T = self.cal_distance()
        
        #他船相对于本船的真方位
        alpha_T = self.calculate_alpha_t()
        
        DCPA = R_T * np.sin(np.deg2rad(phi - alpha_T - np.pi))
        # TCPA = R_T * np.cos(np.deg2rad(phi - alpha_T - np.pi)) / vR
        
        return DCPA
    
class COLREGs_byzheng:
    def __init__(self,my_ship,target_ship):
        self.my_ship = Ship(my_ship)#我船信息
        self.target_ship = Ship(target_ship)#他船信息
        self.num = 0 #遭遇种类
        self.encounter = None #遭遇类型
        
    def judge(self):
        phi_T = self.target_ship.get_cor() #他船航向
        phi_0 = self.my_ship.get_cor() #本船航向
        angle = np.abs(phi_0 - phi_T) #航向夹角的绝对值
        R_T = self.cal_distance() #两船距离
        theta_T = self.angle_normalization(self.get_alpha_T() - phi_0)#他船位于本船的舷角
        theta_0 = self.angle_normalization(self.get_alpha_0() - phi_T)#本船位于他船的舷角
        DCPA = calCPA(self.my_ship,self.target_ship).getCPA()
        
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
        
            # else:
            #     L_or_R[0] = False
            #     L_or_R[1] = False
            #     self.num = 15
            #     self.encounter = 'None' #（15）未到避碰局面
        return L_or_R,self.encounter,self.num
    
    #计算距离
    def cal_distance(self):
        d = np.linalg.norm(np.array([self.target_ship.get_x(),self.target_ship.get_y()]) - 
                           np.array([self.my_ship.get_x(),self.my_ship.get_y()]))
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
        theta = np.arctan2(self.target_ship.get_y() - self.my_ship.get_y(),
                           self.target_ship.get_x() - self.my_ship.get_x())

        return self.angle_change(theta)

    #本船相对他船的位置
    def get_alpha_0(self):
        theta = np.arctan2(self.my_ship.get_y() - self.target_ship.get_y(),
                           self.my_ship.get_x() - self.target_ship.get_x())

        return self.angle_change(theta)

    def angle_normalization(self, deg):
        if deg < 0:
            deg += 360
        elif deg > 360:
            deg -= 360
        return deg

    #遭遇类型
    def get_encounter(self):
        return self.encounter
    
    #遭遇种类
    def get_num(self):
        return self.num

# shipA = [1.0, 6.0, 30.0, 10.0]
# shipB = [3.0, 4.0, 120.0, 12.0]

# L_or_R,encounter,num = COLREGs_byzheng(shipA,shipB).judge()

# print(f"theta_T: {theta_T}")
# print(f"theta_0: {theta_0}")
# print(f"DCPA: {DCPA}")
# print(f"L_or_R: {L_or_R}")
# print(f"Encounter Type: {encounter}")
# print(f"Encounter Num: {num}")
