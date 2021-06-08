from math import cos, sin, pi, fabs, atan
import matplotlib.pyplot as plt
import numpy as np
import pygame

width = 650
height = 650

g_l = 9.8
M = 200000
a_max = 29.43
m = 5000
M += m
v_0 = int(input("введите скорость истечения газа "))
delta_m = int(input("введите скорость сжигания топлива "))
alpha = int(input("введите начальный угол "))
alpha = alpha * pi / 180

H = 0
S = 0
v_y = v_0 * sin(alpha)
v_x = v_0 * cos(alpha)
time = 0.1

x_k = []
y_k = []
times = []
angle_of_lean = []

def autopilot_weight_change(angle, delta_m, time):
    a_y = fabs(-g_l - delta_m *v_0* fabs(sin(angle)) / M)
    a_x = fabs(-delta_m *v_0* fabs(cos(angle)) / M)
    v_y_new = a_y * time + v_y
    v_x_new = a_x * time + v_x
    H_new = H + v_y_new * time + a_y * pow(time, 2) / 2
    S_new = S + v_x_new * time + a_x * pow(time, 2) / 2
    return v_y_new, v_x_new, H_new, S_new

def autopilot_weight_const(angle, delta_m, time, v_x_new):
    a_y = fabs(-g_l - delta_m *v_0* fabs(sin(angle)) / M)
    v_y_new = -a_y * time + v_y
    H_new = H + v_y_new * time - a_y * pow(time, 2) / 2
    S_new = S + time * v_x_new 
    return v_y_new, v_x_new, H_new, S_new

x_k.append(S)
y_k.append(H)
cur_time = 0
times.append(cur_time)
angle_of_lean.append(alpha * 180 / pi) 

while m > 0:
   if delta_m * time > m:
       break
   m -= delta_m * time
   cur_time += time
   H_prev = H
   S_prev = S
   v_y, v_x, H, S = autopilot_weight_change(alpha, delta_m, time)
   alpha = atan((H - H_prev) / (S - S_prev))
   print(f"V_x = {v_x} V_y = {v_y} V = {(v_x * v_x + v_y * v_y)**0.5} угол положения двигателя {alpha * 180 / pi} топлива {m}, время полета {cur_time} S = {S} H = {H}")
   x_k.append(S)
   y_k.append(H)
   times.append(cur_time)
   angle_of_lean.append(alpha* 180 / pi)

while H > 0:
     cur_time += time
     H_prev = H
     S_prev = S
     v_y, v_x, H, S = autopilot_weight_const(alpha, delta_m, time, v_x)
     alpha = atan((H - H_prev) / (S - S_prev))
     print(f"V_x = {v_x} V_y = {v_y} V = {(v_x * v_x + v_y * v_y)**0.5}  угол положения двигателя {alpha * 180 / pi} топлива {m}, время полета {cur_time} S = {S} H = {H}")
     x_k.append(S)
     y_k.append(H)
     times.append(cur_time)
     angle_of_lean.append(alpha * 180 / pi)

print(f"V_x = {v_x} V_y = {v_y} V = {(v_x * v_x + v_y * v_y)**0.5}  угол положения двигателя {alpha * 180 / pi} топлива {m}, время полета {cur_time} S = {S} H = {H}")
print(f"оставшееся топливо: {m}")


plt.grid()
plt.plot(times, y_k)
pygame.init()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rocket")
rocket = [pygame.image.load("rocket0.png"),
          pygame.image.load("rocket1.png"),
          pygame.image.load("rocket2.png"),
          pygame.image.load("rocket3.png"),
          pygame.image.load("rocket4.png")]
bg = pygame.image.load("bg.png")

normalized_step = 250000 / width
meters_per_pixel = 100000 / height

for i in range(len(x_k)):
    pygame.time.delay(10)
    rotated_image = pygame.transform.rotate(rocket[i % 5], angle_of_lean[i])
    win.fill((0, 0, 0))
    win.blit(bg, (0, 0))
    win.blit(rotated_image, (int(x_k[i] / normalized_step) + 10, height - int(fabs(y_k[i]) / meters_per_pixel + 100)))
    pygame.display.update()

plt.show()
