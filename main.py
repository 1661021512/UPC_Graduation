import cv2
import sys
import os
import time
import platform
import  PySide6

dirname = os.path.dirname(PySide6.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
import myframe
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%
import datetime
import csv


# 定义变量




def saveData(fpath,fdata):
    with open(fpath,"a+",encoding="utf8",newline='') as csvfile:
        w = csv.writer(csvfile)
        w.writerow(fdata)



# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

def CamConfig_init():
    window.f_type = CamConfig()


ActionCOUNTER=0



class CamConfig:
    def __init__(self):
        # 设置时钟
        self.v_timer = QTimer()
        # 打开摄像头
        self.cap = cv2.VideoCapture(0)
        if not self.cap:
           pass
        # 设置定时器周期，单位毫秒
        self.v_timer.start(20)
        # 连接定时器周期溢出的槽函数，用于显示一帧视频
        self.v_timer.timeout.connect(self.show_pic)
        # 在前端UI输出提示信息
    def show_pic(self):
        success, frame = self.cap.read()
        # print(success)
        if success:
            conf= float(window.ui.horizontalSlider.value())/100
            ret,frame,fps= myframe.frametest(frame,conf=conf)
            lab = ret[0]
            global ActionCOUNTER
            ActionCOUNTER += 1
            # show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            show = frame
            window.ui.label_4.setText('FPS:'+fps)

            for i in lab:
                if(i == "Chair" and ActionCOUNTER == 7):
                    window.ui.textBrowser.append("<font color=white>检测到椅子</font>")
                    flag=1
                elif(i == "People" and ActionCOUNTER == 7):
                    window.ui.textBrowser.append("<font color=white>检测到人员</font>")
                    flag=1
                elif(i == "Bottle" and ActionCOUNTER == 7):
                    window.ui.textBrowser.append("<font color=white>检测到瓶子</font>")
                    flag=1
                elif(i == "Cup" and ActionCOUNTER == 7):
                    window.ui.textBrowser.append("<font color=white>检测到杯子</font>")
                    flag=1
                elif(i == "Table" and ActionCOUNTER == 7):
                    window.ui.textBrowser.append("<font color=white>检测到杯子</font>")
                    flag=1
                elif(i == "Boat" and ActionCOUNTER == 7):
                    window.ui.textBrowser.append("<font color=white>检测到船只</font>")
                    flag=1
            if(ActionCOUNTER==7):
                ActionCOUNTER=0
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_BGR888)
            pixmap = QPixmap(showImage).scaled(window.ui.label.size(), aspectMode=Qt.KeepAspectRatio)
            window.ui.label.setPixmap(pixmap)



            


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        self.f_type = 0

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX 自定义标题栏
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME 应用程序名
        # ///////////////////////////////////////////////////////////////
        title = "实时演示系统"
        description = "基于YOLO v8的实时目标检测系统 "
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU 菜单栏展开
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self) 

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        

        #CamreButton
        widgets.CamreButton.clicked.connect(self.buttonClick)

        #FileButton
        widgets.pushButton.clicked.connect(self.buttonClick)
        widgets.horizontalSlider.setValue(70)


        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
    





    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "btn_save":
            widgets.stackedWidget.setCurrentWidget(widgets.page)


            file_dir = './logs/pictures'  #你的文件路径
            for i,j,k in os.walk(file_dir):
                files=k

            show = cv2.imread(file_dir+"/"+str(files[0]))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap(showImage).scaled(window.ui.label_9.size(), aspectMode=Qt.KeepAspectRatio)
            window.ui.label_9.setPixmap(pixmap)


            show = cv2.imread(file_dir+"/"+str(files[1]))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap(showImage).scaled(window.ui.label_10.size(), aspectMode=Qt.KeepAspectRatio)
            window.ui.label_10.setPixmap(pixmap)


            show = cv2.imread(file_dir+"/"+str(files[2]))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap(showImage).scaled(window.ui.label_11.size(), aspectMode=Qt.KeepAspectRatio)
            window.ui.label_11.setPixmap(pixmap)


            show = cv2.imread(file_dir+"/"+str(files[3]))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap(showImage).scaled(window.ui.label_12.size(), aspectMode=Qt.KeepAspectRatio)
            window.ui.label_12.setPixmap(pixmap)

            show = cv2.imread(file_dir+"/"+str(files[4]))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap(showImage).scaled(window.ui.label_13.size(), aspectMode=Qt.KeepAspectRatio)
            window.ui.label_13.setPixmap(pixmap)

            show = cv2.imread(file_dir+"/"+str(files[5]))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap(showImage).scaled(window.ui.label_14.size(), aspectMode=Qt.KeepAspectRatio)
            window.ui.label_14.setPixmap(pixmap)


            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        
        if btnName == "CamreButton":
            print("Camre BTN clicked!")
            CamConfig_init()


        if btnName == "pushButton":
            fname,ftype = QFileDialog.getOpenFileName(self, "Open File", "./logs", "csv (*.csv)")#如果添加一个内容则需要加两个分号
            # 该方法返回一个tuple,里面有两个内容，第一个是路径， 第二个是要打开文件的类型，所以用两个变量去接受
            # 如果用户主动关闭文件对话框，则返回值为空
            if fname[0]:# 判断路径非空
                with open(fname,"r",encoding="utf8") as csvreader:  
                    tmp = csv.reader(csvreader)
                    i=0
                    list_data=[]
                    for row in tmp:
                        list_data.append(row)
                    for row in range(len(list_data)):
                        for column in range(len(list_data[row])):
                            widgets.tableWidget.setItem(row,column,QTableWidgetItem(list_data[row][column]))
                        i+=1
                        if i==15:break



        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()
        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())