import sys
import os
import glob
import string
import subprocess
import ROOT
import re
from array import array
from commands import getoutput
from argparse import ArgumentParser

mass = ['M500','M750','M1000','M1250','M1500','M1750','M2000','M2500','M3000']
Xmass = [500, 750, 1000, 1250, 1500, 1750, 2000, 2500, 3000]
width = ['W4','W10','W20','W50']
years = ['2016','2017','2018']
channels =['_mu','_e','']
xsec=[7.56e-02, 1.64e-02, 4.54e-03, 1.46e-03, 5.19e-04, 2.00e-04, 8.14e-05, 1.52e-05, 3.18e-06]

parser = ArgumentParser()
#parser.add_argument('-y', '--years', dest='years', action='store', type=str, choices=['2016', '2016APV', '2017', '2018'], default='2017')
#parser.add_argument('-c', '--channel', dest='channel', action='store', type=str, choices=['e', 'mu'], default='mu')
parser.add_argument('-v', '--variables', dest='variables', action='store', type=str, choices=['ST', 'ZpMass'], default='ST')

args = parser.parse_args()
#years = args.years
#channel = args.channel
variable = args.variables

def main():
    limit_Exp_m2s= [0.9476, 2.1573, 4.6152, 9.062, 16.3066, 30.9902, 57.1289, 218.4375, 921.7852]
    limit_Exp_m1s=  [1.2641, 2.8893, 6.206, 12.2204, 22.1707, 42.6698, 79.5806, 309.3394, 1303.1592]
    limit_Exp=[1.7578, 4.0312, 8.6875, 17.3125, 31.625, 61.5, 117.0, 466.0, 1983.0]
    limit_Exp_p1s=[2.4515, 5.6542, 12.2889, 24.6964, 45.8696, 90.1816, 175.2959, 720.4769, 3089.6052]
    limit_Exp_p2s=[3.2993, 7.6148, 16.6489, 33.7578, 63.7488, 126.8714, 252.1426, 1060.5946, 4605.7529]
    outputpath = './' 
    channel = '_mu'
    year='2016'
    widthpoint='W4'

    limit_Exp_m2s= [x * y for x, y in zip(xsec, limit_Exp_m2s)]
    limit_Exp_m1s= [x * y for x, y in zip(xsec, limit_Exp_m1s)]
    limit_Exp= [x * y for x, y in zip(xsec, limit_Exp)]
    limit_Exp_p1s= [x * y for x, y in zip(xsec, limit_Exp_p1s)]
    limit_Exp_p2s= [x * y for x, y in zip(xsec, limit_Exp_p2s)]
 
    plot_limit(outputpath, channel, Xmass, widthpoint, year, variable, xsec, limit_Exp_m2s, limit_Exp_m1s, limit_Exp, limit_Exp_p1s, limit_Exp_p2s)       


