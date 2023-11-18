import numpy as np
class Ship:
    def __init__(self, ship_info):
        self.x = ship_info[0]
        self.y = ship_info[1]
        self.cor = ship_info[2] #航向
        self.spe = ship_info[3] #速度

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_spd(self):
        return self.spe

    def get_cor(self):
        return np.where(self.cor <= 90,90-self.cor,450 - self.cor)
