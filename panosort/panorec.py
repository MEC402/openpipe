#panorec.py -- define python code for panorama records

import imgoverlap;
#import pyseq;
import sequence;
import csv;

class panoRec:


    def __init__(self,aid):
        self.imglist = [];
        self.myseq = sequence.sequence();
        self.myid = aid;
        self.stereopair = -1;

    def inPano(self,animage):
         #compare animage to limg to see if is in panorama object
         ovrlap = imgoverlap.chkOverlapTime(animage,self.curimage);
         print(ovrlap);
         return ovrlap;

    def addImage(self, animage,afindex ):
        self.imglist.append(animage);
        self.curimage = animage;
        self.myseq.addNum(afindex);

    def panoLength(self):
        return len(self.myseq.numlist);

    def printRec(self):
        #print(len(self.imglist));
        #print (self.myseq.format('%s %h%p%t %R'));
        self.myseq.printSeq()
        for ai in self.imglist:
             print(ai);
    def fromList(self, arow):
        print (arow);
        self.myid = arow[0];
        self.myseq = sequence.sequence();
        self.myseq.fromString(arow[1]);
        self.stereopair = arow[2];

    def minIndex(self):
         return 0;

    def maxIndex(self):
         return 0;

    def outRec(self,awriter):
        #print(len(self.imglist));
        #print (self.myseq.format('%s %h%p%t %R'));
        fullrec = [];
        fullrec.append(self.myid);
        fullrec.append(self.myseq.toString());
        fullrec.append(len(self.myseq.numlist));
        fullrec.append(self.stereopair);
        for ai in self.imglist:
             print(ai);
        awriter.writerow(fullrec);

    def consolidatePanoRec(self):
        #print("Compress the file sequences into a shorened series");
        #self.myseq = pyseq.Sequence(self.imglist.copy());
        a=1;
