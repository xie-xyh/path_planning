import numpy as np

class Ship():
    def __init__(self, data_list):
        self.MMSI = data_list[:, 0].reshape(-1, 1)  # MMSI
        self.lon = data_list[:, 1].reshape(-1, 1)  # 经度
        self.lat = data_list[:, 2].reshape(-1, 1)  # 纬度
        self.cor = data_list[:, 3].reshape(-1, 1)  # 航向(非实际方向)
        self.spd = data_list[:, 4].reshape(-1, 1)  # 航速
        self.phi = data_list[:, 5].reshape(-1, 1)  # 艏向
        self.len = data_list[:, 6].reshape(-1, 1)  # 船长
        self.wid = data_list[:, 7].reshape(-1, 1)  # 船宽
        self.stamp = data_list[:, 8].reshape(-1, 1)  # 时间戳

        self.radCor = self.cor  #转化为弧度的航向
        self.radPhi = self.phi  #转换为弧度的艏向
        self.ktSpd = self.spd   #以节为单位的速度
    # 经度
    def getLon(self):
        return self.lon

    def setLon(self, new_lon):
        self.lon = new_lon

    # 纬度
    def getLat(self):
        return self.lat

    def setLat(self, new_lat):
        self.lat = new_lat

    # 航向(正方向从正北转为正东)
    def getCor(self):
        # 将绝对方向值转换到0到360度之间
        self.cor = np.where(self.cor <= 90,90-self.cor,450 - self.cor)
        
        return self.cor

    def setCor(self, new_cor):
        self.cor = new_cor

    # 航速(m/s),默认给予的值是节为单位的速度
    def getSpd(self):
        self.spd = self.spd * 1852 / 3600
        return self.spd

    def setSpd(self, new_spd):
        self.spd = new_spd

    # 艏向(正方向从正北转为正东)
    def getPhi(self):
        # 将绝对方向值转换到0到360度之间
        self.phi = np.where(self.phi <= 90,90-self.phi,450 - self.phi)
        return self.phi

    def setPhi(self, new_phi):
        self.phi = new_phi

    # 船长
    def getLen(self):
        return self.len

    def setLen(self, new_len):
        self.len = new_len

    # 船宽
    def getWid(self):
        return self.wid

    def setWid(self, new_wid):
        self.wid = new_wid

    # 时间戳
    def getStamp(self):
        return self.stamp

    def setStamp(self, new_stamp):
        self.stamp = new_stamp

    # 转换为弧度的航向
    def getradCor(self):
        # 将绝对方向值转换到0到360度之间
        self.radCor = np.where(self.radCor <= 90,90-self.radCor,450 - self.radCor)
        self.radCor = np.deg2rad(self.radCor)
        return self.radCor

    def setradCor(self, new_radCor):
        self.radCor = new_radCor

    # 转换为弧度的艏向
    def getradPhi(self, data_list):
        # 将绝对方向值转换到0到360度之间
        self.radPhi = np.where(self.radPhi <= 90,90-self.radPhi,450 - self.radPhi)
        self.radPhi = np.deg2rad(self.radPhi)
        return self.radPhi

    def setradPhi(self, new_radPhi):
        self.radPhi = new_radPhi

    # 以节为单位的速度（节每小时）
    def getktSpd(self):
        return self.ktSpd

    def setKtSpd(self, new_ktSpd):
        self.ktSpd = new_ktSpd
