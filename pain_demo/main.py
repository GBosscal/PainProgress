import sys
import cv2
import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow ,QGraphicsScene, QGraphicsPixmapItem, QFileDialog
from PyQt5.QtCore import Qt,pyqtSignal,QCoreApplication
from PyQt5.QtGui import QPixmap,QImage
#from main_window import Ui_MainWindow  # 加载我们的布局
from window import Ui_MainWindow  # 加载我们的布局


#from change import change_bg
from pain_convert import pain_convert

class Mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(Mainwindow, self).__init__(*args, **kwargs)
        self.setupUi(self)  # 初始化ui
        # 在这里，可以做一些UI的操作了，或者是点击事件或者是别的
        # 也可以另外写方法，可以改变lable的内容
        # 设置窗口的最大和最小尺寸
        self.setMaximumSize(1500,800)#显示窗口的宽和高
        self.setMinimumSize(1500, 800)

        # 连接按钮的点击事件到对应的函数
        self.pushButton.clicked.connect(self.getImage)#进入函数
        self.pushButton_2.clicked.connect(self.save)#进入函数
        #self.pushButton_2.clicked.connect(self.classification)#进入函数
        # 初始化一些变量
        import numpy as np
        self.result = np.ones((3, 3), dtype=np.uint8)
        self.image = QPixmap()
        self.signal.connect(self.show_result)

    def getImage(self):
        #(*.png);(*.jpg);(*.jpeg)
        # 通过文件对话框选择图片文件
        path = QFileDialog.getOpenFileName(self, "选取文件", "test_image/", "")[0]
        if path == '':
            pass
        else:
            #self.image.load(path)
            #self.image_ = cv2.imread(path)
            self.image.load(path)
            self.image_ = cv2.imread(path)
            self.LoadImage()
    '''
    def LoadImage(self):
        # 加载图片到 QGraphicsView 中显示
        self.graphicsView.scene = QGraphicsScene()  # 创建一个图片元素的对象
        item = QGraphicsPixmapItem(self.image)  # 创建一个变量用于承载加载后的图片
        self.graphicsView.scene.addItem(item)  # 将加载后的图片传递给scene对象
        item.setScale(self.graphicsView.width()/self.image.width())
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setScene(self.graphicsView.scene)
        threading.Thread(target=self.convert,args=()).start()
        '''
    def LoadImage(self):
        # 加载图片到 QGraphicsView 中显示
        # 创建一个 QGraphicsScene 对象
        self.graphicsView.scene = QGraphicsScene()

        # 创建一个 QGraphicsPixmapItem 对象用于加载图片
        item = QGraphicsPixmapItem(self.image)

        # 将加载后的图片元素添加到 scene 中
        self.graphicsView.scene.addItem(item)

        # 根据视图和图片的比例设置图片的缩放
        item.setScale(self.graphicsView.width() / self.image.width())

        # 禁用水平和垂直滚动条
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
       # 将 scene 设置为 graphicsView 的场景
        self.graphicsView.setScene(self.graphicsView.scene)
    # 在新线程中开始图片转换
        threading.Thread(target=self.convert,args=()).start()
    # 转换背景并更新界面
 
     # 定义一个名为 "convert" 的方法
    def convert(self):
        # 定义一个用于多语言翻译的函数，将其赋值给 _translate 变量
        _translate = QCoreApplication.translate
        
        # 设置一个名为 pushButton_2 的按钮的文本为 "正在转换"，通过多语言翻译函数 _translate 来支持翻译
        self.pushButton_2.setText(_translate("MainWindow", "正在识别"))
        
        # 禁用 pushButton_2 按钮，使其在转换过程中不可点击
        self.pushButton_2.setDisabled(True)
        
        # 将成员变量 self.image_ 的值赋给成员变量 self.result
        img = cv2.cvtColor(self.image_, cv2.COLOR_BGR2GRAY)
        #self.image_是sorce,即src
        #img是3维张量
        self.result = pain_convert(img,self.image_)
        
        # 发出一个信号，用于通知其他部分代码有一些操作已经完成
        self.signal.emit()
        
        # 重新启用 pushButton_2 按钮，使其可点击
        self.pushButton_2.setDisabled(False)
        
        # 将 pushButton_2 按钮的文本更新为 "保存图片"，通过多语言翻译函数 _translate 来支持翻译
        self.pushButton_2.setText(_translate("MainWindow", "保存"))


    
    def show_result(self):
        # 在另一个 QGraphicsView 中显示处理后的图片

        # 将结果图片的通道从 BGR 转换为 RGB
        self.result_show = cv2.cvtColor(self.result, cv2.COLOR_BGR2RGB)#转换图像通道
        #self.result_show=self.result
        # 创建一个 QImage 对象以及相关的 QPixmap 和 QGraphicsPixmapItem
        
        # 创建一个 QImage 对象
        frame = QImage(self.result_show, self.result.shape[1], 
                       self.result.shape[0], self.result.shape[1] * 3, 
                       QImage.Format_RGB888)
        #shape[1]是宽度，shape[0]是宽度，因为使用了Format_RGB888格式
        #所有要用shape[1] * 3来表示，rgb三个通道
        # 从 QImage 创建一个 QPixmap 对象
        pix = QPixmap.fromImage(frame)

        # 使用 QPixmap 创建一个 QGraphicsPixmapItem 对象
        item = QGraphicsPixmapItem(pix) #创建像素图元
        # 设置图片在 QGraphicsView 中的比例
        item.setScale(self.graphicsView.width() / (self.image.width()+1))
        # 创建一个新的 QGraphicsScene，并将图片元素添加到其中
        self.graphicsView_2.scene=QGraphicsScene()                             #创建场景
        self.graphicsView_2.scene.addItem(item)
        #禁用滚动条
        self.graphicsView_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
         # 将新的 QGraphicsScene 设置给 QGraphicsView
        self.graphicsView_2.setScene(self.graphicsView_2.scene)                      #将场景添加至视图
    
    def save(self):
        save_path = QFileDialog.getSaveFileName(self, "选取文件", "h:", "")[0]
        if save_path == '':
            pass
        else:
            cv2.imwrite(save_path,self.result)





if __name__ == '__main__':  # 程序的入口
    app = QApplication(sys.argv)
    win = Mainwindow()
    win.show()
    sys.exit(app.exec_())
