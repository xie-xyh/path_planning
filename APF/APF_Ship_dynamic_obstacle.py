import numpy as np
import matplotlib.pyplot as plt

# 定义船舶和目标点的初始坐标
ship_position = np.array([1, 1])
target_position = np.array([9,9])

# 定义人工势场法参数
attractive_force_gain = 0.5 # 引力的增益系数
obstacle_force_gain = 0.2  # 斥力的增益系数
obstacle_influence = 2  # 障碍物对船舶产生作用的最大影响范围

obstacle_num = 1
# obstacle_position = np.random.uniform(0.9,1,(1, 2)) * 10  # 随机生成初始位置，假设地图大小是10x10
obstacle_position = np.random.uniform(3,4,(1, 2)) + np.array([0,2])  # 随机生成初始位置在（8，2）到（9，4）这个区域内

len_step = 0.05 #步长
n = 2 #改进的调节因子
num_iter = 500 #迭代次数
obstacle_num = 1 #障碍物个数

path = np.array([ship_position]) #保存船舶走过的每个点的坐标

# 定义栅格地图大小
grid_size = 11

# 创建栅格地图
grid_map = np.zeros((grid_size, grid_size))

def obstacle_change():
    
    #动态
    x_range = np.random.uniform(0,0.03, size=(obstacle_num, 1))  # 生成 x 坐标
    y_range = np.random.uniform(-0.1,0, size=(obstacle_num, 1))  # 生成 y 坐标
    position = np.hstack((x_range,y_range))

    return position

# 基于改进的APF计算人工势场力
def calculate_force(position,obstacle_position):

    #初始化
    obstacle_force = np.zeros((obstacle_num,2))#储存与所有障碍物之间的斥力
    # total_force = np.zeros((num,2))#储存与所有障碍物之间的合力

    obstacle_distance = np.zeros(obstacle_num)#储存与所有障碍物之间的距离
    target_distance = np.linalg.norm(position - target_position)#当前位置与目标点位置之间的欧氏距离

    #引力、斥力、合力计算
    attractive_force = -1 * attractive_force_gain * (position - target_position)#引力
    attractive_force = np.array([attractive_force])
    
    for i in range(obstacle_num):
        obstacle_distance[i] = np.linalg.norm(position - obstacle_position[i])#当前位置与单个障碍物位置之间的欧氏距离
        if obstacle_distance[i] < obstacle_influence:
            force_1 = obstacle_force_gain * (1 / obstacle_distance[i] - 1 / obstacle_influence) * (target_distance ** n / np.square(obstacle_distance[i]))#障碍物的斥力大小
            obstacle_force_1 = force_1 * ((position - obstacle_position[i]) / obstacle_distance[i]) #计算斥力1的向量
            force_2 = n / 2 * obstacle_force_gain * np.square(1 / obstacle_distance[i] - 1 / obstacle_influence) * target_distance ** (n - 1)#目标的斥力大小
            obstacle_force_2 = force_2 * (position - target_position) / target_distance #计算斥力2的向量
            obstacle_force[i] = obstacle_force_1 + obstacle_force_2
        else:
            obstacle_force[i] = 0#斥力为零向量

    if target_distance < 0.1:#到达目标点
        total_force = np.array([[0,0]]) 
    else:
        total_force = attractive_force + np.sum(obstacle_force,axis = 0)#计算所有障碍物的合力

    return total_force

# 更新船舶位置
def update_ship_position(position, force):
    
    new_position = position + force * len_step
    # 限制船舶位置在地图范围内
    new_position = np.clip(new_position, 0, grid_size - 0.1)
    
    return new_position

# 可视化地图和船舶路径
def visualize_map(grid_map, ship_position,path):
    plt.imshow(grid_map,cmap='cool')
    plt.plot(ship_position[0], ship_position[1],marker='o', color='red')#船舶初始位置
    plt.plot(target_position[0], target_position[1], marker='x', color='blue')#目标位置
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Ship Path Planning using Artificial Potential Field')
    plt.gca().invert_yaxis()  # 反转Y轴，确保Y轴标签按照期望的顺序显示
    
def visualize_path():
    plt.plot(path[:,0], path[:,1],color='black')#轨迹
    # plt.pause(0.1) #延时0.1s

def visualize_obstacle():
    plt.plot(obstacle_position[:,0], obstacle_position[:,1],marker='.',color='red')#障碍物


#主程序

# 将地图可视化
visualize_map(grid_map, path[0],path)

obstacle_position += obstacle_change()
print(obstacle_position)

for i in range(num_iter):


    if 0 <= obstacle_position[0][0] < grid_size-1 and 0 <= obstacle_position[0][1] < grid_size-1:
        obstacle_position += obstacle_change()
        # obstacle_position[0] = np.clip(obstacle_position[j], 0, grid_size - 1)
    # obstacle_position += obstacle_change()#得到障碍物变化图
    # obstacle_position = np.clip(obstacle_position, 0, grid_size - 1)#限制在地图中
    # print(obstacle_position)
    
    force = calculate_force(ship_position,obstacle_position)
    new_position = update_ship_position(ship_position,force)
    ship_position= np.squeeze(new_position)#将新的坐标降维成一维数组
    path = np.append(path,new_position,axis= 0) #保存更新后的位置信息，形成轨迹
    
    visualize_path()
    visualize_obstacle()
    plt.pause(0.1)
    # print(force)
    
    if np.array_equal(force, np.array([[0, 0]])):
        break

# 显示最终图形
plt.show()






