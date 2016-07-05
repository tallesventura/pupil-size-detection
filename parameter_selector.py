import cv2
import numpy as np
import math
import random
from collections import deque
import circles_utils

# Penalty for the percentage of white pixels on the goal function
PENALTY_WHITE = 5
# Penalty for the percentage of black pixels on the goal function
PENALTY_BLACK = 1
# Number of iterations for the iterated local search (ils)
MAX_IT = 100
# Number of iterations for the local search
MAX_ITER_LS = 6
# Minimum value for the param1 of the cv2.HoughCircles function
LOWER_P1 = 8
# Minimum value for the param2 of the cv2.HoughCircles function
LOWER_P2 = 30
# Minimum value for the minimum distance between the centers of circles in the cv2.HoughCircles function
LOWER_MIN_DIST = 100


# black: percentage of black pixels
# white: percentage of white pixels
def calc_cost(black, white):
  return PENALTY_BLACK*black + PENALTY_WHITE*white


# img_bin: image with a threshold applied
# sol: initial solution
# cost: initial cost
# min_rad: minimum radius
# max_rad: maximum radius
def local_search(img_gray_scale,img_bin,sol,cost,min_rad,max_rad):

  cur_sol = sol.copy()
  cur_cost = cost
  best_sol = sol.copy()
  best_cost = cost
  improved = False

  ratio = random.random() + 0.1
  inc_dec = random.randint(0,1)
  pos = random.randint(0,3)

  for i in range(1,MAX_ITER_LS+1):
    n = cur_sol[pos]
    if(inc_dec == 0):     
      if(pos == 0):
        cur_sol[pos] =  max(int(n - (n*ratio)/i),1)
      elif(pos == 1):
        cur_sol[pos] =  max(int(n - (n*ratio)/i),LOWER_MIN_DIST-1)
      elif(pos == 2):
        cur_sol[pos] =  max(int(n - (n*ratio)/i),LOWER_P1-1)
      elif(pos == 3):
        cur_sol[pos] =  max(int(n - (n*ratio)/i),LOWER_P2-1)
    else:
      cur_sol[pos] = int(n + (n*ratio)/i)

    circles = cv2.HoughCircles(img_gray_scale, cv2.HOUGH_GRADIENT, cur_sol[0], cur_sol[1], param1=cur_sol[2], param2=cur_sol[3], minRadius=min_rad, maxRadius=max_rad)
    if(circles is None):
    	continue
    circles = np.int16(np.around(circles))
    c = circles_utils.select_circle(img_bin,circles[0])
    p_black, p_white = circles_utils.count_pixels(img_bin,c)
    cur_cost = calc_cost(p_black,p_white)

    if(cur_cost <= best_cost):
      improved = True
      best_cost = cur_cost
      best_sol = cur_sol.copy()
    elif(improved == True):
      break
      

  return best_sol


# img_bin: image with a threshold applied
# sol: initial solution
# min_rad: minimum radius
# max_rad: maximum radius
def ils(img_gray_scale,img_bin,sol,min_rad,max_rad):
  cur_sol = sol.copy()
  best_sol = cur_sol.copy()
  circles = cv2.HoughCircles(img_gray_scale, cv2.HOUGH_GRADIENT, cur_sol[0], cur_sol[1], param1=cur_sol[2], param2=cur_sol[3], minRadius=min_rad, maxRadius=max_rad)
  circles = np.int16(np.around(circles))

  c = circles_utils.select_circle(img_bin,circles[0])
  p_black, p_white = circles_utils.count_pixels(img_bin,c)
  cur_cost = calc_cost(p_black,p_white)
  best_cost = cur_cost
  pos = random.randint(0,3)
  hist_pos = deque([pos])

  for i in range(MAX_IT):
    print("Iteration ", i)
    inc_dec = random.randint(0,1)
    ratio = random.randrange(1,6)/10

    while(hist_pos.count(pos) > 0):
      pos = random.randint(0,3)

    hist_pos.append(pos)
    if(len(hist_pos) > 0):
      hist_pos.popleft()

    cur_sol = best_sol.copy()
    n = cur_sol[pos]
    if(inc_dec == 1):
      cur_sol[pos] += int(n*ratio)
    else:
      if(pos == 0):
        cur_sol[pos] =  max(int(n - (n*ratio)),1)
      elif(pos == 1):
        cur_sol[pos] =  max(int(n - (n*ratio)),LOWER_MIN_DIST-1)
      elif(pos == 2):
        cur_sol[pos] =  max(int(n - (n*ratio)),LOWER_P1-1)
      elif(pos == 3):
        cur_sol[pos] =  max(int(n - (n*ratio)),LOWER_P2-1)
    #--------------------------------------------------------------------------------

    # Local search
    cur_sol = local_search(img_gray_scale,img_bin,cur_sol,cur_cost,min_rad,max_rad)

    circles = cv2.HoughCircles(img_gray_scale, cv2.HOUGH_GRADIENT, cur_sol[0], cur_sol[1], param1=cur_sol[2], param2=cur_sol[3], minRadius=min_rad, maxRadius=max_rad)
    if(circles is None):
    	continue
    circles = np.int16(np.around(circles))
    c = circles_utils.select_circle(img_bin,circles[0])
    p_black, p_white = circles_utils.count_pixels(img_bin,c)
    print(p_black)
    cur_cost = calc_cost(p_black,p_white)

    # Acceptance
    if(cur_cost <= best_cost):
      best_cost = cur_cost
      best_sol = cur_sol.copy()

  print("best sol: ",best_sol)
  return best_sol



