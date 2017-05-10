import wx

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        self.controlPanel = wx.Panel(self, -1)
        self.drawPanel = wx.Panel(self, -1, size=(800,500))
        
        self.connectButton = wx.Button(self, -1, "Connect")
        self.topButton = wx.Button(self.drawPanel, -1, "1,2", pos=(375, 75))
        self.leftButton = wx.Button(self.drawPanel, -1, "3,4", pos=(25, 425))
        self.rightButton = wx.Button(self.drawPanel, -1, "5,6", pos=(725, 425))

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetTitle("Sierpinski's Triangle")
        self.SetSize((800, 600))
        self.controlPanel.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.drawPanel.SetBackgroundColour(wx.Colour(255, 255, 255))
        
        self.connectButton.Bind(wx.EVT_BUTTON, self.connect)
        self.drawPanel.Bind(wx.EVT_PAINT, self.on_paint) 
        

    def __do_layout(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        cSizer = wx.BoxSizer(wx.HORIZONTAL)

        cSizer.Add(self.connectButton, 1, wx.SHAPED)

        mainSizer.Add(self.drawPanel, 10, wx.EXPAND, 0)
        mainSizer.Add(cSizer, 1, wx.EXPAND, 1)
        
        self.SetSizer(mainSizer)
        self.Layout()

    def connect(self, event):
        print "Connect pressed."
        
    def on_paint(self, event):
        dc = wx.PaintDC(self.drawPanel)
        dc.SetPen(wx.Pen('black', 4))
        dc.DrawLine(400, 75, 50, 425)
        dc.DrawLine(400, 75, 750, 425)
        dc.DrawLine(50, 425, 750, 425)


if __name__ == "__main__":
    sTriangle = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    MainFrame = MyFrame(None, -1, "")
    sTriangle.SetTopWindow(MainFrame)
    MainFrame.Show()
    sTriangle.MainLoop()
