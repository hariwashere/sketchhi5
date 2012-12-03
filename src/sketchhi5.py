import cStringIO
import urllib2
import simplejson
import wx
import cv2.cv as cv
import os

class Panel1(wx.Panel):

#Create the panel, search box and search button
    def __init__(self, parent, id):        
        wx.Panel.__init__(self, parent, id)
        self.index = 0
        self.current_image_id = "-1"
        self.btn = wx.Button(self, label="Search", pos=(390, 500))
        self.btn.Bind(wx.EVT_BUTTON, self.searchButtonClick)
        self.control = wx.TextCtrl(self, size=(350, 30), pos=(20, 500))
        self.btn = wx.Button(self, label="Refresh Images", pos=(490, 300))
        self.btn.Bind(wx.EVT_BUTTON, self.refresh_button_click)
        self.slider = wx.Slider(self, -1, 125, 0, 1000, (250,460))
        self.slider.Bind(wx.EVT_SCROLL_CHANGED, self.slider_position_changed)
        filedata= open("question.png", "rb").read()
        stream = cStringIO.StringIO(filedata)
        image = wx.ImageFromStream(stream)
        self.question_bmp = wx.BitmapFromImage(image)
        self.button= [wx.BitmapButton(self, -1 ,self.question_bmp, (205, 5)),
        wx.BitmapButton(self, -1 ,self.question_bmp, (405, 5)),
        wx.BitmapButton(self, -1 ,self.question_bmp, (605, 5)),
        wx.BitmapButton(self, -1 ,self.question_bmp, (805, 5))]

    @staticmethod
    def search_image(search_string, index):
        url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&start='+str(index)+ '&imgsz=medium&q='+search_string+'&userip=INSERT-USER-IP')
        request = urllib2.Request(url, None, {'Referer': 'google.com'})
        response = urllib2.urlopen(request)
        return simplejson.load(response)

    @staticmethod
    def obtain_bmp_image(self, url):
            filedata = urllib2.urlopen(url).read()
            stream = cStringIO.StringIO(filedata)
            image = wx.ImageFromStream(stream)
            if(image.IsOk()):
                resizedimage = image.Scale(200, 200, wx.IMAGE_QUALITY_HIGH)
                return wx.BitmapFromImage(resizedimage)
            else:
                return self.question_bmp

    @staticmethod
    def render_outline_image(image_id, threshold):
        im=cv.LoadImage("Image"+str(image_id)+".bmp", cv.CV_LOAD_IMAGE_COLOR)
        gray = cv.CreateImage((im.width, im.height), 8, 1)
        edge = cv.CreateImage((im.width, im.height), 8, 1)
        im_bw1 = cv.CreateImage((im.width, im.height), 8, 1)
        cv.CvtColor(im, gray, cv.CV_BGR2GRAY)
        cv.Not(gray, edge)
        im_white=cv.LoadImage("white.bmp", cv.CV_LOAD_IMAGE_COLOR)
        white = cv.CreateImage((im_white.width, im_white.height), 8, 1)
        cv.Canny(gray, edge, threshold, 125 * 3, 3)
       # cv.Not(white, edge)
        cv.SaveImage("edge_image.png", edge)
        jpg1 = wx.Image('edge_image.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        os.remove("edge_image.png")
        return jpg1

    def refresh_button_click(self, event):
        for i in range(0,4):
            os.remove("Image"+str(i)+".bmp");
        self.index+=4
        results = Panel1.search_image(self.control.GetValue(), self.index)
        for i in range(0,4):
            bmp = Panel1.obtain_bmp_image(self, results['responseData']['results'][i]['unescapedUrl'])
            self.button[i].SetBitmapLabel(bmp)
            #bitmapbutton=wx.BitmapButton(self,-1,bmp, (5 + i*200,5))
            #bitmapbutton.Bind(wx.EVT_LEFT_DOWN, lambda event, arg=i: self.onImageClick(event, arg))
            bmp.SaveFile("Image"+str(i)+".bmp",wx.BITMAP_TYPE_BMP)    

    def slider_position_changed(self,event):
        #Do Image Processing
        image = Panel1.render_outline_image(self.current_image_id, self.slider.GetValue())
        bitmapbutton=wx.BitmapButton(self,-1,image, (200,250))
        
#Call Google API and retrieve images. Create bitmapbutton controls and display the images. Set onImageClick bindings
    def searchButtonClick(self, event):
        self.index = 1
        results = Panel1.search_image(self.control.GetValue(), self.index)
        for i in range(0,4):
            bmp = Panel1.obtain_bmp_image(self, results['responseData']['results'][i]['unescapedUrl'])
            self.button[i].SetBitmapLabel(bmp)
            #bitmapbutton=wx.BitmapButton(self,-1,bmp, (5 + i*200,5))
            self.button[i].Bind(wx.EVT_LEFT_DOWN, lambda event, arg=i: self.onImageClick(event, arg))

            bmp.SaveFile("Image"+str(i)+".bmp",wx.BITMAP_TYPE_BMP)

#Do image processing and show result         
    def onImageClick(self,event,arg):        
        #Do Image Processingc
        self.current_image_id = str(arg)
        image = Panel1.render_outline_image(self.current_image_id, self.slider.GetValue())
        bitmapbutton=wx.BitmapButton(self,-1,image, (200,250))
    
    
wx.InitAllImageHandlers()
app = wx.PySimpleApp()
frame1 = wx.Frame(None, -1, "Sketch-hi-5", size = (1100, 650))
Panel1(frame1,-1)
frame1.Show(1)
app.MainLoop()
