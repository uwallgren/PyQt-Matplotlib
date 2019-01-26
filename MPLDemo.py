# -*- coding: utf-8 -*-
'''
GUIDemo.py  
PyQt5 and matplotlib based 
TODO


'''
import sys, os
import numpy as np
import pickle
from PyQt5 import QtCore, QtGui, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QMainWindow, QPushButton, QHeaderView, QLabel,QSizePolicy
import matplotlib
import matplotlib.pylab as plt
plt.style.use('ggplot')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class MyToolbar(NavigationToolbar):
    def __init__(self, canvas, parent):
        self.parent=parent
        NavigationToolbar.__init__(self, canvas, parent)
        self.addAction(QIcon("icons/cow.jpg"),           'CalcTLBook1', self.icon0)    
#        self.addAction(QIcon(''), 'ICON0', self.icon0)    
        self.addAction(QIcon(''), '')
        self.addAction(QIcon("icons/sync.jpg"), 'Sync all', self.icon1)    
        self.addAction(QIcon("{}"),           '---')
        self.addAction(QIcon("icons/red_cross.jpg"), 'Remove', self.icon2)    
        self.addAction(QIcon("icons/downarrowgreen.jpg"), 'Add', self.icon3)    

    def icon0(self): self.parent.action0(False)
    def icon1(self): self.parent.action1('Hej')
    def icon2(self): self.parent.action2()
    def icon3(self): self.parent.action3()

class MPLDemo(QWidget):
    def __init__(self, id=[], handle=[]):
        QWidget.__init__(self)
        self.id=id
        self.handle = handle
        self.cnds=[]
        self.days=120
        self.mx=0;  self.my=0   # Mouse moved position
        self.key=''             # Key pressed
        
        self.point1=self.point2=self.point3=(); 
    
        self.setWindowTitle('Candlesticks')
        self.setGeometry(200, 400, 1450, 600)   # (left, top, width, height)
        
        self.fig=Figure()
        self.ax = self.fig.add_subplot(111) 
        self.canvas = FigureCanvas(self.fig)
        #self.ax=self.canvas.figure.add_subplot(111)
        self.cursor = matplotlib.widgets.Cursor(self.ax, linewidth=1, color='g')

        self.fig.subplots_adjust(top=1.0, bottom=0.07, left=0.03, right=1.0, hspace=0.32, wspace=0.2)
        xxx=0        

        exp=QSizePolicy.Expanding        
        self.canvas.setSizePolicy(exp,exp)     
                
        leftLayout=QVBoxLayout()        
        leftLayout2=QVBoxLayout()
        butLabels=['Clear','BUT1','BUT2','BUT3']
        butActions=[self.action0, self.action1, self.action2, self.action3] 
        self.buts=[]
        for i in range(len(butLabels)):
            but=QPushButton(butLabels[i])
            but.clicked.connect(butActions[i])
            but.setStyleSheet('background-color: lightgrey')
            but.setToolTip(str(i))
            leftLayout.addWidget(but)
            self.buts.append(but)
            
        gLayout=QGridLayout()
        rLayout=QVBoxLayout()        
        self.label1=QPushButton()
        exp=QSizePolicy.Expanding
        self.label1.setSizePolicy(exp,exp)
        self.label1.setFixedHeight(30)    
        #self.label1.setStyleSheet(" font-size:20px; background-color: rgb(255, 0, 255); border:4px solid rgb(0, 255, 0); font-size:30px;")
        self.label1.setStyleSheet(" font-size:20px; background-color: rgb(255, 255, 0);")
        rLayout.addWidget(self.label1, alignment=QtCore.Qt.AlignCenter)                        
        rLayout.addWidget(self.canvas) 
        toolbar = MyToolbar(self.canvas, self)
        rLayout.addWidget(toolbar) 
        gLayout.addLayout(leftLayout,0,0,2,1)
        gLayout.addLayout(leftLayout2,0,1,2,1)
        gLayout.addLayout(rLayout,0,2,5,20)
        self.setLayout(gLayout)
        
        #Mouse events
        self.canvas.mpl_connect('button_press_event', self.clicked)
        self.canvas.mpl_connect('motion_notify_event', self.moved)  
        self.canvas.mpl_connect('draw_event', self.zoomed)          self.canvas.mpl_connect('key_press_event', self.on_key) # Must set FocusPolicy and Focus for key_press              
        self.canvas.setFocusPolicy( QtCore.Qt.ClickFocus )
        self.canvas.setFocus()
        
   
    def run(self): 
        self.points=[]
        self.plotplot(self.id)        
        self.show()    
        
    def clicked(self,event):
        # Rescaling data does not work good with zoom funtion 
        if event==[]: return
        if event.canvas.underMouse:
            if event.button==1:
                if self.key=='f1': self.point1=(event.xdata, event.ydata)
                if self.key=='f2': self.point2=(event.xdata, event.ydata)
                if self.key=='f3': self.point3=(event.xdata, event.ydata)
                self.drawPoint()
 
    def drawPoint(self):
        if self.point1==(): return
        self.points.append(self.ax.plot(self.point1[0],self.point1[1],'or'))
        self.moved(False)
   
    def moved(self, event,N=0):
        if event==False:
            str1='{} {} {} {} '.format(' '*50, N, self.key, ' '*50)
            self.label1.setText(str1) 
            self.canvas.draw()
            return
        try:
            if event.canvas.underMouse:
                self.mx=event.xdata
                self.mx=np.datetime64(int(self.mx), 'D')
                self.my=event.ydata
                str1='{} {} {} - {:5.2f} {}'.format(' '*50, self.key, self.mx, self.my, ' '*50)
                self.label1.setText(str1)
                #self.canvas.draw()
        except:
            pass
 
    def zoomed(self, event):
        #print('zoomed', event)
        axf=self.ax.get_xticks()  #     get_major_formatter()
        lab=[np.datetime64(int(x),'D') for x in axf]
        lab=[np.datetime_as_string(x) for x in lab]
        self.ax.set_xticklabels(lab)
 
    def on_key(self, event):
        #print('you pressed', event.key, event.xdata, event.ydata)
        self.key=event.key
        self.moved(False)
        
    def labelClicked(self, event):
        print('labelClicked')
 
    def colorButs(self, nr):
        for i in [1,2,3]:
            but=self.buts[i]
            but.setStyleSheet('background-color: lightgrey')
        self.buts[nr].setStyleSheet('background-color: lightgreen')
                
    def action0(self, event=[]):
        #if self.points==[]: return
        for line in self.ax.lines.copy():
            color=line.get_color()
            if color=='r': line.remove()
        self.key=''    
        self.point1=()
        self.moved(False)     
            
            
    def action1(self, event=[]): self.colorButs(1)
    def action2(self, event=[]): self.colorButs(2)
    def action3(self, event=[]): self.colorButs(3)
    
    def plotplot(self,id):    
        refday=np.arange('2019-01-30', '2019-01-01', dtype='datetime64[D]')
         
        x=np.arange(0,25,0.1)
        y=np.sin(x)
        #x=[np.datetime64(z,'D') for z in x]
        #self.x=[z.astype('int64') for z in x]
        #self.y=stock.last[-self.days:]
        #self.ax.cla()
        self.lines =self.ax.plot(x, y,'b', linewidth=0.5)
        self.moved(False)
        self.canvas.draw()
           
if __name__ == "__main__":    
    app = QApplication(sys.argv)
    win = MPLDemo('DEMO')
    win.run()
    sys.exit( app.exec_())

