import math

class Ship:
    def __init__(self, ship_info):
        self.x = ship_info[0]
        self.y = ship_info[1]
        self.cor = ship_info[2]
        self.spe = ship_info[3]

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_spe(self):
        return self.spe

    def get_cor(self):
        return self.cor


class Zheng:
    def __init__(self, ships_info):
        self.our_ship = Ship(ships_info[0])
        self.target_ship = Ship(ships_info[1])
        self.encounter = None

    def get_result(self):
        rel = [False, False]
        t_phi = self.target_ship.get_cor()
        o_phi = self.our_ship.get_cor()
        CT = t_phi - o_phi  # 航向交角

        ca = self.angle_normalization(self.get_AT() - o_phi)  # 他船相对于我船的弦角

        if 0 <= ca <= 5:
            rel[0] = True
            rel[1] = True
            if abs(180 - abs(CT)) <= 5:
                self.encounter = 'HEAD_ON'  # (1) 对遇，让路，右转
            else:
                self.encounter = 'CROSS'  # (2) 交叉，让路，右转
        elif 5 < ca <= 67.5:
            if abs(180 - abs(CT)) > 5:
                rel[0] = True
                rel[1] = True
                self.encounter = 'CROSS'  # (3) 交叉，让路，右转
        elif 67.5 < ca <= 112.5:
            if abs(180 - abs(CT)) > 5:
                rel[0] = True
                rel[1] = False
                self.encounter = 'CROSS'  # (4) 交叉，让路，左转
        elif 112.5 < ca < 247.5:
            rel[0] = False
            self.encounter = 'OVERTAKE'  # (5)被追越，直航
        elif 247.5 < ca < 355:
            if abs(180 - abs(CT)) > 5:
                rel[0] = False
                self.encounter = 'CROSS'  # (6) 交叉，直航
        elif 355 <= ca <= 360:
            if abs(180 - abs(CT)) <= 5:
                rel[0] = True
                rel[1] = True
                self.encounter = 'HEAD_ON'  # (7) 对遇，让路，右转
            else:
                rel[0] = True
                rel[1] = True
                self.encounter = 'CROSS'  # (8) 交叉，让路，右转

        # 以他船为中心判断 / 存在一些问题
        ca_t = self.angle_normalization(self.get_AO() - t_phi)
        if abs(CT) < 67.5:
            if 112.5 <= ca_t <= 180:
                rel[0] = True
                rel[1] = True
                self.encounter = 'OVERTAKE'  # (9 - 10) 追越，让路，右转
            elif 180 < ca_t <= 210:
                rel[0] = True
                rel[1] = False
                self.encounter = 'OVERTAKE'  # (11 -12) 追越，让路，左转
            elif 210 < ca_t <= 247.5:
                rel[0] = True
                rel[1] = False
                self.encounter = 'OVERTAKE'  # (11 -12) 追越，让路，左转

        return rel

    def rad2deg(self, rad):
        deg = rad / math.pi * 180
        if deg < 0:
            deg += 360
        if deg < 90:
            return 90 - deg
        else:
            return 450 - deg

    def get_AT(self):
        theta = math.atan2(self.target_ship.get_y() - self.our_ship.get_y(),
                           self.target_ship.get_x() - self.our_ship.get_x())

        return self.rad2deg(theta)

    def get_AO(self):
        theta = math.atan2(self.our_ship.get_y() - self.target_ship.get_y(),
                           self.our_ship.get_x() - self.target_ship.get_x())

        return self.rad2deg(theta)

    def angle_normalization(self, deg):
        while deg < 0 or deg > 360:
            if deg < 0:
                deg += 360
            else:
                deg -= 360
        return deg

    def get_encounter(self):
        return self.encounter


# 示例用法
ships_info = [[1.0, 2.0, 30.0, 10.0], [3.0, 4.0, 120.0, 12.0]]
zheng_instance = Zheng(ships_info)
result = zheng_instance.get_result()
encounter_type = zheng_instance.get_encounter()
print("Collision Result:", result)
print("Encounter Type:", encounter_type)
