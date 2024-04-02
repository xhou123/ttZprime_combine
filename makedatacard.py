import sys
import os
import glob
import string
import subprocess
import ROOT
from commands import getoutput
from argparse import ArgumentParser

hist = ['TTZprime','ttbar','t_tt_X','tttt','others']
mass = ['M500','M750','M1000','M1250','M1500','M1750','M2000','M2500','M3000','M4000']
width = ['W4','W10','W20','W50']
years = ['2016','2017','2018']
channels =['mu','e']


parser = ArgumentParser()
#parser.add_argument('-y', '--years', dest='years', action='store', type=str, choices=['2016', '2016APV', '2017', '2018'], default='2017')
#parser.add_argument('-c', '--channel', dest='channel', action='store', type=str, choices=['e', 'mu'], default='mu')
parser.add_argument('-v', '--variables', dest='variables', action='store', type=str, choices=['ST', 'ZpMass'], default='ST')

args = parser.parse_args()
#years = args.years
#channel = args.channel
variable = args.variables

path_fw = os.environ['CMSSW_BASE']+"/src/ttZprime_combine"
workspace_path = path_fw +"/"+variable

def main():
 os.chdir(path_fw)
 CreatDirectory(workspace_path)
 os.chdir(workspace_path)
 # creat datacards of different channel in each year
 for i in range(len(years)):
   for j in range(len(width)):
     card_path = workspace_path + "/" + years[i] + "/" + width[j]
     CreatDirectory(card_path)
     os.chdir(card_path)
     for k in range(len(mass)):
       for channel in channels:
         cardname = "datacard_ttZprime_" + channel + "_" + mass[k]
         WriteDatacard(cardname, workspace_path, variable, years[i], channel, hist, width[j], mass[k])
     #creat combine datacards of different channel in each year
     CombineChannel(card_path, mass)
 #creat combine datacards of different years
 CombineRun2(workspace_path, mass, width)

def WriteDatacard(Filename, Path, Variable, Year, Channel, Hist, Width, Mass):
    datacard = file(Filename+".txt","w")
    if Year == "2016" :
       print >> datacard, "imax 2"
       print >> datacard, "jmax *"
       print >> datacard, "kmax *"
       print >> datacard, "----------------------------"
       print >> datacard, "shapes * cat0 %s/workspace_%s_%s.root $PROCESS $PROCESS_$SYSTEMATIC" % (Path,Year,Channel)
       print >> datacard, "shapes * cat1 %s/workspace_%sAPV_%s.root $PROCESS $PROCESS_$SYSTEMATIC" % (Path,Year,Channel)
       print >> datacard, "----------------------------"
       print >> datacard, "bin  cat0  cat1"
       print >> datacard, "observation  -1  -1"
       print >> datacard, "----------------------------"
       print >> datacard, "bin  cat0  cat0  cat0  cat0  cat0  cat1  cat1  cat1  cat1  cat1"
       print >> datacard, "process  %s_%s%s  %s  %s  %s  %s  %s_%s%s  %s  %s  %s  %s" % (Hist[0],Mass,Width,Hist[1],Hist[2],Hist[3],Hist[4],Hist[0],Mass,Width,Hist[1],Hist[2],Hist[3],Hist[4])
       print >> datacard, "process  0  1  2  3  4  0  1  2  3  4"
       print >> datacard, "rate  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1"
       print >> datacard, "----------------------------"
       print >> datacard, "lumi_%s lnN 1.025 - - - - 1.025 - - - -" % (Year)
       print >> datacard, "cat0  autoMCStats 0 0 1"
       print >> datacard, "cat1  autoMCStats 0 0 1"
    if Year == "2017" :
       print >> datacard, "imax 1"
       print >> datacard, "jmax *"
       print >> datacard, "kmax *"
       print >> datacard, "----------------------------"
       print >> datacard, "shapes * cat0 %s/workspace_%s_%s.root $PROCESS $PROCESS_$SYSTEMATIC" % (Path,Year,Channel)
       print >> datacard, "----------------------------"
       print >> datacard, "bin  cat0"
       print >> datacard, "observation  -1"
       print >> datacard, "----------------------------"
       print >> datacard, "bin  cat0  cat0  cat0  cat0  cat0"
       print >> datacard, "process  %s_%s%s  %s  %s  %s  %s" % (Hist[0],Mass,Width,Hist[1],Hist[2],Hist[3],Hist[4])
       print >> datacard, "process  0  1  2  3  4"
       print >> datacard, "rate  -1  -1  -1  -1  -1"
       print >> datacard, "----------------------------"
       print >> datacard, "lumi_%s lnN 1.023 - - - -" % (Year)
       print >> datacard, "cat0  autoMCStats 0 0 1"
    if Year == "2018" :
       print >> datacard, "imax 1"
       print >> datacard, "jmax *"
       print >> datacard, "kmax *"
       print >> datacard, "----------------------------"
       print >> datacard, "shapes * cat0 %s/workspace_%s_%s.root $PROCESS $PROCESS_$SYSTEMATIC" % (Path,Year,Channel)
       print >> datacard, "----------------------------"
       print >> datacard, "bin  cat0"
       print >> datacard, "observation  -1"
       print >> datacard, "----------------------------"
       print >> datacard, "bin  cat0  cat0  cat0  cat0  cat0"
       print >> datacard, "process  %s_%s%s  %s  %s  %s  %s" % (Hist[0],Mass,Width,Hist[1],Hist[2],Hist[3],Hist[4])
       print >> datacard, "process  0  1  2  3  4"
       print >> datacard, "rate  -1  -1  -1  -1  -1"
       print >> datacard, "----------------------------"
       print >> datacard, "lumi_%s lnN 1.025 - - - -" % (Year)
       print >> datacard, "cat0  autoMCStats 0 0 1"

