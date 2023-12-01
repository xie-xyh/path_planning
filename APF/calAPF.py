import sympy as sp
import numpy as np
import Ship
import COLREGs

class calAPF():
    def __init__(self,our_ship,target_ship,goal,apf_values):
        self.ox = Ship.Ship(our_ship).get_x() # 我船位置
        self.oy = Ship.Ship(our_ship).get_y()
        self.tx = Ship.Ship(target_ship).get_x() # 他船位置
        self.ty = Ship.Ship(target_ship).get_y()
        self.oc = Ship.Ship(our_ship).get_cor() # 我船角度
        self.tc = Ship.Ship(target_ship).get_cor() # 他船角度
        self.encounter = COLREGs.COLREGs_byzheng(our_ship,target_ship).get_encounter() #遭遇类型
        self.DCPA,self.TCPA = COLREGs.COLREGs_byzheng(our_ship,target_ship).getCPA() #CPA
        
        # 添加符号变量(我船)
        self.x, self.y = sp.symbols('x y')
        
        #目标点位置
        self.goal = goal
        
        # 势场参数
        self.k_att = apf_values[k_att]
        self.k_rep = apf_values[k_rep]
        self.d1 = apf_values[d1]
        self.d2 = apf_values[d2]
        self.d3 = apf_values[d3]
        self.l_t = apf_values[l_t]
        self.l_0 = apf_values[l_0]

    #计算距离
    def cal_d(self):
        
        d = sp.sqrt((self.x - self.tx)**2 + (self.y - self.ty)**2)
        
        return d
    
    # OS 到 TS 纵向中心线的距离 
    def cal_ds(self):
        theta = self.tc
         # 从正北向正东转换
        if theta < 180:
            theta = 90 - theta
        else:
            theta = 270 - theta
            
        theta = np.deg2rad(theta) #将角度转化为弧度
        # 处理直线垂直于x轴的情况
        if np.isclose(self.tc, 0) or np.isclose(theta, np.pi):
            ds =  self.x - self.tx #包含在左边和右边的情况
        else:
            k = np.tan(theta)
            a = k
            b = -1
            c = self.ty - k * self.tx
            
            #计算距离
            ds = self.judge_ds() * np.abs(a * self.ox + b * self.oy + c) / np.sqrt(a**2 + b**2)
        
        # ds = self.judge_ds() * self.DCPA
        
        if abs(ds) < 1e-10:
            ds = 0
            
        return ds
    
    # OS 到 TS 横向中心线的距离，也就是TCPA * VR
    def cal_ds_2(self):
        theta = self.tc
         # 从正北向正东转换
        if theta < 180:
            theta = 90 - theta
        else:
            theta = 270 - theta
            
        theta = np.deg2rad(theta) #将角度转化为弧度
        # 处理直线垂直于x轴的情况
        if np.isclose(self.tc, np.pi / 2) or np.isclose(theta, 3 * np.pi / 2):
            ds2 =  self.x - self.tx #包含在船尾和船头的情况
        else:
            k = -1 / np.tan(theta) #横向中心线的斜率
            a = k
            b = -1
            c = self.ty - k * self.tx
            
            #计算距离
            ds2 = self.judge_ds2() * np.abs(a * self.ox + b * self.oy + c) / np.sqrt(a**2 + b**2)
        
        # ds2 = self.judge_ds2() * np.sqrt(1-np.square(self.DCPA))
        
        if abs(ds2) < 1e-10:
            ds2 = 0
        
        return ds2
    
        #判断ds的正负
    def judge_ds(self):   
        # 直线方向向量,self.tc是以正北为正方向，因此sin和cos是反的
        dx = np.sin(np.deg2rad(self.tc))
        dy = np.cos(np.deg2rad(self.tc))
            
        # 从直线上的点到OS的向量
        ox_vec = self.ox - self.tx
        oy_vec = self.oy - self.ty

        # 计算叉积
        cross_product = ox_vec * dy - oy_vec * dx

        # 判断正负
        if cross_product < 0: #左边
            return -1 
        elif cross_product > 0: #右边
            return 1
        
    #判断ds的正负
    def judge_ds2(self):   
        # 直线方向向量,self.tc是以正北为正方向，因此sin和cos是反的
        dx = np.sin(np.deg2rad(self.tc))
        dy = np.cos(np.deg2rad(self.tc))

        # 从直线上的点到OS的向量
        ox_vec = self.ox - self.tx
        oy_vec = self.oy - self.ty

        # 计算点积
        dot_product = ox_vec * dx + oy_vec * dy

        # 判断正负
        if dot_product < 0: #后方
            return -1 
        elif dot_product > 0: #前方
            return 1
        
    #吸引力势场
    def U_att(self):
        # 定义符号变量
        sp.sqrt((self.x - self.tx)**2 + (self.y - self.ty)**2)
        d = sp.sqrt((self.x - goal[0])**2 + (self.y - goal[1])**2)#OS和目标点之间的距离
        U_att = 1 / 2 * self.k_att * d * d
        return U_att
    
    #对遇局面下的斥力势场
    def U_head_on(self):
        d = self.cal_d() #OS和TS之间的距离
        ds = self.cal_ds() #OS 到 TS 纵向中心线的距离
        
        # #真实值用于比较
        d_real = d.subs({self.x:self.ox, self.y:self.oy})
        # ds_real = ds.subs({self.x:self.ox, self.y:self.oy})
    
        if d_real < self.l_t and ds > -self.d1 and self.TCPA >= 0:
            U_rep = 1 / 2 * self.k_rep * np.square(ds + self.d1) / np.square(d)
        else:
            U_rep = 0
        return U_rep
    
    #交叉局面下的斥力势场
    def U_cross(self):
        d = self.cal_d() #OS和TS之间的距离
        ds2 = self.cal_ds() #OS 到 TS 横向中心线的距离
        
        #真实值用于比较
        d_real = d.subs({self.x:self.ox, self.y:self.oy})
        # ds2_real = ds2.subs({self.x:self.ox, self.y:self.oy})

        if d_real < self.l_0 and ds2 > -self.d2 and self.TCPA >= 0:
            U_rep = 1 / 2 * self.k_rep * np.square(ds2 + self.d2) / np.square(d)
        else:
            U_rep = 0
            
        return U_rep
    
    #总势场
    def U_total(self):
        
        if self.encounter == 'HEAD_ON':  # 对遇
            U = self.U_att() + self.U_head_on()
        elif self.encounter == 'CROSS':  # 交叉相遇
            U = self.U_att() + self.U_cross()
        elif self.encounter == 'OVERTAKE':  # 追越:
            pass
        else: #未到遭遇情况
            U = self.U_att() 
        
        return U
    
    #势场的梯度
    def gradient_U_total(self):

        U = self.U_total()
        
        # 计算梯度
        grad_x = sp.diff(U, self.x)
        grad_y = sp.diff(U, self.y)

        # 用当前位置替换
        grad_x = grad_x.subs({self.x: self.ox, self.y: self.oy}).evalf()
        grad_y = grad_y.subs({self.x: self.ox, self.y: self.oy}).evalf()

        return grad_x,grad_y  # 返回梯度的反方向，即下降最快的方向

if __name__ == '__main__':
    os = [0.0, 0.0, 0.0, 1] 
    ts = [1.0, 5.0, 270.0, 1.5] 

    goal = [10,10] #目标点位置

    #定义势场系数和其他参数
    k_att,k_rep, d1, d2, d3, l_t , l_0= sp.symbols('k_att k_rep d1 d2 d3 l_t l_0')

    #人工势场参数
    apf_values = {
        k_att: 5, #吸引力势场系数
        k_rep: 200, #排斥势场系数
        d1: 6, #预设的迎头情况参考距离
        d2: 6, #预设的交叉情况参考距离
        d3: 2, #预设的超车情况参考距离
        l_t: 10, #TS的影响半径
        l_0: 10, #TS的影响半径
    }

    a = calAPF(os,ts,goal,apf_values).gradient_U_total()
    # b = COLREGs.COLREGs_byzheng(os,ts).get_alpha_0() #遭遇类型
    print(a)
    # print(b)
