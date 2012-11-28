
import cStringIO
import urllib2
import urllib
import simplejson
import wx
import cv2.cv as cv
import sys

class Panel1(wx.Panel):

    def __init__(self, parent, id):
        # create the panel
        wx.Panel.__init__(self, parent, id)
        self.btn = wx.Button(self, label="Search", pos=(390, 500))
        self.btn.Bind(wx.EVT_BUTTON, self.buttonClick)
        self.control = wx.TextCtrl(self, size=(350, 30), pos=(20, 500))

    def buttonClick(self, event): 
        search_string = self.control.GetValue()
        url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='+search_string+'&userip=INSERT-USER-IP')
        request = urllib2.Request(url, None, {'Referer': 'google.com'})
        response = urllib2.urlopen(request)
        results = simplejson.load(response)
        filedata = urllib2.urlopen(results['responseData']['results'][1]['unescapedUrl']).read()
        #Display original image    
        stream = cStringIO.StringIO(filedata)
        bmp = wx.BitmapFromImage(wx.ImageFromStream(stream))
        wx.StaticBitmap(self, -1, bmp, (5, 5), (450, 480))        
        #OpenCV processing below
        imagefiledata = cv.CreateMatHeader(1, len(filedata), cv.CV_8UC1)
        cv.SetData(imagefiledata, filedata, len(filedata))
        im = cv.DecodeImage(imagefiledata, cv.CV_LOAD_IMAGE_COLOR)                 
        gray = cv.CreateImage((im.width, im.height), 8, 1)
        edge = cv.CreateImage((im.width, im.height), 8, 1)        
        im_bw1 = cv.CreateImage((im.width, im.height), 8, 1)
        cv.CvtColor(im, gray, cv.CV_BGR2GRAY)    
        cv.Not(gray, edge)
        cv.Canny(gray, edge, 125, 125 * 3, 3)                  
        cv.SaveImage("edge_image.png", edge)     
        #Display sketchhi5'ed image    
        jpg1 = wx.Image('edge_image.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(self, -1, jpg1, (500, 5), (450, 480))
        
    
wx.InitAllImageHandlers()
app = wx.PySimpleApp()
frame1 = wx.Frame(None, -1, "Sketch-hi-5", size = (1000, 600))
Panel1(frame1,-1)
frame1.Show(1)
app.MainLoop()
