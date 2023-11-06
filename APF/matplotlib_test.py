import matplotlib.pyplot as plt

# 定义坐标
x = [2, 4, 6, 8, 10]  # x坐标列表
y = [3, 5, 2, 7, 9]  # y坐标列表

# 使用plot函数绘制坐标
plt.plot(x, y, marker='o', color='red')  # 绘制坐标点，使用红色圆圈标记
plt.xlabel('X轴标签')  # 设置X轴标签
plt.ylabel('Y轴标签')  # 设置Y轴标签
plt.title('坐标点的图表')  # 设置图表标题
plt.show()  # 显示图表