def CreatDirectory(path):
    if not os.path.exists(path):
     os.makedirs(path)
     print("%s created successfully" % path)
    else:
     print("%s already exist" % path)

def CombineChannel(Card_path, Mass):
    os.chdir(Card_path)
    shname = "combine_channel.sh"
    shFile = file(shname,"w")
    print >> shFile, "#!/bin/bash"
    for Masspoint in Mass:
      print >> shFile, "combineCards.py mu=datacard_ttZprime_mu_%s.txt e=datacard_ttZprime_e_%s.txt > datacard_ttZprime_%s.txt" % (Masspoint, Masspoint, Masspoint)  
      os.system("combineCards.py mu=datacard_ttZprime_mu_%s.txt e=datacard_ttZprime_e_%s.txt > datacard_ttZprime_%s.txt" % (Masspoint, Masspoint, Masspoint))
    #os.system("source %s/%s" % (Card_path, shname))
    #process = subprocess.Popen(["bash","combine_channel.sh"])  
    #process.wait()
    print "combine cards finish"
 
def CombineRun2(Workspace_path, Mass, Width):
    for Widthpoint in Width:
      Run2_datacard_path = Workspace_path + "/" + "Run2/" + Widthpoint 
      CreatDirectory(Run2_datacard_path)
      shFile_mu = file(Run2_datacard_path + "/combine_Run2_mu.sh","w")
      shFile_e  = file(Run2_datacard_path + "/combine_Run2_e.sh","w")
      shFile    = file(Run2_datacard_path + "/combine_Run2.sh","w")
      for Masspoint in Mass:
        print >> shFile_mu, "combineCards.py Run2016=%s/2016/%s/datacard_ttZprime_mu_%s.txt Run2017=%s/2017/%s/datacard_ttZprime_mu_%s.txt Run2018=%s/2018/%s/datacard_ttZprime_mu_%s.txt > %s/datacard_ttZprime_mu_%s.txt" % (Workspace_path,Widthpoint,Masspoint,Workspace_path,Widthpoint,Masspoint,Workspace_path,Widthpoint,Masspoint,Run2_datacard_path,Masspoint)
        print >> shFile_e, "combineCards.py Run2016=%s/2016/%s/datacard_ttZprime_e_%s.txt Run2017=%s/2017/%s/datacard_ttZprime_e_%s.txt Run2018=%s/2018/%s/datacard_ttZprime_e_%s.txt > %s/datacard_ttZprime_e_%s.txt" % (Workspace_path,Widthpoint,Masspoint,Workspace_path,Widthpoint,Masspoint,Workspace_path,Widthpoint,Masspoint,Run2_datacard_path,Masspoint)
        print >> shFile, "combineCards.py Run2016=%s/2016/%s/datacard_ttZprime_%s.txt Run2017=%s/2017/%s/datacard_ttZprime_%s.txt Run2018=%s/2018/%s/datacard_ttZprime_%s.txt > %s/datacard_ttZprime_%s.txt" % (Workspace_path,Widthpoint,Masspoint,Workspace_path,Widthpoint,Masspoint,Workspace_path,Widthpoint,Masspoint,Run2_datacard_path,Masspoint)
        os.system("combineCards.py Run2016=%s/2016/%s/datacard_ttZprime_mu_%s.txt Run2017=%s/2017/%s/datacard_ttZprime_mu_%s.txt Run2018=%s/2018/%s/datacard_ttZprime_mu_%s.txt > %s/datacard_ttZprime_mu_%s.txt" % (Workspace_path,Widthpoint,Masspoint,Workspace_path,Widthpoint,Masspoint,Workspace_path,Widthpoint,Masspoint,Run2_datacard_path,Masspoint))
        os.system("combineCards.py Run2016=%s/2016/%s/datacard_ttZprime_e_%s.txt Run2017=%s/2017/%s/datacard_ttZprime_e_%s.txt Run2018=%s/2018/%s/datacard_ttZprime_e_%s.txt > %s/datacard_ttZprime_e_%s.txt" % (Workspace_path,Widthpoint,Masspoint,Workspace_path,Widthpoint,Masspoint,Workspace_path,Widthpoint,Masspoint,Run2_datacard_path,Masspoint))
        os.system("combineCards.py Run2016=%s/2016/%s/datacard_ttZprime_%s.txt Run2017=%s/2017/%s/datacard_ttZprime_%s.txt Run2018=%s/2018/%s/datacard_ttZprime_%s.txt > %s/datacard_ttZprime_%s.txt" % (Workspace_path,Widthpoint,Masspoint,Workspace_path,Widthpoint,Masspoint,Workspace_path,Widthpoint,Masspoint,Run2_datacard_path,Masspoint))
      print "combine cards finish"

if __name__=='__main__':
 main()
