#导入船舶信息
#[x,y,航向，速度]
#航向是以正北为正方向
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
        return self.cor
