import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import CheckButtons
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
sys.path.append(r"D:\SiO2_test")
from utility_f import data_open, Plot#, CheckButtonsWithMemory
folder_path = r"D:\SiO2 51_test"
#設定畫布視窗以及主圖大小
fig , (ax,ax2) = plt.subplots(1,2, figsize=(18,8))
# 初始化 Plot 類別物件
myplot = Plot()
# 讀取資料
data_list = data_open(folder_path)
# 清空圖表
ax.cla()  
ax2.cla()
# 繪製 ID-VG 資料圖
myplot.idvg_data(ax, data_list)
# 繪製 ID-VG 對數尺度圖
myplot.idvg_data_log(ax2, data_list)
# 畫圖
plt.draw()
plt.pause(0.001)
def update(frame):
    global myplot, ax, ax2, data_list
    # 取得最新的資料
    new_data_list = data_open(folder_path)
    #print(f"New data list: {new_data_list}")
    # 清空圖表
    ax.cla()
    ax2.cla()
    # 保存勾選框的狀態
    visible_before = myplot.visible.copy()
    # 繪製新的圖表
    # 檢查是否與原本的資料不同
    # 如果有變化，就更新資料並畫圖
    data_list = new_data_list
    print(f"Data list updated: {data_list}")
    # 清空圖表
    ax.cla()
    ax2.cla()
    # 繪製 ID-VG 資料圖
    myplot.idvg_data(ax, data_list)
    # 繪製 ID-VG 對數尺度圖
    myplot.idvg_data_log(ax2, data_list)
    # 恢復勾選框狀態
    myplot.visible_before()
    # 檢查 myplot.lines 屬性是否包含所有的線條
    print(f"Lines in myplot: {[line.get_label() for line in myplot.lines]}")
    # 畫圖
    plt.draw()
# 設定重繪的間隔時間為12秒
ani = FuncAnimation(fig, update, interval=3*1000)
# 設定需要顯示的標籤
labels = [f"{temperature} K" for temperature, _, _ in data_list]
# 設定勾選框的位置和大小
rax = plt.axes([0.05, 0.4, 0.1, 0.2])
# 建立勾選框
check = CheckButtons(rax, labels, [True] * len(data_list))
# 設定勾選框的點擊事件
def on_check_clicked(label):
    index = myplot.labels.index(label)
    myplot.toggle_visibility(label)
    plt.draw()
# 設定當勾選框被點選時，更新顯示的線條
check.on_clicked(on_check_clicked)
plt.show()