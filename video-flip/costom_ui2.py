# cd to python/Scripts
# pyuic5 -x ../../video-flip/ui.ui -o ../../video-flip/ui.py
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_MainWindow
from patch import run_async
import sys, os, datetime, time, ffmpeg, mock




class MyMainWindow(Ui_MainWindow, QtWidgets.QMainWindow):
    trigger = QtCore.pyqtSignal(bool)
    timer= QtCore.pyqtSignal(str)
    
    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)
        _translate = QtCore.QCoreApplication.translate
        # 以main.exe開啟影片時，自動設定路徑
        if os.path.basename(__file__) not in sys.argv[-1]:
            self.filePath.setText(sys.argv[-1])
        # 重新設定圖示路徑
        self.labelRight.setPixmap(QtGui.QPixmap("static/images/right.png"))
        self.labelLeft.setPixmap(QtGui.QPixmap("static/images/left.png"))
        # 瀏覽按鈕按下
        self.searchFile.clicked.connect(self.onenSearchDialog)
        # 開始按鈕按下
        self.confirm.clicked.connect(self.startFlip)
        # 設定thread
        self.threadpool = QtCore.QThreadPool()
        # 設定thread跑完後，要發訊號並連接到endFlip
        self.trigger.connect(self.flipMode)
        # 設定timer
        self.startTime= datetime.datetime.now()
        self.timer.connect(self.labelTimer.setText)
        self.running= False
    
    # 瀏覽按鈕
    def onenSearchDialog(self):
        fileName, _= QtWidgets.QFileDialog.getOpenFileName()
        self.filePath.setText(fileName)
    
    # 開始按鈕
    def startFlip(self):
        filePath= self.filePath.text()
        # 先確認檔案是否存在
        if not os.path.exists(filePath):
            self.showMsg("檔案不存在", icon="critical")
            return
        
        # ui change
        self.trigger.emit(True)
        
        # video thread
        def videoFlip():
             # 設定輸出影片，輸出的影片名稱為xxx-flip.mp4
            videoNames= os.path.basename(filePath)
            newVideoNames= videoNames.split('.')[0]+ "-flip."+ videoNames.split('.')[-1]
            outputPath= filePath.replace(videoNames,newVideoNames)
            # 設定ffmpeg的路徑(環境變數)
            os.environ['PATH'] += ';'+os.path.abspath(os.path.dirname(__file__)+'/static/ffmpeg/')
            # 向右:順時針(clockwise), 向左:逆時針(counter clockwise)
            if self.radioLeft.isChecked():
                # transpose=1:順時針90度，transpose=2:逆時針90度，transpose=1,transpose=1:180度
                transpose=2
            elif self.radioRight.isChecked():
                transpose=1
            # 如果已經有檔案，則先刪除之間翻轉的結果
            os.remove(outputPath) if os.path.exists(outputPath) else None
            # 打補釘，以避免run()會開啟另一個視窗
            with mock.patch("ffmpeg.run_async", run_async):
                ffmpeg.input(filePath).output(outputPath, vf=f'transpose={transpose}', loglevel="quiet").run()
            
            # 轉換結束時發送訊號給trigger
            self.trigger.emit(False)
            # 停止timer
            self.running= False
        # 開始thread
        self.threadpool.start(videoFlip)
        
        # timer
        def setTimer():
            while self.running:
                delta= (datetime.datetime.now()- self.startTime).seconds
                self.timer.emit(f"開始時間 :  {delta//60 : >3d}:{delta%60 :0>2d}\t")
                time.sleep(1)
        # 重設計時器
        self.startTime= datetime.datetime.now()
        # 開始計時
        self.running= True
        self.threadpool.start(setTimer)
    
    # 更改介面狀態
    def flipMode(self, status:bool):
        if status:
            self.confirm.setText("轉換中")
        else:
            self.showMsg("完成", icon="information")
            self.confirm.setText("開始")
        self.confirm.setDisabled(status)
        self.filePath.setDisabled(status)
        self.searchFile.setDisabled(status)
        self.radioLeft.setDisabled(status)
        self.radioRight.setDisabled(status)
    
    # 訊息跳窗
    def showMsg(self, msg:str, icon:str=""):
        msgBox= QtWidgets.QMessageBox()
        msgBox.setWindowTitle("訊息")
        msgBox.setText(msg)
        if icon:
            if icon == "information":
                msgBox.setIcon(QtWidgets.QMessageBox.Information)
            elif icon == "critical":
                msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            elif icon == "warning":
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            elif icon == "question":
                msgBox.setIcon(QtWidgets.QMessageBox.Question)
        x= msgBox.exec_()




if __name__ == "__main__":
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())