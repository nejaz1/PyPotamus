#!/usr/bin/env python
import csv
import sys
import itertools

# Class provides dxxxxd
class TargetFile:
    currTrial = 0
    eof       = -1

    def __init__(self, filename):
        with open(filename,'r') as f:
            tgt2                  = csv.reader(f.read().splitlines(), delimiter ='\t')
            self.headers          = list(next(tgt2, None))
            self.tgt              = list(tgt2)
            TargetFile.currTrial  = 1
            self.trial()

    # method to attribute row to currTrial and header to variable
    def trial(self):
        L = self.tgt
        for i, row in enumerate(L,start=1):
            if i == TargetFile.currTrial:
                s = "currTrialStr"
                setattr(self,s,row)
                for value,index in itertools.izip(row,self.headers):
                    setattr(self,index,value)

    # method to increment the trial number
    def nextTrial(self):
        TargetFile.currTrial +=1
        self.trial()
        if TargetFile.currTrial> len(self.tgt):
            self.currTrial = self.eof
            for value in self.headers:
                setattr(self,value,self.eof)

    # method to return the number of trials
    def getTrialNum(self):
        for row, val in enumerate(self.tgt,start =1):
            L = len(self.tgt)
        print(L)

    # method to print the headers of a file
    def printHeaders(self):
        return self.headers

    # method to print the entire current trial to screen
    def printCurrTrial(self):
        print(self.headers)
        for i,row in enumerate(self.tgt, start =1):
            if i == self.currTrial:
                print row

    # method to return the entire file with trial #'s
    def printTrial(self):
        print(self.headers)
        for row in enumerate(self.tgt, start=1):
            values  = ' '.join(str(v) for v in row)
            print('Trial #%s' %(values))




