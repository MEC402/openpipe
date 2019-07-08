#sequence clmyss for compressing strings of numbers
# for compact representation of sequences
import re

class sequence:

    def __init__(self):
        self.numlist = [];
        self.seqlist = [];


    def addNum(self, anum):
#        print("AddNum");
#print (anum);
        self.numlist.append(anum);

    def printSeq(self):
        #print(len(self.imglist));
        self.compressNumList();
#        for ai in self.numlist:
#            print(ai);
        print("sequence");
        for ani in self.seqlist:
#            print("GODJAS");
            print(ani);

    def fromString(self,astring):
        stolist = re.findall('\d+',astring);
        istart = int(stolist[0]);
        iend = int(stolist[1])+1;
        self.numlist = list(range(istart,iend));

    def toString(self):
        #print(len(self.imglist));
        self.compressNumList();
#        for ai in self.numlist:
#            print(ai);
        print("sequence");
        for ani in self.seqlist:
#            print("GODJAS");
            print(ani);
        return '^'.join("(%s,%s)" % tup for tup in self.seqlist);

#if I was smarter I would document this better
    def compressNumList(self):
        #compress a sequence of numbers into a compact list representation
        numstart = self.numlist[0];
        numend = numstart;
        count = 1;
        numcur = numstart;
        if len(self.numlist) == 1:
            self.seqlist.append((numstart,numstart));
            return;
        elif len(self.numlist) == 2:
            self.seqlist.append((numstart,self.numlist[1]));
            return;

        while count < len(self.numlist)-1:
           #print (count, numcur, self.numlist[count-1]);
           while count <= len(self.numlist) and numcur  == self.numlist[count-1]:
               numend = numcur;
               numcur += 1;
               count += 1;
           #print (count, numcur, numend);
           self.seqlist.append((numstart,numend));
           if count < len(self.numlist)-1:
              numstart=self.numlist[count-1];
              numend = numstart;
              numcur = numstart;


#mys = sequence();
#mys.addNum(1);
#mys.addNum(2);
#mys.addNum(3);
#mys.addNum(4);
#mys.addNum(5);
#mys.addNum(7);
#mys.addNum(8);
#mys.addNum(9);
#mys.addNum(10);
#mys.addNum(11);

#mys.printSeq();