def plot_limit(OutputPath, Channel, XMass, Widthpoint, Year, Variable, Xsec, Limit_Exp_m2s, Limit_Exp_m1s, Limit_Exp, Limit_Exp_p1s, Limit_Exp_p2s):
    XMass_reverse = XMass[::-1]
    Limit_Exp_p1s_reverse = Limit_Exp_p1s[::-1]
    Limit_Exp_p2s_reverse = Limit_Exp_p2s[::-1]

    XMass_sigma = XMass + XMass_reverse
    XMass_sigma.append(XMass[0])
    Limit_1sigma = Limit_Exp_m1s + Limit_Exp_p1s_reverse    
    Limit_1sigma.append(Limit_Exp_m1s[0])
    Limit_2sigma = Limit_Exp_m2s + Limit_Exp_p2s_reverse     
    Limit_2sigma.append(Limit_Exp_m2s[0])
    WIDTH = re.findall(r'\d+', Widthpoint) 
    #print XMass_sigma
    #print Limit_1sigma
    #print Limit_2sigma
 
    #print XMass
    #print Limit_Exp


    canvas = ROOT.TCanvas("canvas", "Combine Limits", 800, 600)
    canvas.SetLogy()
    limit_exp = ROOT.TGraph(len(XMass), array('d', XMass), array('d', Limit_Exp))
    XSEC = ROOT.TGraph(len(XMass), array('d', XMass), array('d', Xsec))
    band_1s = ROOT.TGraph(len(XMass_sigma), array('d', XMass_sigma), array('d', Limit_1sigma))
    band_2s = ROOT.TGraph(len(XMass_sigma), array('d', XMass_sigma), array('d', Limit_2sigma))

    band_2s.SetLineStyle(1);
    band_2s.SetLineColor(0);
    band_2s.SetFillColor(ROOT.kOrange);
    band_2s.Draw("AF");
    band_2s.SetTitle("");
    if Variable == "ST":
      band_2s.GetXaxis().SetTitle("ST [GeV]");
    if Variable == "ZpMass":
      band_2s.GetXaxis().SetTitle("#it{m}_{Z'} [GeV]");
    band_2s.GetYaxis().SetTitle("#sigma(pp #rightarrow t#bar{t}Z') #upoint BR(Z' #rightarrow t#bar{t}) [pb]");

    band_1s.SetLineStyle(1);
    band_1s.SetLineColor(0);
    band_1s.SetFillColor(ROOT.kGreen+1);
    band_1s.Draw("LF2");
   
    limit_exp.SetLineWidth(2);
    limit_exp.SetLineStyle(2);
    limit_exp.SetMarkerSize(1.3);
    limit_exp.Draw("L");

    XSEC.SetLineColor(4);
    XSEC.SetMarkerColor(4);
    XSEC.SetLineWidth(2);
    XSEC.SetLineStyle(9);
    XSEC.Draw("L");


    pad = ROOT.TPad("pad","pad",0.01,0.01,0.99,0.99)
    ROOT.gPad.RedrawAxis()
    if Channel=='_e':
      channelText = "electron channel"
    if Channel=='_mu':
      channelText = "muon channel"
    if Channel=='':
      channelText = ""
    widthText = "#Gamma/#it{m}_{Z'}="+WIDTH[0]+"%" 
    #channelTextFont   = 42
    #channelTextSize   = 0.060
    cmsText     = "CMS"
    cmsTextFont   = 61  # default is helvetic-bold
    #writeExtraText = true
    #extraText   = "Simulation"
    #extraTextFont = 52  # default is helvetica-italics
    extraText = widthText + ' '+ channelText
    extraTextFont = 42  
    extraTextSize = 0.045  
    #text sizes and text offsets with respect to the top frame in unit of the top margin size
    lumiTextSize     = 0.7
    lumiTextOffset   = 0.2
    cmsTextSize      = 0.75
    cmsTextOffset    = 0.1  # only used in outOfFrame version
    relPosX    = 0.045
    relPosY    = 0.035
    relExtraDY = 1.2
    # ratio of "CMS" and extra text size
    extraOverCmsTextSize  = 0.65
    lumi_13TeV = "36.3 fb^{-1}"
    #lumiText += lumi_13TeV
    lumiText = Year + " (13 TeV)"
    t = pad.GetTopMargin()
    b = pad.GetBottomMargin()
    r = pad.GetRightMargin()
    l = pad.GetLeftMargin()
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(ROOT.kBlack)
    #extraTextSize = extraOverCmsTextSize*cmsTextSize
    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    latex.SetTextSize(lumiTextSize*t)
    latex.DrawLatex(1-r,0.92,lumiText)
    latex.SetTextFont(cmsTextFont)
    latex.SetTextAlign(11)
    latex.SetTextSize(cmsTextSize*t)
    latex.DrawLatex(l, 0.92,cmsText)#0.075
    latex.SetTextFont(extraTextFont)
    latex.SetTextSize(extraTextSize)
    latex.DrawLatex(0.51, 0.57, extraText) 
    #latex.DrawLatex(l+0.18, 1-t+lumiTextOffset*t-0.12,extraText)#0.075
    del pad

    widthlegend = "Theoretical #sigma, #Gamma/#it{m}_{Z'}="+WIDTH[0]+"%" 
    legend = ROOT.TLegend(0.50, 0.63, 0.88, 0.88, "95% CL upper limits")
    legend.SetTextSize(0.038)
    legend.SetFillColor(0)
    legend.SetBorderSize(0)
    legend.AddEntry(limit_exp, "Median expected", "L")
    legend.AddEntry(band_1s, "68% expected", "f")
    legend.AddEntry(band_2s, "95% expected", "f")
    legend.AddEntry(XSEC,widthlegend,"L");
    legend.Draw()

    #canvas.Draw()
    canvas.SaveAs(OutputPath + "/limitplot_"+Year+"_"+Widthpoint+Channel+".pdf")

if __name__=='__main__':
 main()
