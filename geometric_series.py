# 下載需要的套件
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (11,5)
import numpy as np
import sympy as sym
from sympy import init_printing, latex
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# True present value of a finite lease
def finite_lease_pv_true(T, g, r, x_0):
   G = (1 + g)
   R = (1 + r)
   return (x_0 * (1 - G**(T + 1) * R**(-T - 1))) / (1 - G * R**(-1))

# First approximation for our finite lease
def finite_lease_pv_approx_1(T, g, r, x_0):
   p = x_0 * (T + 1) + x_0 * r * g * (T + 1) / (r - g)
   return p

# Second approximation for our finite lease
def finite_lease_pv_approx_2(T, g, r, x_0):
   return (x_0 * (T + 1))

# Infinite lease
def infinite_lease(g, r, x_0):
   G = (1 + g)
   R = (1 + r)
   return x_0 / (1 - G * R**(-1))

def plot_function(axes, x_vals, func, args):
   axes.plot(x_vals, func(*args), label=func.__name__)
T_max = 50
T = np.arange(0, T_max+1)
g = 0.02
r = 0.03
x_0 = 1
our_args = (T, g, r, x_0)
funcs = [finite_lease_pv_true,
finite_lease_pv_approx_1,
finite_lease_pv_approx_2]
## the three functions we want to compare
fig, ax = plt.subplots()
ax.set_title('Finite Lease Present Value $T$ Periods Ahead')
for f in funcs:
   plot_function(ax, T, f, our_args)
ax.legend()
ax.set_xlabel('$T$ Periods Ahead')
ax.set_ylabel('Present Value, $p_0$')
plt.show()


# Convergence of infinite and finite
T_max = 1000
T = np.arange(0, T_max+1)
fig, ax = plt.subplots()
ax.set_title('Infinite and Finite Lease Present Value $T$ Periods Ahead')

f_1 = finite_lease_pv_true(T, g, r, x_0)
f_2 = np.full(T_max+1, infinite_lease(g, r, x_0))
ax.plot(T, f_1, label='T-period lease PV')
ax.plot(T, f_2, '--', label='Infinite lease PV')
ax.set_xlabel('$T$ Periods Ahead')
ax.set_ylabel('Present Value, $p_0$')
ax.legend()
plt.show()

    