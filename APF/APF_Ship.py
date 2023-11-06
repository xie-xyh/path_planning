import numpy as np
import matplotlib.pyplot as plt

# 定义船舶和目标点及障碍物的初始坐标
ship_position = np.array([0, 0])
target_position = np.array([9,9])
# obstacle_position = np.array([[1.1,0.9],
                            #   [2.4,2.5],
                            #   [2.9,3.1],
                            #   [3.8,4.0],
                            #   [4.0,5.0],
                            #   [5.9,6.2],
                            #   [8.1,8.3]])

# 定义人工势场法参数
attractive_force_gain = 0.5 # 引力的增益系数
repulsive_force_gain = 0.2  # 斥力的增益系数
repulsive_distance = 1.5  # 障碍物对船舶产生作用的最大影响范围

len_step = 0.05 #步长
n = 1 #改进的调节因子
num_iter = 500 #迭代次数
obstacle_num = 15 #障碍物个数

path = np.array([ship_position]) #保存船舶走过的每个点的坐标

# 定义栅格地图大小
grid_size = 10

# 创建栅格地图
grid_map = np.zeros((grid_size, grid_size))

def obstacle_generation():
    
    for i in range(obstacle_num):
        # 生成随机斜率和截距
        k = np.random.uniform(0.9,1.1,(obstacle_num,1))  # 随机斜率，避免斜率为0
        b = np.random.uniform(-1,1,(obstacle_num,1)) # 随机截距,0-1的范围内
        
        x = np.random.uniform(1, 8.5, (obstacle_num, 1)) #在1-8.5之间随机生成x坐标
        y = k * x + b

    obstacle_position = np.column_stack((x, y)) #将x坐标和y坐标合成为二维数组

    return obstacle_position

# 基于改进的APF计算人工势场力
def calculate_force(position,obstacle_position):

    #初始化
    repulsive_force = np.zeros((obstacle_num,2))#储存与所有障碍物之间的斥力
    # total_force = np.zeros((num,2))#储存与所有障碍物之间的合力

    obstacle_distance = np.zeros(obstacle_num)#储存与所有障碍物之间的距离
    target_distance = np.linalg.norm(position - target_position)#当前位置与目标点位置之间的欧氏距离

    #引力、斥力、合力计算
    attractive_force = -1 * attractive_force_gain * (position - target_position)#引力
    attractive_force = np.array([attractive_force])
    
    for i in range(obstacle_num):
        obstacle_distance[i] = np.linalg.norm(position - obstacle_position[i])#当前位置与单个障碍物位置之间的欧氏距离
        if obstacle_distance[i] < repulsive_distance:
            force_1 = repulsive_force_gain * (1 / obstacle_distance[i] - 1 / repulsive_distance) * (target_distance ** n / np.square(obstacle_distance[i]))#障碍物的斥力大小
            repulsive_force_1 = force_1 * ((position - obstacle_position[i]) / obstacle_distance[i]) #计算斥力1的向量
            force_2 = n / 2 * repulsive_force_gain * np.square(1 / obstacle_distance[i] - 1 / repulsive_distance) * target_distance ** (n - 1)#目标的斥力大小
            repulsive_force_2 = force_2 * (position - target_position) / target_distance #计算斥力2的向量
            repulsive_force[i] = repulsive_force_1 + repulsive_force_2
        else:
            repulsive_force[i] = 0#斥力为零向量

        
    total_force = attractive_force + np.sum(repulsive_force,axis = 0)#计算所有障碍物的合力

    return total_force

# print(calculate_force(ship_position,obstacle_position))
# 更新船舶位置
def update_ship_position(position, force):
    
    new_position = position + force * len_step
    # 限制船舶位置在地图范围内
    new_position = np.clip(new_position, 0, grid_size - 0.1)
    
    return new_position

# 可视化地图和船舶路径
def visualize(grid_map, ship_position,obstacle_position,path):
    plt.imshow(grid_map,cmap='cool')
    plt.plot(ship_position[0], ship_position[1],marker='o', color='red')#船舶初始位置
    plt.plot(target_position[0], target_position[1], marker='x', color='blue')#目标位置
    plt.plot(obstacle_position[:, 0], obstacle_position[:, 1],marker='v', color='green',linestyle='None')#离散的障碍物位置
    plt.plot(path[:, 0], path[:, 1], color='black')#轨迹
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Ship Path Planning using Artificial Potential Field')
    plt.gca().invert_yaxis()  # 反转Y轴，确保Y轴标签按照期望的顺序显示
    plt.show()

#主程序

obstacle_position = obstacle_generation() #随机生成障碍物位置

for i in range(num_iter):
    force = calculate_force(ship_position,obstacle_position)
    new_position = update_ship_position(ship_position,force)
    ship_position= np.squeeze(new_position)#将新的坐标降维成一维数组
    path = np.append(path,new_position,axis= 0) #保存更新后的位置信息，形成轨迹

print(path)

# 将船舶路径可视化
visualize(grid_map, path[0],obstacle_position,path)


