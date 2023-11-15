import numpy as np
from Ship import Ship

#所有计算的角度均以正东为正方向，逆时针为正
#输入的角度为真实方向，即以正北为正方向
class calCPA:
    def __init__(self, shipA, shipB):
        self.shipA = Ship(shipA)
        self.shipB = Ship(shipB)
    
    #经纬度位置
    def location(self):
        
        xA = self.shipA.getLon()#经度
        yA = self.shipA.getLat()#纬度
        xB = self.shipB.getLon()#经度
        yB = self.shipB.getLat()#纬度
        
        return xA, yA, xB, yB
    
    #他船与本船的速度分量差
    def calculate_relative_velocity(self):
        #必须要将radCor(使用弧度是因为三角函数是对弧度进行计算的)的值赋予变量
        #否则会重复对角度进行转换
        shipA_radCor = self.shipA.getradCor()
        shipB_radCor = self.shipB.getradCor()
        
        vA = self.shipA.getSpd()
        vB = self.shipB.getSpd()
        
        vA_x = vA * np.cos(shipA_radCor)
        vA_y = vA * np.sin(shipA_radCor)
        vB_x = vB * np.cos(shipB_radCor)
        vB_y = vB * np.sin(shipB_radCor)
        
        #相对速度分量差
        vR_x = vB_x - vA_x
        vR_y = vB_y - vA_y

        return vR_x,vR_y

    #alpha
    def calculate_alpha(self):
        vR_x,vR_y = self.calculate_relative_velocity()
        if vR_x >= 0 and vR_y >= 0:
            return 0
        elif vR_x > 0 and vR_y < 0:
            return 360
        else:
            return 180

    #他船相对本船的相对速度航向phi
    def calculate_phi(self):
        vR_x, vR_y = self.calculate_relative_velocity()
        alpha = self.calculate_alpha()
        phi = np.rad2deg(np.arctan(vR_y/vR_x)) + alpha

        return phi

    #距离投影下的坐标
    def calculate_location(self, refer, in_coords):
        # 距离投影，以某一点refer为原点，获得in相对refer点横纵坐标米的坐标
        # input
        # refer 参考点的经纬度坐标
        # in_coords 待求点的经纬度坐标 

        #角度转化为弧度
        refer = np.deg2rad(refer)
        in_coords = np.deg2rad(in_coords)

        #地球参数
        a = 6378137  # 长轴
        b = 6356752  # 短轴
        e = (a * a - b * b) / (a * a)  # 第一偏心率
        M = (a * (1 - e)) / (np.sqrt(1 - e * np.sin(refer[1]) * np.sin(refer[1]))) ** 3  # 子午圈曲率半径
        N = a / (np.sqrt(1 - e * np.sin(refer[1]) * np.sin(refer[1])))  # 卯酉圈曲率半径
        rLat = N * np.cos(refer[1])  # 纬线圈半径
    
        #以refer为原点
        num = in_coords.shape[1]
        Tc = np.zeros((num,2))
        for i in range(num):
            Tc[i,0] = rLat * (in_coords[i,0] - refer[0])#横坐标
            Tc[i,1] = M * (in_coords[i,1] - refer[1])#纵坐标
            
        return Tc
    
    #距离投影下的相对距离
    def calculate_distance(self,Tc):
        num = Tc.shape[0]
        distanceT = np.zeros((num - 1,1))
        
        for i in range(1,num):
            delta_x = Tc[i,0] - Tc[0,0]
            delta_y = Tc[i,1] - Tc[0,1]
            distanceT[i - 1] = np.sqrt(np.square(delta_x)+np.square(delta_y))
        
        return delta_x,delta_y,distanceT

    #方位alpha_t
    def calculate_alpha_t(self, delta_x,delta_y):
        
        alpha = self.calculate_alpha()
        alpha_t = np.rad2deg(np.arctan(delta_y / delta_x)) + alpha

        return alpha_t
    
    #判断是否存在CPA
    def judge_CPA(self,location,phi):
        
        x1 = location[0,0]
        y1 = location[0,1]#本船
        x2 = location[1,0]
        y2 = location[1,1]#他船
    
        if np.abs(x2 - x1) < 0.01:
            connect_k = float('inf') # 垂直线的斜率为无穷大   
            k = 0

        elif np.abs(y2-y1) < 0.01:
            connect_k = 0
            k = float('inf') # k斜率无穷大
        
        else:
            connect_k = (y2 - y1) / (x2 - x1)#两点的连线斜率
            k = -1 / connect_k #与连线垂直的线的斜率
        
        b = y2 - k*x2 #经过他船的直线
        length = 100
        y = y2 + length * np.sin(np.deg2rad(phi))#预估值

        if(y2 > y1):#他船在上
            if y >= k * (x2 + length * np.cos(np.deg2rad(phi)))+b:
                flag = 0#无CPA
            else:
                flag = 1#有CPA
        else:#他船在下
            if y > k * (x2 + length * np.cos(np.deg2rad(phi)))+b:
                flag = 1#有CPA
            else:
                flag = 0#无CPA
        
        return flag
    
    #DCPA & TCPA
    def getCPA(self):
        
        #经纬度位置
        xA, yA, xB, yB = self.location()
        
        #速度分量差
        vR_x,vR_y = self.calculate_relative_velocity()
        
        #相对速度
        vR = np.sqrt(np.square(vR_x) + np.square(vR_y))

        alpha = self.calculate_alpha()

        #相对速度航向
        phi = self.calculate_phi()

        #他船的相对坐标(笛卡尔坐标系)
        refer = [120.5,25.6]#参照点的经纬度坐标
        in_coords = [[xA,yA],[xB,yB]]
        location = self.calculate_location(refer,in_coords)
        
        #他船相对于本船的相对距离
        delta_x,delta_y,R_T = self.calculate_distance(location)
        
        #他船相对于本船的真方位
        alpha_T = self.calculate_alpha_t(delta_x, delta_y)

        # #判断有无CPA
        flag = self.judge_CPA(location,phi)
        
        if(flag == 0):
            DCPA = R_T
            TCPA = 0
        else:
            DCPA = np.abs(R_T * np.sin(np.deg2rad(phi - alpha_T)))
            TCPA = np.abs(R_T * np.cos(np.deg2rad(phi - alpha_T)) / vR)
        
        return DCPA, TCPA

shipA = np.array([[123456789, 120.5, 25.6, 45.0, 10.0, 90.0, 50.0, 15.0, 123]])
shipB = np.array([[987654321, 121.0, 25.8, 120.0, 8.0, 120.0, 40.0, 12.0, 321]])

cpa = calCPA(shipA,shipB)

print(cpa.getCPA())