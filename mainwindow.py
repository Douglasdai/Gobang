import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QCoreApplication
#import AI_doodlesnake_game
import doodlesnake_game
import main

        
class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    

    def initUI(self):
        #五子棋系列按钮
        #AI对战
        QToolTip.setFont(QFont('SansSerif',10))
        fiveinrow = QPushButton('对战五子棋',self)
        fiveinrow.setToolTip('这是一个<b>AI五子棋</b>对战游戏')
        fiveinrow.clicked.connect(main.USER_AI)
        fiveinrow.resize(fiveinrow.sizeHint())
        fiveinrow.move(20,30)

        #观看AI vs AI
        fiveinrow = QPushButton('观看AI五子棋',self)
        fiveinrow.setToolTip('这是一个<b>AI VS AI五子棋</b>对战游戏')
        fiveinrow.clicked.connect(main.AI_AI)
        fiveinrow.resize(fiveinrow.sizeHint())
        fiveinrow.move(20,60)

        #用户对用户
        fiveinrow = QPushButton('五子棋',self)
        fiveinrow.setToolTip('这是一个<b>五子棋</b>对战游戏')
        fiveinrow.clicked.connect(main.USER_USER)
        fiveinrow.resize(fiveinrow.sizeHint())
        fiveinrow.move(20,90)

        #贪吃蛇按钮
        doodlesnake = QPushButton('贪吃蛇',self)
        doodlesnake.setToolTip('这是一个<b>贪吃蛇</b>游戏')
        doodlesnake.clicked.connect(doodlesnake_game.main)
        doodlesnake.resize(doodlesnake.sizeHint())
        doodlesnake.move(20,120)
        
        #退出按钮
        exit_ = QPushButton('退出',self)
        exit_.clicked.connect(QCoreApplication.instance().quit)
        exit_.setToolTip('这是一个<b>退出</b>按钮')
        exit_.resize(exit_.sizeHint())
        exit_.move(20,180)


        self.setGeometry(300,300,300,220)
        self.setWindowTitle('Games')
        self.setWindowIcon(QIcon('game_icon.png'))
        self.center()
        self.show()
    #退出挽留
    def closeEvent(self,event):
        reply = QMessageBox.question(self,'退出提示','确定退出？(Y/N)',QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        
        if reply ==QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    #中心显示
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ =='__main__':
    app= QApplication(sys.argv)
    ex =Example()
    sys.exit(app.exec_())