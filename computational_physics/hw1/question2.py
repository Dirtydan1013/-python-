import numpy as np
import matplotlib.pyplot as plt

def random_walk(steps):
    return np.random.choice([-1, 1], size=steps).cumsum()

def first_passage_time(positions):
    return np.argmax(np.abs(positions) == 0)

def main(num_walks, max_steps):
    first_passage_times = []
    
    for _ in range(num_walks):
        positions = random_walk(max_steps)
        first_passage_times.append(first_passage_time(positions))
    
    first_passage_times = np.array(first_passage_times)
    t_values = np.arange(1, max_steps + 1)
   
    # 计算首次通过概率 F(t)
    F_t = np.array([np.mean(first_passage_times <= t) for t in t_values])
    
    # 拟合 F(t) = t^a
    coeffs = np.polyfit(np.log(t_values), np.log(F_t), 1)
    a = coeffs[0]
    
    # 绘制结果
    plt.plot(t_values, F_t, 'o', label='Simulation')
    plt.plot(t_values, np.exp(coeffs[1]) * t_values**coeffs[0], label=f'Fit: a={a:.2f}')
    plt.xlabel('t')
    plt.ylabel('F(t)')
    plt.title('Time dependence of first-passage probability')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    num_walks = 1000
    max_steps = 100000
    main(num_walks, max_steps)

