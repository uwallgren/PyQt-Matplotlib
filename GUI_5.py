# -*- coding: utf-8 -*-
''' 
GUI_5.py  matplotlib + PyQt5
C:\ProgramData\Anaconda3\lib\site-packages\matplotlib\mpl-data\images    mpl-data\matplotlibrc 

'''

import os, sys, time
import datetime as dt
import numpy as np
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QMainWindow, QPushButton
from PyQt5.QtGui import QIcon


import matplotlib
import matplotlib.pylab as mpl
#mpl.style.use('ggplot')  # better without
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar





class MyToolbar(NavigationToolbar):
    TIPS=['Red','Green','Blue','Yellow','Sync']
    def __init__(self, canvas, parent):
        self.parent=parent
        NavigationToolbar.__init__(self, canvas, parent, coordinates=False)
        self.addAction('')  # use when eidth> 650   
 
        self.addAction(QIcon("icons/sync.png"),  self.TIPS[4], self.icon4)    
        self.addAction(QIcon("icons/rspot.png"),       self.TIPS[0], self.icon0)    
        self.addAction(QIcon("icons/gspot.png"), self.TIPS[1], self.icon1)    
        self.addAction(QIcon("icons/bspot.png"), self.TIPS[2], self.icon2)    
        self.addAction(QIcon("icons/yspot.png"), self.TIPS[3], self.icon3)    

        #Not working
        size = super().sizeHint()
        size.setHeight(30)
 
    def icon0(self): self.parent.icon0()
    def icon1(self): self.parent.icon1() 
    def icon2(self): self.parent.icon2() 
    def icon3(self): self.parent.icon3() 
    def icon4(self): self.parent.icon4() 

class pointAndFigure(QWidget):
    def __init__(self, activeId, handNN=[]):
        QWidget.__init__(self)
        '''Create Window'''
        self.setGeometry(200, 200, 675, 400)
        self.handNN=handNN
        self.activeId=activeId
        # Add plot figure
        vLayout=QVBoxLayout()
        self.fig=Figure()
        self.fig, self.ax=mpl.subplots(1)
        self.fig.subplots_adjust(top=0.91, bottom=0.075, left=0.05, right=1.0, wspace=0.095) #, hspace=0.32, wspace=0.2)
        self.canvas = FigureCanvas(self.fig)
        #self.canvas.set_window_title('Point & Figure')
        self.canvas.mpl_connect('motion_notify_event', self.mouseMoved)               
        self.canvas.mpl_connect('button_press_event', self.clicked) # Must set FocusPolicy for key_press              
        self.canvas.setFocusPolicy( QtCore.Qt.ClickFocus )
  
        vLayout.addWidget(self.canvas)             #(row, col, hight, width)
        toolbar = MyToolbar(self.canvas, self)
        vLayout.addWidget(toolbar)
        self.setLayout(vLayout)         
 
        self.name=''
        self.txt1=[]
        self.action0()
        self.show()
    
    def mouseMoved(self,event):
        if event.canvas.underMouse:
            if event.ydata==None: return
            xx=self.ax.get_xlim()
            yy=self.ax.get_ylim()
            str2='{:10s} x={:4.1f}, y={:4.1f}'.format(self.name, event.xdata,event.ydata)
            if self.txt1==[]: 
                self.txt1=self.ax.text(xx[0], yy[1], str2)
            else:
                self.txt1.set_text(str2)
            self.canvas.draw()
        
    def clicked(self,event):
        # Do somthing when click in left or right part of window
        if event==[]: return
        if event.canvas.underMouse:
            w=self.geometry().width()
            if event.x<w/2:
                self.action0()
            else:
                self.action1()
                
    def icon0(self): 
        # Red
        self.action0()
        
    def icon1(self):
        # Green
        self.action1()
   
    def icon2(self): pass # Blue
    def icon3(self): pass # Yellow
    def icon4(self): pass #Sync 
    
    def action0(self):
        '''sinc'''
        self.ax.clear()
        x=np.arange(1,100,0.1)
        y=np.sin(x)/x
        self.plotAx(x,y,'Sinc(x)')
          
    def action1(self):
        '''sin'''
        self.ax.clear()
        x=np.arange(1,100,0.1)
        y=np.cos(x)
        self.plotAx(x,y,'Cos(x)')
        
    def plotAx(self, x, y, name):    
        self.name=name
        self.ax.clear()
        self.txt1=self.ax.text(x[0], np.max(y), self.name)
        self.ax.plot(x,y,'r',linewidth=1)
        self.canvas.draw()
    
        
def main():
    app = QApplication([])
    p=pointAndFigure([])
    app.exec_()
    
if __name__=='__main__':
    main()
