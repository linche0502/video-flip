# cd to python/Scripts
# pyuic5 -x ../../video-flip/ui.ui -o ../../video-flip/ui.py
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_MainWindow
import os, cv2, datetime, time, ffmpeg




class MyMainWindow(Ui_MainWindow, QtWidgets.QMainWindow):
    trigger = QtCore.pyqtSignal(bool)
    timer= QtCore.pyqtSignal(str)
    
    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)
        _translate = QtCore.QCoreApplication.translate
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
        
        # 讀取影片檔
        try:
            capture = cv2.VideoCapture(filePath)
            # 獲取影片長.寬.FPS
            if capture.isOpened(): 
                width  = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))   # float `width`
                height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
                frameRate= capture.get(cv2.CAP_PROP_FPS)
        except:
            self.showMsg("讀取影片失敗", icon="critical")
            return
        
        # ui change
        self.trigger.emit(True)
        
        # video thread
        def videoFlip():
             # 設定輸出影片
            videoNames= os.path.basename(filePath)
            newVideoNames= videoNames.split('.')[0]+ "-flip-temp."+ videoNames.split('.')[-1]
            newVideoPath= filePath.replace(videoNames,newVideoNames)
            fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
            outputVideo = cv2.VideoWriter(newVideoPath, fourcc, frameRate, (height,width))
            # ret: 是否擷取成功，frame: 擷取下來的一幀影像
            ret = True
            # 向右:順時針(clockwise), 向左:逆時針(counter clockwise)
            if self.radioLeft.isChecked():
                while ret:
                    ret, frame = capture.read() # read one frame from the 'capture' object; img is (H, W, C)
                    outputVideo.write(cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE))
            elif self.radioRight.isChecked():
                while ret:
                    ret, frame = capture.read() # read one frame from the 'capture' object; img is (H, W, C)
                    outputVideo.write(cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE))
            # 關閉outputVideo，以便後續ffmpeg可以正常開啟
            outputVideo.release()
            # 設定ffmpeg的路徑(環境變數)
            os.environ['PATH'] += ';'+os.path.abspath(os.path.dirname(__file__)+'/static/ffmpeg/')
            # 用ffmpeg加入聲音檔案
            input_video = ffmpeg.input(newVideoPath)
            input_audio = ffmpeg.input(filePath)
            newVideoPathsAudio= newVideoPath.replace("-flip-temp.","-flip.")
            os.remove(newVideoPathsAudio) if os.path.exists(newVideoPathsAudio) else None
            ffmpeg.concat(input_video, input_audio, v=1, a=1).output(newVideoPathsAudio).run(overwrite_output=True)
            os.remove(newVideoPath)
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
    import sys, os
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())