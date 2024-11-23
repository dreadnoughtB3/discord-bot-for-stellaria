import csv
import os

STOCK_F_PATH = "data/stock_f.csv"
STOCK_N_PATH = "data/stock_n.csv"

def check_stock_data():
    if not os.path.exists(STOCK_F_PATH):
        with open(STOCK_F_PATH, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([-7,-6,-5,28,-6,1,-18,-43,-37,-42,-36,0,-21,-15,-36,48,72,78,73,48,75,29,6,41,13])
            writer.writerow([-25,-25,-25,-25,-25,-25,-25,-25,-25,-25,-25,-25,-25,-25,-25,50,50,50,50,50,50,25,0,0,0])
        print("[LOGGER] data/stock_f.csv was created!")

    if not os.path.exists(STOCK_N_PATH):
        with open(STOCK_N_PATH, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([48,-1,1,-49,16,-36,-23,19,-19,1,-21,14,46,98,75,38,-18,39,42,17,47,7,25,-32,25])
            writer.writerow([0,-25,-25,-25,-25,-25,-25,-25,-25,-25,-25,-25,50,50,50,25,0,0,0,-25,-25,-25,-25,-25,-25])
        print("[LOGGER] data/stock_n.csv was created!")