import numpy as np

def determine_collision_action(theta_tau, phi_T, phi_0, R_T, alpha_T, DCPA, u_T):
    # 情况1-8的条件判断
    if 0 <= theta_tau <= 5 and R_T <= 6 and u_T == 1:
        if abs(180 - abs(phi_T - phi_0)) <= 5:
            return 1 #对遇，本船右转
        elif abs(180 - abs(phi_T - phi_0)) > 5:
            return 2 #交叉相遇，本船右转
    elif 5 <= theta_tau <= 67.5 and abs(180 - abs(phi_T - phi_0)) > 5 and R_T <= 6 and u_T == 1:
        return 3 #交叉相遇，本船右转
    elif 67.5 <= theta_tau <= 112.5 and abs(180 - abs(phi_T - phi_0)) > 5 and R_T <= 6 and u_T == 1:
        return 4 #交叉相遇，本船左转
    elif 112.5 <= theta_tau <= 247.5 and R_T <= 3 and u_T == 1:
        if abs(180 - abs(phi_T - phi_0)) > 5:
            return 6 #交叉相遇，直行
        else:
            return 5 #他船追越，直行
    elif 247.5 <= theta_tau <= 335 and abs(180 - abs(phi_T - phi_0)) > 5 and R_T <= 6 and u_T == 1:
        return 8
    elif 355 <= theta_tau <= 360 and R_T <= 6 and u_T == 1:
        if abs(180 - abs(phi_T - phi_0)) <= 5:
            return 7
        else:
            return 8
    # 情况9-14的条件判断
    elif abs(phi_0 - phi_T) <= 67.5 and R_T <= 3 and u_T == 1:
        if 112.5 + phi_T <= alpha_T + 180 <= 180 + phi_T:
            if DCPA < 0:
                return 9
            else:
                return 10
        elif 180 + phi_T <= alpha_T + 180 <= 210 + phi_T:
            if DCPA < 0:
                return 11
            else:
                return 12
        elif 210 + phi_T <= alpha_T + 180 <= 247.5 + phi_T:
            if DCPA > 0:
                return 13
            else:
                return 14
    return "无法判定"
