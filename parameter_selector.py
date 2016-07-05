#!/usr/env python

import cv2
import numpy as np
import os
import math
import random
import time
from matplotlib import pyplot as plt
from collections import deque

PENALTY_WHITE = 7
PENALTY_BLACK = 1
MAX_IT = 100
MAX_ITER_LS = 6
LOWER_P1 = 8
LOWER_P2 = 30
LOWER_MIN_DIST = 100


# circle: list with a circle's parameters (x,y,radius)
def count_pixels(img, circle):
  x = circle[1]
  y = circle[0]
  r = circle[2]
  xs = x-r
  xe = x+r+1
  ys = y-r
  ye = y+r+1

  img_box = np.array(img[xs:xe,ys:ye])
  h = img_box.shape[0]
  w = img_box.shape[1]

  black = 0
  white = 0
  for i in range(h):
      for j in range(w):
          if(img_box[i,j] == 0):
              black+= 1
          else:
            white+= 1

  percent_black = (100*black)/total_pixels
  percent_white = (100*white)/total_pixels


  return perecent_black, percent_white


def select_circle(img,circles):
  best_circle = circles[0]
  best_percent_black = count_pixels(img,best_circle)
  for c in circles:
    black, white = count_pixels(img,c)
    if(black > best_percent_black):
      best_circle = c

  return best_circle


def calc_cost(black, white):  
  return WEIGHT_BLACK*black + WEIGHT_WHITE*white


def local_search(sol,cost,min_rad,max_rad):

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

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, cur_sol[0], cur_sol[1], param1=cur_sol[2], param2=cur_sol[3], minRadius=min_rad, maxRadius=max_rad)
    c = select_circles(circles)
    p_black, p_white = count_pixels(img,c)
    cur_cost = calc_cost(p_black,p_white)

    if(cur_cost <= best_cost):
      improved = True
      best_cost = cur_cost
      best_sol = cur_sol.copy()
    elif(improved == True):
      break
      


  return best_sol


def ils(img,min_rad,max_rad):
  cur_sol = [2,100,20,100]
  best_sol = cur_sol.copy()
  circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, sol[0], sol[1], param1=sol[2], param2=sol[3], minRadius=min_rad, maxRadius=max_rad)
  c = select_circle(img,circles)
  p_black, p_white = count_pixels(img,c)
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
    cur_sol = local_search(cur_sol,cur_cost,min_rad,max_rad)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, cur_sol[0], cur_sol[1], param1=cur_sol[2], param2=cur_sol[3], minRadius=min_rad, maxRadius=max_rad)
    c = select_circles(img,circles)
    p_black, p_white = count_pixels(img,c)
    cur_cost = calc_cost(p_black,p_white)

    # Acceptance
    if(cur_cost < best_cost):
      best_cost = cur_cost
      best_sol = cur_sol.copy()

  return best_sol



