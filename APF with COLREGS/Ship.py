#导入船舶信息
#[x,y,航向，速度]
#航向是以正北为正方向
class Ship:
    def __init__(self, ship_info):
        self._x = ship_info[0]
        self._y = ship_info[1]
        self._cor = ship_info[2] #航向
        self._spe = ship_info[3] #速度

    @property
    def get_x(self):
        return self._x

    @property
    def get_y(self):
        return self._y

    @property
    def get_spd(self):
        return self._spe

    @property
    def get_cor(self):
        return self._cor
