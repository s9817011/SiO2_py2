import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import CheckButtons
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
sys.path.append(r"D:\SiO2_test")
from utility_f import data_open, Plot
folder_path = r"D:\SiO2 51_test"
#設定畫布視窗以及主圖大小
fig , (ax,ax2) = plt.subplots(1,2, figsize=(18,8))
# 初始化 Plot 類別物件
myplot = Plot()
# 讀取資料
data_list = data_open(folder_path)
last_data_list = data_list
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
def update(data_list,folder_path):
    global myplot, ax, ax2, last_data_list, check, myplot
    # 保存勾選框的狀態
    visible_before = myplot.visible.copy()
    # 取得最新的資料
    new_data_list = data_open(folder_path)
    new_data_list.sort(key=lambda x: x[0])
    print(f'visible_before',len(visible_before))
    if last_data_list != new_data_list:
        print("正在迴圈中")
        for line in ax.lines:
            line.remove()
        myplot.lines.clear()
        for line in ax2.lines:
            line.remove()
        print(f'myplot.lines',myplot.lines)

        ch_labels = [f"{temperature} K" for temperature, _, _ in new_data_list]
        print(f"ch_labels",ch_labels)
        
        ax.cla()
        ax2.cla()
        # 繪製 ID-VG 資料圖
        myplot.idvg_data(ax, new_data_list)
        # 繪製 ID-VG 對數尺度圖
        myplot.idvg_data_log(ax2, new_data_list)
        print(f'myplot.lines',myplot.lines)
        print(f'清除後的myplot.lines',len(myplot.lines))
        # 獲取 new_lines，用於檢查 visible 狀態
        new_lines = myplot.lines[len(last_data_list):]
        print(f'new_lines',new_lines)
        for i, line in enumerate(new_lines):
            line.set_visible(True)
        print(f'迴圈中news_lines',len(new_lines))
        visible_dict = {label: vis for label, vis in zip(ch_labels, visible_before)}
        print(f'visible_dict',visible_dict)
        visible_dict.update({label: True for label in ch_labels[len(last_data_list):]})
        print(f'visible_dict_update',visible_dict)
        # 與可視狀態列表同步
        myplot.visible = [visible_dict[label] for label in myplot.labels]
        print(f'myplot.visible',myplot.visible)
        # # 恢復勾選框狀態
        # myplot.visible = visible_before
        # print(f'myplot.visible = ',myplot.visible)
        # for i, line in enumerate(myplot.lines):
        #     print(f'myplot.lines',len(myplot.lines))
        #     line.set_visible(myplot.visible[i])
        # 檢查 myplot.lines 屬性是否包含所有的線條
        # print(f"Lines in myplot: {[line.get_label() for line in myplot.lines]}")
        # 畫圖
        plt.draw()
        # 更新上次读取的数据为当前的数据
        # 設定需要顯示的標籤
           # 設定需要顯示的標籤
        new_data_list.sort(key=lambda x: x[0])
        ch_labels = [f"{temperature} K" for temperature, _, _ in new_data_list]
        # 將標籤更新到 myplot 中
        myplot.labels = ch_labels
        # 更新勾選框
        check_labels = check.labels
        # 如果勾選框中的標籤和當前需要顯示的標籤不一致，就需要重新設置勾選框
        if check_labels != ch_labels:
            # 移除現有的勾選框
            check.disconnect_events()
            # 建立新的勾選框
            rax = plt.axes([-0.01, 0.4, 0.1, 0.2])
            check = CheckButtons(rax, ch_labels, myplot.visible)
            # 將之前勾選的項重新勾選上
            for i, label in enumerate(ch_labels):
                if label in check_labels and myplot.visible[i]:
                    check.set_active(i)
            check.on_clicked(on_check_clicked)
            # check = check
            # check.on_clicked(on_check_clicked)
            last_data_list = new_data_list
            data_list = new_data_list
    else:
        print('pass')
        pass
# 設定重繪的間隔時間為12秒
ani = FuncAnimation(fig, update, fargs=[folder_path], interval=3*1000)
# 設定需要顯示的標籤
last_data_list.sort(key=lambda x: x[0])
ch_labels = [f"{temperature} K" for temperature, _, _ in last_data_list]
# 設定勾選框的位置和大小
rax = plt.axes([-0.01, 0.4, 0.1, 0.2])
# 建立勾選框
check = CheckButtons(rax, ch_labels, myplot.visible)
def on_check_clicked(label):
    # 在 on_check_clicked 函数内定义一个内部函数，来更新勾选框的状态
    def update_checkboxes():
        global check, myplot
        # 移除现有的勾选框
        check.disconnect_events()
        # 建立新的勾选框
        rax = plt.axes([-0.01, 0.4, 0.1, 0.2])
        # 設定需要顯示的標籤
        last_data_list.sort(key=lambda x: x[0])
        ch_labels = [f"{temperature} K" for temperature, _, _ in last_data_list]
        check = CheckButtons(rax, ch_labels, myplot.visible)
        # 將之前勾選的項重新勾選上
        for i, label in enumerate(ch_labels):
            if label in ch_labels and myplot.visible[i]:
                check.set_active(i)
        check.on_clicked(on_check_clicked)
        # for i, label in enumerate(myplot.labels):
        #     if myplot.visible[i]:
        #         check.rectangles[i].set(facecolor=myplot.line_colors[i])
        #         check.lines[i][0].set_color(myplot.line_colors[i])
        #     else:
        #         check.rectangles[i].set(facecolor='#FFFFFF')
        #         check.lines[i][0].set_color('#000000')
        # 将之前勾选的项重新勾选上
        # for i, label in enumerate(ch_labels):
        #     if myplot.visible[i]:
        #         ud_check.set_active(i)
        # 重新连接勾选框的点击事件
        # 設定需要顯示的標籤
        last_data_list.sort(key=lambda x: x[0])
        ch_labels = [f"{temperature} K" for temperature, _, _ in last_data_list]
        check = CheckButtons(rax, ch_labels, myplot.visible)
        check.on_clicked(on_check_clicked)
        # 畫圖
        plt.draw()
    print('按鈕的myplot.labels',myplot.labels)
    index = myplot.labels.index(label)
    myplot.toggle_visibility(label)
    update(last_data_list, folder_path)
    update_checkboxes()
    plt.draw()


check.on_clicked(on_check_clicked)
plt.show()