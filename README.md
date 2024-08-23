This project was created to do the combine work for ttZprime analysis. It has two functions:

1. Produce the datacards which were used for combine. These datacards include electron channel, muon channel in different widths and years. It can also merge the two channels and three years datacards 

2. Calculate the combine limits of a list of mass points and plot them. You will get the limit plots of electron channel, muon channel in different widths and years. In addition you can get their combine of two channels and three years.

You can follow these steps to do it:

# Setup the combine tool

We use the Combine v9 in CMSSW 11\_3\_X runs on slc7

```bash
cmssw-el7
cmsrel CMSSW_11_3_4
cd CMSSW_11_3_4/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
```

Update to a recommended tag - currently the recommended tag is **v9.2.0**

```bash
git fetch origin
git checkout v9.2.0
scramv1 b clean; scramv1 b # always make a clean build
```

# Creat the local working area

Copy the project in the location

```bash
cd $CMSSW_BASE/src
git clone https://github.com/xhou123/ttZprime_combine.git ttZprime_combine
cd ttZprime_combine
```

Copy the workspace root file

`cp <workspace root file> ./ST/`

`cp <workspace root file> ./ZpMass/`

# Produce the datacards and limit plots

## Produce the datacards 

`python makedatacard.py` add `-v ST` or `-v ZpMass`

`-v ST` means discrimination variable is ST, `-v ZpMass` means means discrimination variable is Z' mass

It can produce datacards in `ST/<year>/<width>/` or `ZpMass/<year>/<width>/`

## Produce the limit plots

`python plotter_combineLimit.py` add `-v ST` or `-v ZpMass`

It can produce limit plots in `limit_plots/<discrimination variable>/<year>/<width>/`












