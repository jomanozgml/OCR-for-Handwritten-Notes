# -*- coding: utf-8 -*-
import os
#Importing all from Tkinter for GUI
from Tkinter import *
#Importing openFileDialog and saveFileDialog
from tkFileDialog import *
from tkMessageBox import *
import PIL
from PIL import Image, ImageTk
import shutil
import numpy as np
import cv2

filepath, tifFilePath, lan, font, homeImage = None, None, None, None, None
flag, w, h, angle, refresh_flag = 0, 0, 0, 0, 0

#Button click event for Open File Button
def openFile(option):
	global filepath, w, h, angle, refresh_flag, homeImage
	rotation_flag = 1
		
	if option == 0:
		rotation_flag = 0
		filepath = askopenfilename()
		
	elif option == 1:
		angle = 270
	elif option == 2:
		angle = 90
	elif option == 3:
		angle = 180
	elif option == 4:
		window.lower()
		angle = int(raw_input("\nEnter Desired Angle for Rotation: "))
		window.lift()
		# if refresh_flag == 0
			# angleWindow = Toplevel(window)
			# def setAngle():
				# strangle = entry1.get()
				# angle = int(strangle)
				# print angle
				# # orimg = Image.open(filepath)
				# # rotImg = orimg.rotate(angle, expand=1)
				# # rotImg.save(filepath)
				# angleWindow.destroy()
				
			# angleWindow.geometry("300x200")
					
			# label1 = Label(angleWindow, text = "Enter Arbitrary Angle")
			# label1.pack(side = LEFT)
		
			# entry1 = Entry(angleWindow, bd = 2)
			# entry1.pack(side = LEFT)
			
			# refresh_flag == 1
			
			# button1 = Button(angleWindow, text = "Done", command = setAngle)
			# button1.pack(padx = 5, pady = 5, side = BOTTOM)
						
	if rotation_flag:
		orimg = Image.open(filepath)
		rotImg = orimg.rotate(angle, expand=1)
		rotImg.save(filepath)
				
	picture = Image.open(filepath)
	width, height = picture.size
	ratio1 = 1.0 * 500 / width
	ratio2 = 1.0 * 500 / height
	ratio = min(ratio1, ratio2)
	w = int(width * ratio)
	h = int(height * ratio)
	res = picture.resize((w, h), Image.ANTIALIAS)
	homeImage.pack_forget()
	showImage.img = ImageTk.PhotoImage(res)
	showImage.config(width = w, height = h, image = showImage.img)
	
#Button click event for OCR Button	
def recognize():
	language = "eng"
	# if lang.get() == "OurNepali":
		# language = "nep"
	if lang.get() == "Nepali":
		language = "hin"
	elif lang.get() == "Custom":
		language = "man"
	img = cv2.imread(filepath, 0)
	noiselessImg = cv2.fastNlMeansDenoising(img, None, 15, 7, 21)
	#image sharpening
	#kernel_sharpen = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
	kernel_sharpen = np.array([[-1,-1,-1,-1,-1],
                             [-1,2,2,2,-1],
                             [-1,2,8,2,-1],
                             [-1,2,2,2,-1],
                             [-1,-1,-1,-1,-1]]) / 8.0
	#sharpImg = cv2.filter2D(noiselessImg, -1, kernel_sharpen)
	
	ret, binaryImg = cv2.threshold(noiselessImg, 127, 255, cv2.THRESH_BINARY)
	sharperImg = cv2.filter2D(binaryImg, -1, kernel_sharpen)
	ret, invBinaryImg = cv2.threshold(sharperImg, 127, 255, cv2.THRESH_BINARY_INV)
	cv2.imwrite('temp.jpg', noiselessImg)
	#cmd = "tesseract \"%s\" output_text -l %s" %(filepath, language)
	cmd = "tesseract temp.jpg output_text -l %s" %language
	os.system(cmd)
	
   	#Output text printing on GUI
	file = open("output_text.txt")
	read_file = (file.read()).split()
	print_text = " ".join(read_file)
	outputText.insert(INSERT, print_text)
	file.close()
	os.remove('temp.jpg')
	res_noiselessImg = resize(noiselessImg)
	#res_sharpImg = resize(sharpImg)
	res_binaryImg = resize(binaryImg)
	res_sharperImg = resize(sharperImg)
	res_invBinaryImg = resize(invBinaryImg)
	cv2.imshow('Noise Removed Image', res_noiselessImg)
	#cv2.imshow('Sharp Image', res_sharpImg)
	cv2.imshow('Binarised Image', res_binaryImg)
	cv2.imshow('Sharper Image', res_sharperImg)
	cv2.imshow('Inverse Binarised Image', res_invBinaryImg)
	cv2.waitKey(0)                      # wait for user key press
	cv2.destroyAllWindows()             # remove windows from memory
	

def resize(image):
	return cv2.resize(image, (w, h), interpolation = cv2.INTER_CUBIC)


