import numpy as np
import matplotlib.pyplot as plt

def random_walk_2D(steps):
    # 定义四个可能的方向：上、下、左、右
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    # 初始位置
    position = [0, 0]
    # 记录每一步的平方位移
    squared_displacement = [0]

    for _ in range(steps):
        # 随机选择一个方向
        direction = np.random.choice(range(4))
        # 更新位置
        position[0] += directions[direction][0]
        position[1] += directions[direction][1]
        # 计算平方位移并记录
        squared_displacement.append(position[0]**2 + position[1]**2)

    return squared_displacement

def main(M, steps):
    # 存储每个步骤的平均平方位移
    mean_squared_displacement = np.zeros(steps+1)
    
    for _ in range(M):
        # 对每个walker进行随机行走
        squared_displacement = random_walk_2D(steps)
        # 更新平均平方位移
        mean_squared_displacement += squared_displacement
    
    # 对所有walker的平均平方位移取平均
    mean_squared_displacement /= M
    
    # 绘制时间演变图
    plt.plot(range(steps+1), mean_squared_displacement)
    plt.xlabel('time t')
    plt.ylabel('expectation squared')
    plt.title('Graph')
    plt.show()

# 定义walkers数量和步数
M = 100
steps = 10000

# 运行主函数
main(M, steps)
