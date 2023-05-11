'''
===================utility_f===================
此程式是撰寫讀檔、idvg還有idvg的log圖的函數，主程式
請到
===============================================
'''
import re
import os
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
import json
#取資料及設定圖例
def data_open(folder_path):
    data_list = []
    files = os.listdir(folder_path)
    for file_name in files:
    # 判斷檔案名稱是否包含IdVd
        if "IdVg" in file_name and file_name.endswith(".dat") and "LeakingCurrent" not in file_name:
            # 如果符合條件，讀取檔案內容
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r") as f:
                data = f.readlines()
            # 解析檔案中的數據
            x = []
            y = []
            for line in data:
                line = line.strip().split()
                x.append(float(line[0]))
                y.append(float(line[1]))
            # 將file_path中只保留=和k之間
            match = re.search(r"T=(\d+)k", file_name)
            if match:
                num = match.group()
                # 用提取到的數字來替換原本的文件名
                temperature = int(match.group(1)) if match else "Unknown temperature"
                data_list.append((temperature, x, y))
    # 按照溫度排序，x[0]前面加"-"會變成由大到小
    data_list.sort(key=lambda x: x[0])
    return data_list
class Plot:     
    def __init__(self):
        self.visible = []
        self.lines = []
        self.labels = []
        self.label_state = {}  # 保存標籤勾選狀態
    def idvg_data(self, ax, data_list):
        self.visible = [True] * len(data_list)
        for i, data in enumerate(data_list):
            temperature, x, y = data
            state = self.label_state.get(f"{temperature} K", True)  # 檢查標籤勾選狀態
            line, = ax.plot(x, y,label=f"{temperature} K",marker='o', 
                            markersize=2.5, visible=state, picker=5)
            self.lines.append(line)
            self.labels.append(f"{temperature} K")
        # 設定圖表標題和x軸、y軸標籤
        ax.set_title("IdVg data")
        ax.set_xlabel("Vg (V)")
        ax.set_ylabel("Id (A)")
        # 計算 x 和 y 軸數據的範圍
        x_min = min([min(data[1]) for data in data_list])
        x_max = max([max(data[1]) for data in data_list])
        y_min = min([min(data[2]) for data in data_list])
        y_max = max([max(data[2]) for data in data_list])
        # 計算 margin，留白比例
        x_margin = (x_max - x_min) * 0.01 
        y_margin = (y_max - y_min) * 0.01 
        # 設定 x 軸和 y 軸的範圍
        ax.set_xlim(x_min - x_margin, x_max + x_margin)
        ax.set_ylim(y_min - y_margin, y_max + y_margin)
        # 設定 x 軸和 y 軸的刻度密度
        ax.xaxis.set_major_locator(plt.MaxNLocator(11))
        ax.yaxis.set_major_locator(plt.MaxNLocator(11)) 
        # 設定 x 軸和 y 軸的標籤字體大小
        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
        # 設定 x 軸和 y 軸刻度方向
        ax.tick_params(axis='x', direction='in')
        ax.tick_params(axis='y', direction='in')
        # 加入圖例
        #ax.legend(loc='best', bbox_to_anchor=(1.0, 1.05),prop =  {'size':9})
        #對y軸取log
    def idvg_data_log(self, ax2,data_list):
        ax2.set_yscale('log')
        for i, data in enumerate(data_list):
            temperature, x, y = data
            state = self.label_state.get(f"{temperature} K", True)  # 檢查標籤勾選狀態
            line, = ax2.plot(x, y,label=f"{temperature} K",marker='o', 
                             markersize=2.5, visible=state, picker=5)
            self.lines.append(line)
            self.labels.append(f"{temperature} K")
        # 設定圖表標題和x軸、y軸標籤
        ax2.set_title("IdVg log")
        ax2.set_xlabel("Vg (V)")
        ax2.set_ylabel("Id (A)")
        # 計算 x 和 y 軸數據的範圍
        x_min = min([min(data[1]) for data in data_list])
        x_max = max([max(data[1]) for data in data_list])
        y_min = min([min(data[2]) for data in data_list])
        y_max = max([max(data[2]) for data in data_list])
        # 計算 margin，留白比例
        x_margin = (x_max - x_min) * 0.01 
        y_margin = (y_max - y_min) * 0.5 
        # 設定 x 軸和 y 軸的範圍
        ax2.set_xlim(x_min - x_margin, x_max + x_margin)
        ax2.set_ylim(max(y_min - y_margin,1e-13), y_max + y_margin)
        # 設定 x 軸和 y 軸的刻度密度
        ax2.xaxis.set_major_locator(plt.MaxNLocator(11))
        # 設定 x 軸和 y 軸的標籤字體大小
        ax2.tick_params(axis='x', labelsize=10)
        ax2.tick_params(axis='y', labelsize=10)
        # 設定 x 軸和 y 軸刻度方向
        ax2.tick_params(axis='x', direction='in')
        ax2.tick_params(axis='y', direction='in')
        # 加入圖例
        ax2.legend(bbox_to_anchor=(1.18, 1.05),prop =  {'size':10},loc='upper right')
    def update_labels(self, data_list):
        # 更新 self.labels 和 self.visible 列表的大小
        for temperature, _, _ in data_list:
            label = f"{temperature} K"
            if label not in self.labels:
                self.labels.append(label)
                self.visible.append(True)
    def toggle_visibility(self, label):
        if label in self.labels:
            index = self.labels.index(label)
            self.visible[index] = not self.visible[index]
            vis = self.visible[index]
            self.lines[index].set_visible(vis)
            for line in self.lines:
                if line.get_label() == self.labels[index]:
                    line.set_visible(self.visible[index])
            # 将标签的勾选状态保存到字典中
            self.label_state[label] = vis
            plt.draw()
        else:
            print(f"f{label} not found in {self.labels}")
    def toggle_visibility_with_memory(self, label_list):
        for label in label_list:
            # 記憶指定線條的顯示/隱藏狀態，並切換該線條的顯示/隱藏狀態
            index = self.labels.index(label)
            self.visible[index] = not self.visible[index]
            self.lines[index].set_visible(self.visible[index])
        self.update_memory()