#Button click event for Save File Button
def saveFile():
	save_file = asksaveasfile(mode = 'w', defaultextension = '.txt')
	get_text = outputText.get(1.0, "end-1c")
	get_text = get_text.encode('utf-8')
	save_file.write(get_text)
	save_file.close()


def train(option):
	if option == 1:			#makeBox
		def tifPath():
			global lan, font, tifFilePath
			lan = entry1.get()
			font = entry2.get()
			tifFilePath = askopenfilename()
			window.lower()
								
		def boxGeneration():
			# rename = "rename-item 'tifFilePath' '%s.%s.exp0.tif'" %(lan, font)
			# os.system(rename)
			shutil.copy(tifFilePath, '%s.%s.exp0.tif' %(lan, font))
			cmnd = "tesseract %s.%s.exp0.tif %s.%s.exp0 batch.nochop makebox" %(lan, font, lan, font)
			os.system(cmnd)
			subWindow.destroy()
			openBox = "python pytrainer.py %s.%s.exp0.tif" %(lan, font)
			os.system(openBox)
			
		subWindow = Tk()
		subWindow.title("Make Box File")
		subWindow.geometry("400x300")
		subWindow.wm_iconbitmap('logo.ico')
				
		label1 = Label(subWindow, text = "Enter Language Code")
		label1.pack(pady = 10, side = TOP)
		
		entry1 = Entry(subWindow, bd = 5)
		entry1.pack(side = TOP)
				
		label2 = Label(subWindow, text = "Enter Font Code")
		label2.pack(pady = 20, side = TOP)
		
		entry2 = Entry(subWindow, bd = 5)
		entry2.pack(side = TOP)
				
		openTif = Button(subWindow, text = "Open TIF File", command = tifPath)
		openTif.pack(pady = 20, side = TOP)
		
		genBox = Button(subWindow, text = "Generate Box File", command = boxGeneration)
		genBox.pack(pady = 20, side = BOTTOM)
		subWindow.mainloop()
	
	elif option == 2:		#editBox
		os.system("python pytrainer.py")
	
	elif option == 3:		#train
		os.system("SerakTesseractTrainer.exe")


def aboutInfo():
	#showinfo("Developers", "Ganesh Raj Manadhar\nManraj Thapa\nManoj Shrestha\nNitesh Manandhar")
	aboutWindow = Toplevel()
	aboutWindow.title("Developers")
	aboutWindow.wm_iconbitmap('logo.ico')
	pic = Image.open("about1.jpg")
	
	aboutImage = Label(aboutWindow)
	aboutImage.img = ImageTk.PhotoImage(pic)
	aboutImage.config(width = 500, height = 500, image = aboutImage.img)
	aboutImage.pack(side = TOP)

	
#Main window creation
window = Tk()
window.title("Nepali-OCR")
window.geometry("900x600")
window.wm_iconbitmap('logo.ico')

#Home image

homeImg = Image.open("home.jpg")
homeImage = Label(window)
homeImage.img = ImageTk.PhotoImage(homeImg)
homeImage.config(width = 900, height = 600, image = homeImage.img)
homeImage.pack(side = TOP)
	
#Menubar creation
menubar = Menu(window)
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label = "Open Image File", command = lambda: openFile(0))
filemenu.add_command(label = "Save Text File", command = saveFile)
filemenu.add_separator()
filemenu.add_command(label = "Exit", command = window.destroy)
menubar.add_cascade(label = "File", menu = filemenu)

trainmenu = Menu(menubar, tearoff = 0)
trainmenu.add_command(label = "Make Box File", command = lambda: train(1))
trainmenu.add_command(label = "Edit Box File", command = lambda: train(2))
trainmenu.add_command(label = "Train", command = lambda: train(3))
menubar.add_cascade(label = "Train", menu = trainmenu)

rotatemenu = Menu(menubar, tearoff = 0)
rotatemenu.add_command(label = "Rotate Clockwise [90 degree]", command = lambda: openFile(1))
rotatemenu.add_command(label = "Rotate Counter-Clockwise [90 degree]", command = lambda: openFile(2))
rotatemenu.add_command(label = "Rotate 180 degree", command = lambda: openFile(3))
rotatemenu.add_command(label = "Rotate to Arbitrary angle", command = lambda: openFile(4))
menubar.add_cascade(label = "Rotate", menu = rotatemenu)

helpmenu = Menu(menubar, tearoff = 0)
helpmenu.add_command(label = "About", command = aboutInfo)
menubar.add_cascade(label = "Help", menu = helpmenu)
window.config(menu = menubar)

#OCR Button widget
recognize = Button(window, text = "Start OCR", command = recognize)
recognize.pack(pady = 10, side = BOTTOM)

#Option Menu widget
lang = StringVar(window)
lang.set("Select Language")
optMenu = OptionMenu(window, lang, "English", "Nepali", "Custom")
optMenu.pack(side = BOTTOM)

# Label widget
showImage = Label(window)
showImage.pack(side = LEFT)

#Text widget
outputText = Text(window, width = 150, height = 150, wrap = "word")
outputText.pack(padx = 10, pady = 10, side = LEFT)

window.mainloop()