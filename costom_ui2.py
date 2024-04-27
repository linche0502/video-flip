# cd to python/Scripts
# pyuic5 -x "D:\OneDrive\Documents\workspace\python\video-flip\ui.ui" -o "D:\OneDrive\Documents\workspace\python\video-flip\ui.py"
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_MainWindow
import sys, os, datetime, time, ffmpeg




class MyMainWindow(Ui_MainWindow, QtWidgets.QMainWindow):
    # 在thread或subprocess中, 要顯示訊息用的trigger
    msgTrigger= QtCore.pyqtSignal(str, str)
    # 在timer thread中, 要在介面上顯示輸出訊息用的trigger
    timerTrigger= QtCore.pyqtSignal(str)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        _translate = QtCore.QCoreApplication.translate
        
        # 重新設定圖示路徑
        self.labelRight.setPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(__file__, "..", "static", "images", "right.png"))))
        self.labelLeft.setPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(__file__, "..", "static", "images", "left.png"))))
        # 瀏覽按鈕按下
        self.searchFile.clicked.connect(self.onenSearchDialog)
        # 開始按鈕按下
        self.startBtn.clicked.connect(self.run)
        # 設定影片轉換程序
        self.process= QtCore.QProcess(self)
        # 獲取影片轉換程序的stdout, 並開始計時器
        self.process.started.connect(lambda: self.timerThread(True))
        # 結束時關閉計時器
        self.process.finished.connect(lambda: self.timerThread(False))
        # 設定thread
        self.threadpool = QtCore.QThreadPool()
        # 在thread或subprocess中, 要顯示訊息用的trigger
        self.msgTrigger.connect(self.showMsg)
        # 在timer thread中, 要在介面(labelTimer)上顯示輸出訊息用的trigger
        self.timerTrigger.connect(self.labelTimer.setText)
        # 影片幀數
        self.video_frames= 0
    
    # 瀏覽按鈕
    def onenSearchDialog(self):
        fileName, _= QtWidgets.QFileDialog.getOpenFileName()
        self.filePath.setText(fileName)
    
    # 開始按鈕
    def run(self):
        filePath= self.filePath.text()
        # 先確認檔案是否存在
        if not os.path.exists(filePath):
            self.msgTrigger.emit("檔案不存在", "critical")
            return
        
        # 設定輸出影片，輸出的影片名稱為xxx-flip.mp4
        newVideoNames= os.path.splitext(filePath)
        outputPath= newVideoNames[0]+ "-flip"+ newVideoNames[1]
        # 設定ffmpeg的路徑(環境變數)
        os.environ['PATH'] += ';'+ os.path.join(os.path.dirname(__file__),"static","ffmpeg")
        try:
            # 取得影片資訊
            streams= ffmpeg.probe(filePath)
            streams = [stream for stream in streams["streams"] if stream["codec_type"] == "video"]
            self.video_frames= int(streams[0]["nb_frames"])
            # 讀取影片
            streams= ffmpeg.input(filePath)
            audio= streams.audio
        except Exception as e:
            self.msgTrigger.emit("影片讀取失敗", "critical")
            return
        try:
            # 向右:順時針(clockwise), 向左:逆時針(counter clockwise)
            if self.radioLeft.isChecked():
                # transpose=1:順時針90度，transpose=2:逆時針90度，transpose=1,transpose=1:180度
                streams= ffmpeg.output(streams, audio, outputPath, vf=f'transpose=2')
            elif self.radioRight.isChecked():
                streams= ffmpeg.output(streams, audio, outputPath, vf=f'transpose=1')
            # 如果已經有檔案，則先刪除之間翻轉的結果
            if os.path.exists(outputPath):
                os.remove(outputPath)
            # 開始轉換
            # ffmpeg.run_async(streams, pipe_stdout=True, pipe_stderr=True, overwrite_output=True)
            # 改用compile獲取cmd用的args, 再由subprocess或QProcess執行, 以實時抓取stdout
            streams= ffmpeg.compile(streams)
            # compile之後的streams= ["ffmpeg", "其他選項指令", ...]
            self.process.start(streams[0], streams[1:])
        except Exception as e:
            self.msgTrigger.emit("影片轉換時發生錯誤", "critical")
            print(e)
        
    
    # 開始/關閉計時器, 並獲取QProcess的stdout
    def timerThread(self, status:bool):
        self.disableWigets(status)
        if status:
            self.threadpool.start(self.setTimer)
        else:
            if self.process.exitCode() == 0:
                # 結束訊息
                self.msgTrigger.emit("完成", "information")
    
    # timer
    def setTimer(self):
        startTime= datetime.datetime.now()
        progress, predict= "", ""
        while self.process.pid():
            delta= (datetime.datetime.now()- startTime).seconds
            # ffmpeg的輸出是放在stderr, 而不是stdout
            stdout= bytes(self.process.readAllStandardError()).decode("utf-8").replace('\n','').replace('\r','\n').strip()
            print(stdout, '-')
            # 確認輸出結果為"frame= 01 fps= 30 q=18.0 size=  123KiB time=00:00:01.23 bitrate=12345.6kbits/s speed=1.234x", 而不是其他影片資訊相關的輸出結果
            if stdout.startswith('frame='):
                # 如果1秒內有多個輸出, 取最新的
                # progress= stdout.split('\n')[-1]
                progress= stdout.split("frame=")[-1].split("fps=")[0]
                progress= int(progress)/self.video_frames
                if progress > 0:
                    predict= int(delta/progress)-delta
                    predict= f"預估剩餘時間 :  {predict//60 : >3d}:{predict%60 :0>2d},"
                progress= f"轉換進度 :  {progress*100 :.1f}%,"
            # 顯示結果到畫面上
            self.timerTrigger.emit(f"{predict}   {progress}   經過時間 :  {delta//60 : >3d}:{delta%60 :0>2d}\t")
            time.sleep(1)
        # 結束時, 如果沒有發生錯誤, 且輸出結果不是100%, 則調為100%
        if self.process.exitCode() == 0:
            self.timerTrigger.emit(f"轉換進度 :  100%,   經過時間 :  {delta//60 : >3d}:{delta%60 :0>2d}\t")
    
    # 更改介面狀態
    def disableWigets(self, status:bool):
        if status:
            self.startBtn.setText("轉換中..")
        else:
            self.startBtn.setText("開始")
        inputWidgets= self.centralwidget.findChildren((QtWidgets.QRadioButton, QtWidgets.QLineEdit, QtWidgets.QPushButton))
        for inputWidget in inputWidgets:
            inputWidget.setDisabled(status)
    
    # 訊息跳窗
    def showMsg(self, msg:str, icon:str="information"):
        # 建立訊息視窗
        msgBox= QtWidgets.QMessageBox(MainWindow)
        # 設定訊息類型和內容
        if icon == "information":
            msgBox.information(self, "訊息", msg)
        elif icon == "critical":
            msgBox.critical(self, "訊息", msg)
        elif icon == "warning":
            msgBox.warning(self, "訊息", msg)
        elif icon == "question":
            msgBox.question(self, "訊息", msg)
    
    # 關閉視窗時結束ffmpeg程序
    def closeEvent(self, event):
        self.threadpool.clear()
        self.process.kill()
        self.process.waitForFinished()
        sys.exit()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # ui = MyMainWindow()
    # ui.setupUi(MainWindow)
    # 直接建立MyMainWindow()物件, 才能夠覆寫closeEvent
    MainWindow = MyMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())