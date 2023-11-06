#!/usr/bin/env python3
import ROOT
import os

ROOT.gROOT.SetBatch(True)

ROOT.gROOT.LoadMacro("CLICdpStyle.C")
ROOT.CLICdpStyle()

ROOT.gStyle.SetOptFit(1111)
#ROOT.gStyle.SetPalette(ROOT.kRainBow)
ROOT.gStyle.SetMarkerSize(2)
ROOT.gStyle.SetMarkerStyle(33)
#ROOT.gStyle.SetMarkerStyle(ROOT.kDot)

#ParticleList = ["mu", "e", "pi"]
#ParticleList = ["mu"]
ParticleList = ["mu-", "e-"]
ThetaList = ["10", "20", "30", "40", "50", "60", "70", "80", "89"]
#ThetaList = ["80", "89"]
# MomentumList = ["1", "2", "5", "10", "20", "50", "100", "200"]
MomentumList = ["1", "2", "5", "10", "20", "50", "100"]
stackMomentumList = ["1", "10", "100"]
stackThetaList = ["10", "30", "50", "70", "89"]

title_string = {
    "p": "p [GeV]",
    "t": "#theta [#circ]",
}

def pname(particle, theta, momentum):
    return f"{particle}_{theta}deg_{momentum}GeV_1000evt"

unit_scale = {
    "delta_d0": 1e3,
    "delta_z0": 1e3,
    "delta_phi0": 1.0,
    "delta_omega": 1.0,
    "delta_tanLambda": 1.0,
    #"delta_phi": 17.4533,
    #"delta_theta": 17.4533,
    "delta_phi": 1e3,
    "delta_theta": 1e3,
    "sdelta_pt": 1.0,
    "sdelta_p": 1.0,
}

processList = {
    pname(particle, theta, momentum): {}
    for particle in ParticleList
    for theta in ThetaList
    for momentum in MomentumList
}

detectorModel = "CLD_o2_v05"

outputDir = f"Output/plots/{detectorModel}"

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

inputDir = f"Output/final/{detectorModel}"

residualList = ["d0", "z0", "phi0", "omega", "tanLambda", "phi", "theta"]
specialList = ["pt", "p"]

varList = [f"delta_{v}"
           for v in residualList] + [f"sdelta_{v}" for v in specialList]

title = {
    "delta_d0": "#sigma(#Deltad_{0})[#mum]",
    "delta_z0": "#sigma(#Deltaz_{0})[#mum]",
    "delta_phi0": "#Delta#phi_{0}",
    "delta_omega": "#Delta#Omega",
    "delta_tanLambda": "tan#Lambda",
    "delta_phi": "#sigma(#Delta#phi)[mrad]",
    "delta_theta": "#sigma(#Delta#theta)[mrad]",
    "sdelta_pt": "#sigma(#Deltap_{T}/p_{T,true}^{2})[GeV^{-1}]",
    "sdelta_p": "#sigma(#Deltap/p_{true}^{2})[GeV^{-1}]",
}

file = ROOT.TFile(f"{inputDir}/resolutions.root", "read")
#TODO: changes here
mean = {}
mean_err = {}
sigma = {}
sigma_err = {}
for p in processList:
    print(p)
    fname = f"{outputDir}/{p}.pdf"
    dir = file.Get(p)
    mean[p] = {}
    mean_err[p] = {}
    sigma[p] = {}
    sigma_err[p] = {}
    for v in varList:
        h = dir.Get(v)
        f = h.GetFunction(f"f_{p}_{v}")
        mean[p][v] = f.GetParameter(1)
        mean_err[p][v] = f.GetParError(1)
        sigma[p][v] = f.GetParameter(2)
        sigma_err[p][v] = f.GetParError(2)


# combined plots
def combined_plots(mode, particle):
    dist = {}
    dist_mode = {}
    c = ROOT.TCanvas()
    fname = f"{outputDir}/{particle}_{mode}_dist.pdf"
    c.Print(f"{fname}[")
    legend = {}
    for v in varList:
        legend[v] = ROOT.TLegend(0.6, 0.7, 0.8, 0.9)
        dist[v] = ROOT.TMultiGraph()
        dist_mode[v] = {}
        outer_list = None
        inner_list = None
        if mode == "p":
            outer_list = stackThetaList
            inner_list = MomentumList
        elif mode == "t":
            outer_list = stackMomentumList
            inner_list = ThetaList
        for o in outer_list:
            y = None
            y_err = None
            if mode == "p":
                y = ROOT.std.vector["double"](
                    (sigma[pname(particle, o, i)][v]) for i in inner_list)
                y_err = ROOT.std.vector["double"](
                    (sigma_err[pname(particle, o, i)][v]) for i in inner_list)
            elif mode == "t":
                y = ROOT.std.vector["double"](
                    (sigma[pname(particle, i, o)][v]) for i in inner_list)
                y_err = ROOT.std.vector["double"](
                    (sigma_err[pname(particle, i, o)][v]) for i in inner_list)

            x = ROOT.std.vector["double"](float(i) for i in inner_list)
            dist_mode[v][o] = ROOT.TGraphErrors(len(inner_list), x.data(), y.data(), 0, y_err.data())
            dist_mode[v][o].Scale(unit_scale[v])
            dist[v].Add(dist_mode[v][o])

            legend_string = {
                "p": f"theta = {o}#circ",
                "t": f"momentum = {o}GeV",
            }
            legend[v].AddEntry(dist_mode[v][o], legend_string[mode], "pl")

        dist[v].SetTitle(f";{title_string[mode]};{title[v]}")
        dist[v].Draw("AP5 PMC")
        legend[v].Draw()
        if mode == "p":
            c.SetLogx()

        c.SetLogy()
        c.SaveAs(f"{outputDir}/{particle}_{mode}_{v}.pdf")
        c.Print(fname)

    c.Print(f"{fname}]")

for p in ParticleList:
    combined_plots("p", p)
    combined_plots("t", p)
