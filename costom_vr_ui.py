# cd to python/Scripts
# pyuic5 -x "D:\OneDrive\Documents\workspace\python\video-flip\vr_ui.ui" -o "D:\OneDrive\Documents\workspace\python\video-flip\vr_ui.py"
from PyQt5 import QtCore, QtWidgets
from vr_ui import Ui_MainWindow
import sys, os, datetime, time, ffmpeg, traceback





class MyMainWindow(Ui_MainWindow, QtWidgets.QMainWindow):
    # 在thread或subprocess中, 要顯示訊息用的trigger
    msgTrigger= QtCore.pyqtSignal(str, str)
    # 在timer thread中, 要在介面上顯示輸出訊息用的trigger
    timerTrigger= QtCore.pyqtSignal(str)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        
        # 瀏覽按鈕按下
        self.browseBtn.clicked.connect(self.browseFileDialog)
        # 選擇輸入/輸出類型時, 如果不是fisheye, 就disable fisheye的fov選項
        for radioBtn in self.inputGroup.findChildren((QtWidgets.QRadioButton,)):
            radioBtn.toggled.connect(self.setFisheyeFOV_disable)
        # 輸入路徑時, 設定預設輸出路徑與名稱
        self.input_filePath.textChanged.connect(self.setOutputName)
        # 選擇輸出類型時, 設定預設輸出路徑與名稱
        for radioBtn in self.outputGroup.findChildren((QtWidgets.QRadioButton,)):
            radioBtn.toggled.connect(self.setFisheyeFOV_disable)
            radioBtn.toggled.connect(self.setOutputName)
        # 開始按鈕按下
        self.startBtn.clicked.connect(self.run)
        # 設定影片轉換程序
        self.process= QtCore.QProcess(self)
        # 獲取影片轉換程序的stdout, 並開始計時器
        # self.process.readyRead.connect(lambda: self.timerThread(True))
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
    def browseFileDialog(self):
        filePath, _= QtWidgets.QFileDialog.getOpenFileName()
        self.input_filePath.setText(filePath)
        # 同時設定輸出位置
        self.setOutputName()
    
    # 設定魚眼FOV設定欄是否disable
    def setFisheyeFOV_disable(self):
        groups= {self.inputGroup:self.input_fov, self.outputGroup:self.output_fov}
        for group in groups:
            checkedOptionName= self.getRadioValue(group).objectName()
            groups[group].setDisabled("fisheye" not in checkedOptionName)
    
    # 設定預設輸出路徑與名稱
    def setOutputName(self):
        if filePath:= self.input_filePath.text():
            outputType= self.getRadioValue(self.outputGroup).text()
            newfileName= os.path.splitext(filePath)
            self.output_filePath.setText(newfileName[0]+ '-'+ outputType+ newfileName[1])
    
    # 確認radio button的值
    def getRadioValue(self, group:QtWidgets.QGroupBox):
        radioBtns= group.findChildren((QtWidgets.QRadioButton,))
        for radioBtn in radioBtns:
            if radioBtn.isChecked():
                return radioBtn
    
    # 開始
    def run(self):
        # 設定ffmpeg的路徑(環境變數)
        os.environ['PATH'] += ';'+ os.path.join(os.path.dirname(__file__),"static","ffmpeg")
        try:
            filePath= self.input_filePath.text()
            # 取得影片資訊
            streams= ffmpeg.probe(filePath)
            streams = [stream for stream in streams["streams"] if stream["codec_type"] == "video"]
            width,height, self.video_frames= streams[0]["width"], streams[0]["height"], int(streams[0]["nb_frames"])
            # 讀取影片
            streams= ffmpeg.input(filePath)
            audio= streams.audio
        except Exception as e:
            self.msgTrigger.emit("影片載入錯誤", "critical")
            print(e)
            print(traceback.format_exc())
            return
        try:
            # 輸入選項  1:上下/左右格式, 2:180°/360°/魚眼
            iOptions= self.getRadioValue(self.inputGroup).objectName().split('_')
            oOptions= self.getRadioValue(self.outputGroup).objectName().split('_')
            # 分割左右眼的視訊, splitedStream[0]:左眼,[1]:右眼, 上下:左眼在上,右眼在下
            if iOptions[1]=="flat" or oOptions[1]=="flat":
                splitedStream= [streams]
            elif iOptions[1] == "lr":
                splitedStream= [ffmpeg.crop(streams, width=width//2, height=height, x=0, y=0), ffmpeg.crop(streams, width=width//2, height=height, x=width//2, y=0)]
                width//= 2
            elif iOptions[1] == "ud":
                splitedStream= [ffmpeg.crop(streams, width=width, height=height//2, x=0, y=0), ffmpeg.crop(streams, width=width, height=height//2, x=0, y=height//2)]
                height//= 2
            # 將輸入180度的先拉伸成360度, 再去做接下來的處理, 確保視野外的部分為全黑色的背景, 避免出現邊緣的像素被拉伸的現象
            if iOptions[2]=="180" and oOptions[2] in ["360", "fisheye"]:
                for i in range(2):
                    splitedStream[i]= ffmpeg.filter(splitedStream[i], "pad", width=f"{width*2}", height=f"{height}", x=f"{width//2}", y='0')
                iOptions[2]= "360"
            # 處理影像類型
            if iOptions[2:] != oOptions[2:]:
                for i in range(len(splitedStream)):
                    options_trans= {"180":"hequirect","360":"equirect","fisheye":"fisheye", "flat":"flat"}
                    filter_args= {"input":options_trans[iOptions[2]], "output":options_trans[oOptions[2]]}
                    if iOptions[2] == "fisheye": filter_args= {**filter_args, **{"ih_fov":self.input_fov.text(), "iv_fov":self.input_fov.text()}}
                    if oOptions[2] == "fisheye": filter_args= {**filter_args, **{"h_fov":self.output_fov.text(), "v_fov":self.output_fov.text()}}
                    splitedStream[i]= ffmpeg.filter(splitedStream[i], "v360", **filter_args)
            # 將分割的左右眼影像堆疊
            if iOptions[1]=="flat" or oOptions[1]=="flat":
                streams= splitedStream[0]
            elif oOptions[1] == "lr":
                streams= ffmpeg.filter(splitedStream, 'hstack')
            elif oOptions[1] == "ud":
                streams= ffmpeg.filter(splitedStream, 'vstack')
            # 設置輸出, 並合併從原始影片來的音訊與新的視訊(有時在過多操作後會丟失音訊), crf:0~29(壓縮率,0=幾乎無壓縮)
            streams= ffmpeg.output(streams, audio, self.output_filePath.text(), crf=10)
            # 如果已經有檔案，則先刪除之間轉換的結果
            if os.path.exists(self.output_filePath.text()):
                os.remove(self.output_filePath.text())
            # 開始轉換
            # ffmpeg.run_async(streams, pipe_stdout=True, pipe_stderr=True, overwrite_output=True)
            # 改用compile獲取cmd用的args, 再由subprocess或QProcess執行, 以實時抓取stdout
            streams= ffmpeg.compile(streams)
            print(streams)
            # compile之後的streams= ["ffmpeg", "其他選項指令", ...]
            self.process.start(streams[0], streams[1:])
            
        except Exception as e:
            self.msgTrigger.emit("影片轉換時發生錯誤", "critical")
            print(e)
            print(traceback.format_exc())
    
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
        # QProcess.pid() : If its running, the pid will be > 0
        # QProcess.state() : Check it again the ProcessState enum to see if its QProcess::NotRunning
        # QProcess.atEnd() : Its not running if this is true
        while self.process.state():
            print(self.process.state())
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
        inputWidgets= self.centralwidget.findChildren((QtWidgets.QRadioButton, QtWidgets.QLineEdit, QtWidgets.QSpinBox, QtWidgets.QPushButton))
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