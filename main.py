import os

from thaicidhelper import *
from datathaicid import *
from imagehelper import *

from delphivcl import *

# DelphiVCL reference
# https://embarcadero.github.io/DelphiVCL4Python/reference.html

class FrmMain(Form):

    def __init__(self, owner):
       
        self.btnReset = None
        self.btnReadData = None
        self.btnClose = None
        self.btnSaveToClipboard = None
        self.btnSaveToFile = None
        self.bevel1 = None
        self.lblVersion = None       
        self.pnTop = None
        self.pnLeft = None
        self.pnRight = None
        self.pnBottom = None
        self.pnStatus = None
        self.mmData = None
        self.imgPerson = None
        
        # Free Form หรือไม่ก็ได้
        #self.FrmMain = None

        # Load UI
        self.LoadProps(os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.pydfm"))

    
        # self.Font.Name = 'Segoe UI'
        # self.Font.Color = clRed
        # self.Font.size = 12

        # คลาส Image ต้องถูกสร้างก่อนใช้งานเสมอ        
        self.imgPerson =  Image(self)
        self.imgPerson.Stretch = True
        
        #self.mmData.Font.size = 12
        
        
        self.SetupUI()
        
    
    def SetupUI(self):

        self.OnShow = self.onFrmMainShow
        self.OnClose = self.onFrmMainClose
        
        # ประกาศ Instance 
        # self.CIDReader = ThaiCIDHelper(APDU_SELECT,APDU_THAI_CARD,procStepNotify=self.showStepInfo)
        # self.CIDResponse = self.CIDReader.connectReader(0)
        
        # if autoRead == True:
        #     if self.CIDResponse[1] == True:
        #         # Read Data
        #         self.CIDReader.readData(
        #             procStepNotify=self.showStepInfo,
        #             procReadTextCallBack=self.showDataToMemo,
        #             procReadPhotoFinish=self.showPhoto)
        #     else:
        #         print(f'Error: {self.CIDReader.LastError}')
        
        
    def onFrmMainShow(self,sender):
        # ประกาศ Instance 
        self.CIDReader = ThaiCIDHelper(APDU_SELECT,APDU_THAI_CARD,procStepNotify=self.showStepInfo)
        self.CIDResponse = self.CIDReader.connectReader(0)
        print("Form-Show")
        print(self.CIDResponse)
        
        
    def onFrmMainClose(self,sender,action):
        action.Value = caFree


    def showStepInfo(self,message):
        self.pnStatus.Caption = message
        # สั่ง Update เพื่อ Repaint / Invalidate UI
        self.pnStatus.Update()


    def showDataToMemo(self,message):
        self.mmData.Lines.Add(message)


    def showPhoto(self,fileName):
        self.imgPerson.Hint = fileName
        self.imgPerson.Picture.LoadFromFile(fileName)


    def btnResetClick(self, Sender):
        self.imgPerson.Picture = None
        self.mmData.Lines.Text = ""
        self.showStepInfo("Reset CardReader ...")
        
        # free Instance
        self.CIDReader = None
        # set Instance
        self.CIDReader = ThaiCIDHelper(APDU_SELECT,APDU_THAI_CARD,procStepNotify=self.showStepInfo)
        for i in range(2):
            # 1 connect for kick old State (share-data to close-share)
            # 2 Normal connect
            self.CIDResponse = self.CIDReader.connectReader(0)

        # refresh Form
        self.Update()
        
        
    def btnReadDataClick(self, Sender):
        
        if self.CIDReader.Connected == True:
            # Read Data
            self.CIDReader.readData(
                procStepNotify=self.showStepInfo,
                procReadTextCallBack=self.showDataToMemo,
                procReadPhotoCallBack= self.showStepInfo,
                procReadPhotoFinish=self.showPhoto)
        else:
            print(f'Error: {self.CIDReader.LastError}')
            

    def btnCloseClick(self, Sender):
        Application.Terminate()


    def lblVersionClick(self, Sender):
        ShowMessage("About\nวรเพชร  เรืองพรวิสุทธิ์")


    def btnSaveToClipboardClick(self, Sender):
        if self.imgPerson.Hint != "":
            saveImageFileToClipboard(self.imgPerson.Hint)
        else:
            ShowMessage("ไม่พบข้อมูล !!")
        
        
    def btnSaveToFileClick(self, Sender):
        if self.mmData.Lines.Count > 0:
            dlgSave = SaveDialog(self)
            dlgSave.DefaultExt = ".txt"
            dlgSave.Filter = "Text file(*.txt)|.txt"
            dlgSave.FilterIndex = 0
            if dlgSave.Execute():
                self.mmData.Lines.SaveTofile(dlgSave.FileName,Encoding="UTF-8")
            
            dlgSave = None
        else:
            ShowMessage("ไม่พบข้อมูล !!")



def main():
    Application.Initialize()
    Application.Title = 'Python +Delphi GUI โปรแกรมอ่านบัตรประชาชน'
    MainForm = FrmMain(Application)
    MainForm.Show()
    
    # OSError: [WinError 6] The handle is invalid.
    # FreeConsole()
    
    
    Application.Run()
    
    # Application.FreeAndNil() 
    MainForm.Destroy()

if __name__ == '__main__':
    main()



"""
    - - paths "D:\anaconda3\envs\env311\Lib\site-packages"
    
    กรณี virtual path
    D:\anaconda3\envs\env311\Lib\site-packages
    
    กรณี delphivcl
    ** ดาวนโหลดโค้ด มาวาง
    https://pypi.org/project/delphivcl/#files
    
    "M:\pythonBOT\08 ThaiCIDHelper GUI\delphivcl\Win32"
    "M:\pythonBOT\08 ThaiCIDHelper GUI\delphivcl\Win64"
    
    
    AddDllDirectory
    
    pyinstaller --clean --noconsole --windowed --onefile --icon reader.ico --paths "M:\pythonBOT\08 ThaiCIDHelper GUI"  --hidden-import "delphivcl" --collect-all delphivcl  main.py


    pyinstaller --clean --noconsole --windowed --onefile --icon reader.ico --paths "D:\anaconda3\envs\env311\Lib\site-packages", --hidden-import "delphivcl" --add-data "D:\anaconda3\envs\env311\Lib\site-packages\delphivcl\Win64\DelphiVCL.pyd":.  main.py
    

    pyinstaller --clean --noconsole --windowed --onefile --icon reader.ico --paths "D:\anaconda3\envs\env311\Lib\site-packages", --hidden-import "delphivcl" --collect-submodules "delphivcl"  main.py

    pyinstaller --clean --noconsole --onefile --icon reader.ico  main.py
    pyinstaller --clean --noconsole --onefile --icon reader.ico -F --collect-all delphivcl main.py
    
    pyinstaller --clean --noconsole --onefile --windowed --icon reader.ico -F --collect-all delphivcl main.py
    pyinstaller --clean --noconsole --windowed --icon reader.ico --debug=imports main.py
    
    
    
    # pyinstaller --clean --noconsole --onefile --windowed  --icon reader.ico --paths "D:\anaconda3\envs\env311\Lib\site-packages" --hidden-import DelphiVCL main.py
    # ModuleNotFoundError: No module named 'delphivcl'
"""