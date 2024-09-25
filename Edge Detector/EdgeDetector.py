from PyQt5.QtWidgets import QLabel,QPushButton,QFileDialog,QSpacerItem,QSizePolicy,QVBoxLayout,QHBoxLayout,QApplication,QWidget
from PyQt5.QtGui import QIcon,QPixmap,QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np
import sys

class MainAppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.showFullScreen()
        self.vertical_kernel=np.array([[0.25,0,-0.25],
                 [1,0,-1],
                 [1.75,0,-1.75]])
        self.horizontal_kernel=np.array([[1,1,1],
                            [0,0,0],
                            [-1,-1,-1]])
        self.setWindowTitle("EdgeSearch")
        self.init_ui()
    
    def keyPressEvent(self, event):
        if event.key()==Qt.Key_F11:
            self.showFullScreen()
        if event.key()==Qt.Key_Escape:
            self.showNormal()

    

    def init_ui(self):
        self.State="Vertical"
        self.layout=QVBoxLayout()
        title=QLabel("Image Edge Detector ",alignment=Qt.AlignCenter)
        title.setStyleSheet('''
                            font-size:80px;
                            color:black;
                            
                            ''')
        self.image_layout=QHBoxLayout()
        open_file_button=QPushButton("Select An Image !")
        open_file_button.setStyleSheet('''
                                font-size:50px;
                                background-color:blue;
                                color:white;
                                ''')
        open_file_button.clicked.connect(self.open_file)
        self.stateButton=QPushButton(text=self.State)
        self.stateButton.setStyleSheet('''
                                font-size:50px;
                                background-color:blue;
                                color:white;
                                ''')
        self.stateButton.clicked.connect(self.changeState)
        
        
        self.layout.addWidget(title)
        self.layout.addWidget(open_file_button)
        self.layout.addWidget(self.stateButton)
        self.setLayout(self.layout)
    
    def open_file(self):
        opt=QFileDialog.Options()
        file_filter = "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        filepath,file=QFileDialog.getOpenFileName(self,"Select An Image","",file_filter,options=opt)
        
        while self.image_layout.count():
            child = self.image_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if filepath:
            
            self.addImageToBox(filepath)
            img_=cv2.imread(filepath,cv2.IMREAD_GRAYSCALE)
            if self.State=="Vertical":
                img_1=cv2.filter2D(img_,-1,self.vertical_kernel)
                cv2.imwrite("EdgedImage.jpg",img_1)
                
                self.addImageToBox(r"EdgedImage.jpg")
            else:
                img_2=cv2.filter2D(img_,-1,self.horizontal_kernel)
                cv2.imwrite("EdgedImage.jpg",img_2)
                
                self.addImageToBox(r"EdgedImage.jpg")
    
    def addImageToBox(self,filepath):
        img_label=QLabel("hi",alignment=Qt.AlignCenter)
        image=QImage(filepath)
        image=QPixmap(image.scaled(400,400))
        img_label.setPixmap(image)
        img_label.setStyleSheet(    '''    QLabel {
                            font-size:20px;
                            background-color:black;
                            border: 20px solid #16b851;
                            border-radius:20px;
                            color:white;
                                }
                       '''     
        )
        self.image_layout.addWidget(img_label)
        self.image_layout.addSpacerItem(QSpacerItem(0,30,QSizePolicy.Minimum,QSizePolicy.Expanding))
        self.layout.addLayout(self.image_layout)
        if self.layout.indexOf(self.image_layout) == -1:
            self.layout.addLayout(self.image_layout)
    
    def changeState(self):
        self.State="Vertical" if self.State=="Horizontal" else "Horizontal"
        self.stateButton.setText(self.State)

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainAppWindow()
    window.show()
    sys.exit(app.exec_())