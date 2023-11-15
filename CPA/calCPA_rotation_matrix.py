#使用旋转矩阵计算CPA

import numpy as np
from Ship import Ship

class calCPA:
    def __init__(self, ships):

        self.ships = Ship(np.array(ships))
   
    #经纬度位置
    def location(self):

        ships_x = self.ships.getLon()
        ships_y = self.ships.getLat()
        ships = np.concatenate((ships_x, ships_y), axis=1)
        
        return ships
    
    #他船与本船的速度矢量
    def calculate_relative_velocity(self):
        #必须要将radCor(使用弧度是因为三角函数是对弧度进行计算的)的值赋予变量
        #否则会重复对角度进行转换
        ships_radCor = self.ships.getradCor()
        
        v = self.ships.getSpd()
        
        v_x = v * np.cos(ships_radCor)
        v_y = v * np.sin(ships_radCor)
        
        #相对本船的速度
        relative_v = np.concatenate([v_x[1:] - v_x[0],v_y[1:] - v_y[0]], axis=1)

        return relative_v

    #距离投影下的位置矢量
    def distance_calculate_location(self, refer, in_coords):
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
        M = (a * (1 - e)) / (np.sqrt(1 - e * np.sin(refer[0,1]) * np.sin(refer[0,1]))) ** 3  # 子午圈曲率半径
        N = a / (np.sqrt(1 - e * np.sin(refer[0,1]) * np.sin(refer[0,1])))  # 卯酉圈曲率半径
        rLat = N * np.cos(refer[0,1])  # 纬线圈半径
    
        #以refer为原点
        num = in_coords.shape[0]
        ships_distance_location = np.zeros((num,2))
        ships_distance_location[:,0] = rLat * (in_coords[:,0] - refer[0,0])
        ships_distance_location[:,1] = M * (in_coords[:,1] - refer[0,1])

        #其他船的相对本船的位置矢量
        relative_location = ships_distance_location[1:] - ships_distance_location[0]

        return relative_location
    
    #DCPA & TCPA
    def getCPA(self):
        
        #所有船只的经纬度位置
        ships_location  = self.location()
        
        #距离投影下的船舶位置矢量
        refer = [[120.5,25.6]]
        ships_distance_location = self.distance_calculate_location(refer,ships_location)

        #所有船只的速度矢量
        relative_v = self.calculate_relative_velocity()

        #CPA
        #利用投影原理计算TCPA，利用相对速度和TCPA计算DCPA
        TCPA = np.diagonal(-np.dot(ships_distance_location,relative_v.T)/ np.dot(relative_v,relative_v.T))[:,np.newaxis]
        TCPA.flags.writeable = True#将数组设置为可写
        TCPA[TCPA < 0] = 0#判断元素是否小于0
        DCPA = np.linalg.norm(ships_distance_location + relative_v * TCPA,axis= 1).reshape(-1,1) #缺少DCPA正负的判断
        CPA = np.concatenate((DCPA,TCPA), axis=1)

        return CPA

#测试
ships = np.array([[0, 120.5, 25.6, 45.0, 10.0, 0, 0, 0, 0],#本船
                  [0, 113.0, 25.8, 68.0,  8.0, 0, 0, 0, 0],
                  [0, 116.0, 26.0, 180.0,  5.0, 0, 0, 0, 0],
                  [0, 116.2, 26.8, 14.0,  12.0, 0, 0, 0, 0],
                  [0, 114.3, 26.9, 96.0,  3.0, 0, 0, 0, 0],
                  [0, 125.4, 25.7, 37.0,  4.0, 0, 0, 0, 0],
                  [0, 119.0, 24.8, 75.0,  5.0, 0, 0, 0, 0],
                  [0, 123.2, 25.7, 160.0,  9.0, 0, 0, 0, 0],
                  [0, 124.6, 23.9, 45.0,  5.0, 0, 0, 0, 0],
                  [0, 118.5, 28.5, 75.0,  4.0, 0, 0, 0, 0],
                  [0, 117.0, 27.1, 48.0,  2.0, 0, 0, 0, 0],
                  [0, 119.3, 26.1, 25.0,  15.0, 0, 0, 0, 0]])


cpa = calCPA(ships)
CPA= cpa.getCPA()
print(CPA)