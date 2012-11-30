import cStringIO
import urllib2
import urllib
import simplejson
import wx
import cv2.cv as cv
import sys
import os
import Image

class Panel1(wx.Panel):

#Create the panel, search box and search button
    def __init__(self, parent, id):        
        wx.Panel.__init__(self, parent, id)
        self.btn = wx.Button(self, label="Search", pos=(390, 500))
        self.btn.Bind(wx.EVT_BUTTON, self.searchButtonClick)
        self.control = wx.TextCtrl(self, size=(350, 30), pos=(20, 500))

#Call Google API and retrieve images. Create bitmapbutton controls and display the images. Set onImageClick bindings
    def searchButtonClick(self, event): 
        search_string = self.control.GetValue()
        url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='+search_string+'&userip=INSERT-USER-IP')
        request = urllib2.Request(url, None, {'Referer': 'google.com'})
        response = urllib2.urlopen(request)
        results = simplejson.load(response)
        for i in range(0,3):
            filedata = urllib2.urlopen(results['responseData']['results'][i]['unescapedUrl']).read()                   
            stream = cStringIO.StringIO(filedata)
            image = wx.ImageFromStream(stream)
            resizedimage = image.Scale(200, 200, wx.IMAGE_QUALITY_HIGH)
            bmp = wx.BitmapFromImage(resizedimage)       
            bitmapbutton=wx.BitmapButton(self,-1,bmp, (5 + i*200,5))
            bitmapbutton.Bind(wx.EVT_LEFT_DOWN, lambda event, arg=i: self.onImageClick(event, arg))
            bmp.SaveFile("Image"+str(i)+".bmp",wx.BITMAP_TYPE_BMP)

#Do image processing and show result         
    def onImageClick(self,event,arg):        
        #Do Image Processing
        im=cv.LoadImage("Image"+str(arg)+".bmp", cv.CV_LOAD_IMAGE_COLOR)             
        gray = cv.CreateImage((im.width, im.height), 8, 1)
        edge = cv.CreateImage((im.width, im.height), 8, 1)        
        im_bw1 = cv.CreateImage((im.width, im.height), 8, 1)
        cv.CvtColor(im, gray, cv.CV_BGR2GRAY)    
        cv.Not(gray, edge)
        cv.Canny(gray, edge, 125, 125 * 3, 3)                  
        cv.SaveImage("edge_image.png", edge)       
        jpg1 = wx.Image('edge_image.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        bitmapbutton=wx.BitmapButton(self,-1,jpg1, (200,250))
        os.remove("edge_image.png")
    
    
wx.InitAllImageHandlers()
app = wx.PySimpleApp()
frame1 = wx.Frame(None, -1, "Sketch-hi-5", size = (700, 550))
Panel1(frame1,-1)
frame1.Show(1)
app.MainLoop()
