# coding=utf-8
import win32gui
import win32con
import win32api
import os
import sys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class NoteWallpaper(object):
	"""
	eq:NoteWallpaper(text,imgpath).setWallpaper()
	text:设置文本
	imgpath:设置壁纸路径（默认"C:\wallpaper\book.bmp"）
	"""
	def __init__(self,text,imgpath="C:\\wallpaper\\book.bmp"):
		self.text=text.split("\n")
		self.imgpath=imgpath
		
	def setWallpaper(self,fontsize=22,verticalspacing=26,leftmargin=800):   
	    if self.__setimage(fontsize,verticalspacing,leftmargin)=="FilePathError":
	    	return "FilePathError"
	    k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)  
	    win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2")  
	    win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")  
	    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, self.wallpaperpath, 1+2) 

	def __setimage(self,fontsize,verticalspacing,leftmargin):
		
		try:
			img=Image.open(self.imgpath)
		except IOError:
			return "FilePathError"
		a=ImageDraw.Draw(img)
		font = ImageFont.truetype ("YaHei.Consolas.1.11b.ttf",fontsize)
		if self.text!=[""]:
			for row,t in enumerate(self.text):
				a.text((img.size[0]-leftmargin,row*verticalspacing),t,fill=(255,255,255,128),font=font)
		self.wallpaperpath=os.path.join(os.path.dirname(self.imgpath),"notewallpaper.bmp")
		img.save(self.wallpaperpath)

if __name__ == "__main__":
    text=""
    NoteWallpaper(text).setWallpaper()
