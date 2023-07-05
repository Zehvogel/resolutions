#!/usr/bin/env python3
import ROOT
from math import ceil, floor

ROOT.gStyle.SetOptFit(1111)
ROOT.gStyle.SetPalette(ROOT.kRainBow)
ROOT.gStyle.SetMarkerSize(2)
ROOT.gStyle.SetMarkerStyle(33)

#ParticleList = ["mu", "e", "pi"]
ParticleList = ["mu"]
ThetaList = ["10", "20", "30", "40", "50", "60", "70", "80", "89"]
#ThetaList = ["80", "89"]
MomentumList = ["1", "2", "5", "10", "20", "50", "100", "200"]
stackMomentumList = ["1", "10", "100"]
stackThetaList = ["10", "30", "50", "70", "89"]

def pname(particle, theta, momentum):
    return f"{particle}_{theta}deg_{momentum}GeV_1000evt"

processList = {pname(particle, theta, momentum):{} for particle in ParticleList for theta in ThetaList for momentum in MomentumList}
#print(processList)
outputDir = "Output/final"

inputDir = "Output/stage2"

residualList = ["d0", "z0", "phi0", "omega", "tanLambda", "phi", "theta"]
specialList = ["pt", "p"]

varList = [f"delta_{v}" for v in residualList] + [f"sdelta_{v}" for v in specialList]

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

unit_scale = {
    "delta_d0": 1e3,
    "delta_z0": 1e3,
    "delta_phi0": 1.0,
    "delta_omega": 1.0,
    "delta_tanLambda": 1.0,
    "delta_phi": 1e3,
    "delta_theta": 1e3,
    "sdelta_pt": 1.0,
    "sdelta_p": 1.0,
}

df = {}
var_col_rp = {}
# get column for each variable by running event loop once
for p in processList:
    df[p] = ROOT.RDataFrame("events", f"{inputDir}/{p}.root")
    for v in specialList:
        df[p] = df[p].Define(f"sdelta_{v}", f"delta_{v} / (true_{v} * true_{v})")
    var_col_rp[p] = {}
    for v in varList:
        var_col_rp[p][v] = df[p].Take["double"](v)

var_col = {}
var_low = {}
var_high = {}
h = {}
# get bin borders and run again to make histograms
for p in processList:
    var_col[p] = {}
    var_low[p] = {}
    var_high[p] = {}
    h[p] = {}
    for v in varList:
        var_col[p][v] = sorted(var_col_rp[p][v].GetValue())
        var_low[p][v] = var_col[p][v][ceil(0.05 * len(var_col[p][v]))]
        var_high[p][v] = var_col[p][v][floor(0.95 * len(var_col[p][v]))]
        h[p][v] = (df[p]
                   .Filter(f"{v} > {var_low[p][v]} && {v} < {var_high[p][v]}")
                   .Histo1D((v, f"{p};{title[v]}", 50, var_low[p][v], var_high[p][v]), v)
                   )

# after both runs do fits and make plots
mean = {}
mean_err = {}
sigma = {}
sigma_err = {}
for p in processList:
    fname = f"{outputDir}/{p}.pdf"
    mean[p] = {}
    mean_err[p] = {}
    sigma[p] = {}
    sigma_err[p] = {}
    c = ROOT.TCanvas()
    c.Print(f"{fname}[")
    for v in varList:
        f = ROOT.TF1(f"f_{p}_{v}", "gaus", var_low[p][v], var_high[p][v])
        h[p][v].Fit(f, "RQ")
        mean[p][v] = f.GetParameter(1)
        mean_err[p][v] = f.GetParError(1)
        sigma[p][v] = f.GetParameter(2)
        sigma_err[p][v] = f.GetParError(2)
        h[p][v].Draw()
        c.Print(fname)
    c.Print(f"{fname}]")

# combined plots
p_dist = {}
p_dist_t = {}
c = ROOT.TCanvas()
fname = f"{outputDir}/p_dist.pdf"
c.Print(f"{fname}[")
legend = {}
for v in varList:
    legend[v] = ROOT.TLegend(0.6,0.7,0.8,0.9)
    p_dist[v] = ROOT.TMultiGraph()
    p_dist_t[v] = {}
    for t in stackThetaList:
        y = ROOT.std.vector["double"]((sigma[pname("mu", t, p)][v]) for p in MomentumList)
        x = ROOT.std.vector["double"](float(p) for p in MomentumList)
        p_dist_t[v][t] = ROOT.TGraph(len(MomentumList), x.data(), y.data())
        p_dist_t[v][t].Scale(unit_scale[v])
        p_dist[v].Add(p_dist_t[v][t])
        legend[v].AddEntry(p_dist_t[v][t], f"theta = {t}#circ", "pl")

    p_dist[v].SetTitle(f";p [GeV];{title[v]}")
    p_dist[v].Draw("AP PMC")
    legend[v].Draw()
    c.SetLogx()
    c.SetLogy()
    c.Print(fname)

c.Print(f"{fname}]")

t_dist = {}
t_dist_p = {}
c = ROOT.TCanvas()
fname = f"{outputDir}/t_dist.pdf"
c.Print(f"{fname}[")
legend = {}
for v in varList:
    legend[v] = ROOT.TLegend(0.6,0.7,0.8,0.9)
    t_dist[v] = ROOT.TMultiGraph()
    t_dist_p[v] = {}
    for p in stackMomentumList:
        y = ROOT.std.vector["double"]((sigma[pname("mu", t, p)][v]) for t in ThetaList)
        x = ROOT.std.vector["double"](float(t) for t in ThetaList)
        t_dist_p[v][p] = ROOT.TGraph(len(ThetaList), x.data(), y.data())
        t_dist_p[v][p].Scale(unit_scale[v])
        t_dist[v].Add(t_dist_p[v][p])
        legend[v].AddEntry(t_dist_p[v][p], f"Momentum = {p}GeV", "pl")

    t_dist[v].SetTitle(f";#theta [#circ];{title[v]}")
    t_dist[v].Draw("AP PMC")
    legend[v].Draw()
    c.SetLogy()
    c.Print(fname)

c.Print(f"{fname}]")

