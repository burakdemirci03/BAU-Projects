from random import random

red = 20
blue = 20
green = 20

def red_func(red):
  red_trans = 0
  blue_trans = 0
  for each in range(red):
    r = random()
    if (r >= 0.4):
      red_trans -= 1
      blue_trans += 1
  return [red_trans, blue_trans]

def blue_func(blue):
  red_trans = 0
  blue_trans = 0
  green_trans = 0
  for each in range(blue):
    r = random()
    if (r <= 0.3):
      red_trans += 1
      blue_trans -= 1
    if (r >= 0.6):
      blue_trans -= 1
      green_trans += 1
  return [red_trans, blue_trans, green_trans]    

def green_func(green):
  blue_trans = 0
  green_trans = 0
  for each in range(green):
    r = random()
    if (r <= 0.5):
      blue_trans += 1
      green_trans -= 1
  return [blue_trans, green_trans]    

def box_func(red, blue, green):
  red_list = red_func(red)
  blue_list = blue_func(blue)
  green_list = green_func(green)
  r_red_decrease = red_list[0]
  r_blue_increase = red_list[1]
  b_red_increase = blue_list[0]
  b_blue_decrease = blue_list[1]
  b_green_increase = blue_list[2]
  g_blue_increase = green_list[0]
  g_green_decrease = green_list[1]
  red += r_red_decrease + b_red_increase
  blue += r_blue_increase + b_blue_decrease + g_blue_increase
  green += b_green_increase + g_green_decrease
  return [red, blue, green]

with open("simulation.csv", "w") as sim:
  sim.write(f"{'Time':>3},{'Red':>8},{'Blue':>8},{'Green':>8},\n")
  for t in range(101):
    ball_num = box_func(red,blue,green)
    red_box = ball_num[0]
    blue_box = ball_num[1]
    green_box = ball_num[2]
    message = (f"{t:>4},{red_box:>8},{blue_box:>8},{green_box:>8},\n")
    sim.write(message)