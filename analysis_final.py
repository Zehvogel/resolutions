#!/usr/bin/env python3
import ROOT
from math import ceil, floor
import numpy as np
import os

ROOT.gROOT.SetBatch(True)

ROOT.gStyle.SetOptFit(1111)
ROOT.gStyle.SetPalette(ROOT.kRainBow)
ROOT.gStyle.SetMarkerSize(2)
ROOT.gStyle.SetMarkerStyle(33)
# ROOT.gStyle.SetMarkerStyle(ROOT.kDot)

# ParticleList = ["mu", "e", "pi"]
ParticleList = ["mu-", "e-"]
# ParticleList = ["mu"]
# ParticleList = ["e-"]
ThetaList = ["10", "20", "30", "40", "50", "60", "70", "80", "89"]
# ThetaList = ["10", "20"]
# ThetaList = ["89"]
# MomentumList = ["1", "2", "5", "10", "20", "50", "100", "200"]
MomentumList = ["1", "2", "5", "10", "20", "50", "100"]
stackMomentumList = ["1", "10", "100"]
stackThetaList = ["10", "30", "50", "70", "89"]


def pname(particle, theta, momentum):
    return f"{particle}_{theta}deg_{momentum}GeV_1000evt"


# len(edges) == len(counts) + 1
def make_bins(edges, counts):
    res = []
    for i in range(len(counts)):
        dist = edges[i + 1] - edges[i]
        inc = dist / counts[i]
        res.extend([edges[i] + j * inc for j in range(counts[i])])
    return res


processList = {
    pname(particle, theta, momentum): {}
    for particle in ParticleList
    for theta in ThetaList
    for momentum in MomentumList
}
# print(processList)

# detectorModel = "CLD_o2_v05"
detectorModel = "FCCee_o1_v04"

outputDir = f"Output/final/{detectorModel}"

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

inputDir = f"Output/stage2/{detectorModel}"

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
        # TODO: calculate special bins here
        bins = (50, var_low[p][v], var_high[p][v])
        if p.startswith("e") and v in ["delta_omega", "sdelta_pt", "sdelta_p"]:
            low = var_low[p][v]
            high = var_high[p][v]
            dist = high - low
            special_bins = make_bins(
                [low, low + 0.7 * dist, low + 0.8 * dist, low + 0.9 * dist, high],
                [1, 2, 3, 25],
            )
            bins = (len(special_bins) - 1, np.asarray(special_bins))
        h[p][v] = (
            df[p]
            .Filter(f"{v} > {var_low[p][v]} && {v} < {var_high[p][v]}")
            .Histo1D((v, f"{p};{title[v]}", *bins), v)
        )

# after both runs do fits and make plots
outfile = ROOT.TFile(f"{outputDir}/resolutions.root", "recreate")
for p in processList:
    dir = outfile.mkdir(p)
    dir.cd()
    # fname = f"{outputDir}/{p}.pdf"
    c = ROOT.TCanvas()
    # c.Print(f"{fname}[")
    for v in varList:
        f = None
        # scale histogram bins here
        h[p][v].Scale(1, "width")
        if p.startswith("e") and v in ["delta_omega", "sdelta_pt", "sdelta_p"]:
            f = ROOT.TF1(
                f"f_{p}_{v}",
                "ROOT::Math::crystalball_function(x, [0], [1], [2], [3])*[4]",
                var_low[p][v],
                var_high[p][v],
            )
            # alpha, n, sigma, mu
            f.SetParameters(1, 1, abs(h[p][v].GetMean()), 0, h[p][v].GetMaximum())
        else:
            f = ROOT.TF1(f"f_{p}_{v}", "gaus", var_low[p][v], var_high[p][v])

        h[p][v].Fit(f, "R")
        h[p][v].Draw()
        h[p][v].Write()
        # c.Print(fname)
    # c.Print(f"{fname}]")
outfile.Close()
