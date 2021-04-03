import cv2
import numpy as np
import pytesseract as pyt

class Extractor:
	
	def __init__(self,img):
		
		self.img = img
		self.image = []
		self.greyScale = []
		self.combineDetect = []
		self.inverse = []
		self.rectangleImg = []
		self.data=[]
		self.order = []
		
	def convertToGray(self):
	
		self.image = cv2.imdecode(np.asarray(bytearray(self.img.read()), dtype="uint8"), 0)
		#self.image = cv2.imread(self.img, 0)
		convertBin, self.greyScale = cv2.threshold(self.image, 112, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		self.greyScale = 255 - self.greyScale
		
	def grapStruct(self):
	
		length = np.array(self.image).shape[1]//100

		horizontalKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (length, 1))
		horizontalDetect = cv2.erode(self.greyScale, horizontalKernel, iterations=3)
		horizontalLine = cv2.dilate(horizontalDetect, horizontalKernel, iterations=3)

		verticalKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, length))
		verticalDetect = cv2.erode(self.greyScale, verticalKernel, iterations=3)
		verticalLine = cv2.dilate(verticalDetect, verticalKernel, iterations=3)

		finalDetect = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
		self.combineDetect = cv2.addWeighted(verticalLine, 0.5, horizontalLine, 0.5, 0.0)
		self.combineDetect = cv2.erode(~self.combineDetect, finalDetect, iterations=2)
		thresh, self.combineDetect = cv2.threshold(self.combineDetect, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		convert_xor = cv2.bitwise_xor(self.image, self.combineDetect)
		self.inverse = cv2.bitwise_not(convert_xor)
	
	def makeOrder(self, hor, total, mid):
    
		order=[]
		for i in range(len(hor)):
			arrange=[]
			for k in range(total):
				arrange.append([])
			for j in range(len(hor[i])):
				sub = abs(mid-(hor[i][j][0]+hor[i][j][2]/4))
				lowest = min(sub)
				idx = list(sub).index(lowest)
				arrange[idx].append(hor[i][j])
			order.append(arrange)
		return (order)
		
	def countHorizontal(self, hor):
		
		total = 0
		for i in range(len(hor)):
			total1 = len(hor[i])
			if total1 > total:
				total = total1			
		mid = [int(hor[i][j][0]+hor[i][j][2]/2) for j in range(len(hor[i])) if hor[0]]
		mid=np.array(mid)
		mid.sort()
		return (total, mid)

	def horVer(self, boxes):
		
		dim = [boxes[i][3] for i in range(len(boxes))]
		avg = np.mean(dim)
		ver=[]
		hor=[]

		for i in range(len(boxes)):    
			if(i==0):
				ver.append(boxes[i])
				last=boxes[i]    
			else:
				if(boxes[i][1]<=last[1]+avg/2):
					ver.append(boxes[i])
					last=boxes[i]            
					if(i==len(boxes)-1):
						hor.append(ver)        
				else:
					hor.append(ver)
					ver=[]
					last = boxes[i]
					ver.append(boxes[i])
		return (hor)

	def getBoxes(self, num, method="left-to-right"):
	
		invert = False
		flag = 0
		
		if method == "right-to-left" or method == "bottom-to-top":
			invert = True

		if method == "top-to-bottom" or method == "left-to-right":
			flag = 1

		boxes = [cv2.boundingRect(c) for c in num]
		(num, boxes) = zip(*sorted(zip(num, boxes), key = lambda b:b[1][flag], reverse=invert))
		return (num, boxes)

	def makedict(self, ocr):

		ocrlist = ocr.split('\n')
		ocrlist = [i for i in ocrlist if i]
		if len(ocrlist) == 0:
			return
		tmp = ocrlist[0].split('-')
		test = ()
		if len(tmp) == 1:
			if len(ocrlist) == 2:
				test=(ocrlist[0].strip(),'All',ocrlist[1].strip())
				if test not in self.data and test != ():
					self.data.append(test)
		elif len(tmp) == 4:
			for i in ocrlist:
				var = i.split('-')
				test=(var[1].strip(),(var[0].strip())[1],var[2].strip())
				if test not in self.data and test != ():
					self.data.append(test)


	def extractData(self, order):

		order.pop(0)
		for i in range(len(order)):
			for j in range(len(order[i])):
				for k in range(len(order[i][j])):
					side1,side2,width,height = order[i][j][k][0],order[i][j][k][1],order[i][j][k][2],order[i][j][k][3]
					finalExtract = self.inverse[side2:side2+height, side1:side1+width]
					finalKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
					getBorder = cv2.copyMakeBorder(finalExtract,2,2,2,2, cv2.BORDER_CONSTANT,value=[255,255])
					resize = cv2.resize(getBorder, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
					dil = cv2.dilate(resize, finalKernel,iterations=1)
					ero = cv2.erode(dil, finalKernel,iterations=1)
					ocr = pyt.image_to_string(ero)
					if(len(ocr)==0):
						ocr = pyt.image_to_string(ero, config='--psm 3')
					ocr = ocr.replace("\x0c","")
					ocr = ocr.upper()
					self.makedict(ocr)
						
	
	def detectBoxAndExtract(self):
		
		cont, _ = cv2.findContours(self.combineDetect, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		cont,boxes = self.getBoxes(cont, method="top-to-bottom")

		finalBox = []
		for c in cont:
			s1, s2, s3, s4 = cv2.boundingRect(c)
			if (s3<1000 and s4<500):
				self.rectangleImg = cv2.rectangle(self.image,(s1, s2), (s1+s3, s2+s4),(0, 255,0),2)
				finalBox.append([s1,s2,s3,s4])
		
		hor = self.horVer(boxes)
		total, mid = self.countHorizontal(hor)
		order = self.makeOrder(hor, total, mid)
		
		self.extractData(order)
				
	def printData(self):
		
		print("\nTime Table data:- ")
		for i in self.data:
			print(i)	
			
	def getData(self):
		
		return self.data
