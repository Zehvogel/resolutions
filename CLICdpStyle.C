#include "TROOT.h"
#include "TStyle.h"
#include "TPad.h"
#include "TLatex.h"
#include "TH1.h"
#include "TLegend.h"
#include "TLegendEntry.h"
#include "TPaveStats.h"
#include "TGraph.h"
#include "TObject.h"

#include<iostream>


Color_t color1 = kBlack;
Color_t color2 = kRed-7;
Color_t color3 = kBlue;
Color_t color4 = kGreen+2;
Color_t color5 = kCyan+1;
Color_t color6 = kRed+2;
Color_t color7 = kOrange;
Color_t color8 = kViolet+2;


void CLICdpLabel(std::string status);
void CLICdpLabel(Double_t x=0.20, Double_t y=0.86, std::string status="work in progress", Color_t color=kBlack);

void CLICdpStyle()
{
  gROOT->SetStyle("Plain"); /*Default white background for all plots*/

  TStyle *clicdpStyle = gROOT->GetStyle("Plain");

  /* set bkg color of all to kWhite: white, but not 0*/
  clicdpStyle->SetCanvasColor(kWhite);
  clicdpStyle->SetFrameFillColor(kWhite);
  clicdpStyle->SetStatColor(kWhite);
  clicdpStyle->SetPadColor(kWhite);
  clicdpStyle->SetFillColor(10);
  clicdpStyle->SetTitleFillColor(kWhite);
  
  
   /* SetPaperSize wants width & height in cm: A4 is 20,26 & US is 20,24*/
   clicdpStyle->SetPaperSize(20, 26); 
   /* No yellow border around histogram*/
   clicdpStyle->SetDrawBorder(0);
   /* remove border of canvas*/
   clicdpStyle->SetCanvasBorderMode(0);
   /* remove border of pads*/
   clicdpStyle->SetPadBorderMode(0);
   clicdpStyle->SetFrameBorderMode(0);
   clicdpStyle->SetLegendBorderSize(0);
  
   /* default text size*/
   clicdpStyle->SetTextSize(0.05);
   clicdpStyle->SetTitleSize(0.07,"xyz");
   clicdpStyle->SetLabelSize(0.06,"xyz");
   /* title offset: distance between given text and axis, here x,y,z*/
   clicdpStyle->SetLabelOffset(0.015,"xyz");
   clicdpStyle->SetTitleOffset(1.2,"yz"); //equivalent to: clicdpStyle->SetTitleYOffset(1.2);
   clicdpStyle->SetTitleOffset(1.0,"x");



   /* Use visible font for all text*/
   int font = 42; 
   clicdpStyle->SetTitleFont(font);
   clicdpStyle->SetTitleFontSize(0.06);
   clicdpStyle->SetStatFont(font);
   clicdpStyle->SetStatFontSize(0.07);
   clicdpStyle->SetTextFont(font);
   clicdpStyle->SetLabelFont(font,"xyz");
   clicdpStyle->SetTitleFont(font,"xyz");
   clicdpStyle->SetTitleBorderSize(0);
   clicdpStyle->SetStatBorderSize(1);
   //clicdpStyle->SetLegendFont(font);

   /* big marker points*/
   clicdpStyle->SetMarkerStyle(1);
   clicdpStyle->SetLineWidth(2);  
   clicdpStyle->SetMarkerSize(1.2);
   /*set palette in 2d histogram to nice and colorful one*/
   clicdpStyle->SetPalette(1,0); 

   /*No title for histograms*/
   clicdpStyle->SetOptTitle(0);
   /* show the errors on the stat box */
   clicdpStyle->SetOptStat(0); 
   /* show errors on fitted parameters*/
   clicdpStyle->SetOptFit(0); 
   /* number of decimals used for errors*/
   clicdpStyle->SetEndErrorSize(5);   

   /* set line width to 2 by default so that histograms are visible when printed small
      idea: emphasize the data, not the frame around*/
   clicdpStyle->SetHistLineWidth(2);
   clicdpStyle->SetFrameLineWidth(2);
   clicdpStyle->SetFuncWidth(2);
   clicdpStyle->SetHistLineColor(kBlack);
   clicdpStyle->SetFuncColor(kRed);
   clicdpStyle->SetLabelColor(kBlack,"xyz");

   //set the margins
   clicdpStyle->SetPadBottomMargin(0.18);
   clicdpStyle->SetPadTopMargin(0.08);
   clicdpStyle->SetPadRightMargin(0.08);
   clicdpStyle->SetPadLeftMargin(0.17);
   
   //set the number of divisions to show
   clicdpStyle->SetNdivisions(506, "xy");
   
   //turn off xy grids
   clicdpStyle->SetPadGridX(0);
   clicdpStyle->SetPadGridY(0);
   
   //set the tick mark style
   clicdpStyle->SetPadTickX(1);
   clicdpStyle->SetPadTickY(1);

   clicdpStyle->SetCanvasDefW(800);
   clicdpStyle->SetCanvasDefH(700);

   gROOT->ForceStyle();
}

/***********************************************************************/
/*                                                                     */
/*       draw legend for 2 histos on the same plot                     */
/*                                                                     */
/***********************************************************************/
void Draw2Legend(TH1 *histo1, 
                 TH1 *histo2,
                 const Char_t *label1, 
                 const Char_t *label2,
                 const Char_t *header="")
{

  Float_t max1 = histo1->GetMaximum();
  Float_t max2 = histo2->GetMaximum();
  if (max1 >= max2) histo1->SetMaximum(max1 * 1.3);
  else histo1->SetMaximum(max2 * 1.3);

  TLegend *legend = new TLegend(0.1436782,0.8072034,0.6408046,0.9851695,NULL,"brNDC");
  legend->SetTextAlign(22);
  legend->SetTextSize(0.1);
  legend->SetTextSize(0.06);
  legend->SetTextFont(42);
  
  TLegendEntry* entry1 = legend->AddEntry(histo1,label1,"LPF");  
  entry1->SetTextColor(histo1->GetLineColor());
  
  TLegendEntry* entry2 = legend->AddEntry(histo2,label2,"LPF");
  entry2->SetTextColor(histo2->GetLineColor());

  if (std::string(header) != "") legend->SetHeader(header); 

  legend->SetFillColor(kWhite); 
  legend->Draw();

  gPad->Update();
}

/***********************************************************************/
/*                                                                     */
/*       draw legend for 7 histos on the same plot                     */
/*                                                                     */
/***********************************************************************/
void Draw7Legend(TGraph *histo1, 
                 TGraph *histo2,
                 TGraph *histo3,
                 TGraph *histo4,
                 TGraph *histo5,
                 TGraph *histo6,
                 TGraph *histo7,
		 const Char_t *label1, 
                 const Char_t *label2,
		 const Char_t *label3, 
                 const Char_t *label4,
		 const Char_t *label5, 
                 const Char_t *label6,
		 const Char_t *label7, 
                 const Char_t *header="")
{

  TLegend *legend = new TLegend(0.006231824,0.3648567,0.8683008,0.9190962,NULL,"brNDC");
  legend->SetTextAlign(12);
  legend->SetTextSize(0.1);
  legend->SetTextSize(0.1);
  legend->SetTextFont(42);
  
  TLegendEntry* entry1 = legend->AddEntry(histo1,label1,"L");  
  entry1->SetTextColor(histo1->GetLineColor());
  
  TLegendEntry* entry2 = legend->AddEntry(histo2,label2,"L");
  entry2->SetTextColor(histo2->GetLineColor());

  TLegendEntry* entry3 = legend->AddEntry(histo3,label3,"L");
  entry3->SetTextColor(histo3->GetLineColor());

  TLegendEntry* entry4 = legend->AddEntry(histo4,label4,"L");
  entry4->SetTextColor(histo4->GetLineColor());

  TLegendEntry* entry5 = legend->AddEntry(histo5,label5,"L");
  entry5->SetTextColor(histo5->GetLineColor());

  TLegendEntry* entry6 = legend->AddEntry(histo6,label6,"L");
  entry6->SetTextColor(histo6->GetLineColor());

  TLegendEntry* entry7 = legend->AddEntry(histo7,label7,"L");
  entry7->SetTextColor(histo7->GetLineColor());

  if (std::string(header) != "") legend->SetHeader(header); 

  legend->SetFillColor(kWhite); 
  legend->Draw();

  gPad->Update();
}

/***********************************************************************/
/*                                                                     */
/*       draw statistics boxes for 2 histos                            */
/*       (needs h2->Draw("sames"))                                     */
/*                                                                     */
/***********************************************************************/
bool Draw2StatsBoxes(TH1 *histo1, TH1 *histo2)
{
  /*Get the stats box and set the right colors*/
  TPaveStats *statsh1 = (TPaveStats*)histo1->GetListOfFunctions()->FindObject("stats");
  if (statsh1 == NULL)
    {
      std::cout<<"\n Could not find statistics box for histo " << histo1->GetName()<<std::endl;
      return false;
    }
  statsh1->SetLineColor(histo1->GetLineColor());
  statsh1->SetTextColor(histo1->GetLineColor());
  statsh1->SetX1NDC(0.72);
  statsh1->SetY1NDC(0.68);
  statsh1->SetX2NDC(0.92);
  statsh1->SetY2NDC(0.92);

  TPaveStats *statsh2 = (TPaveStats*)histo2->GetListOfFunctions()->FindObject("stats");
  if (statsh2 == NULL)
    {
      std::cout<<"\n Could not find statistics box for histo " << histo2->GetName()<<std::endl;
      std::cout<<"You need to call: histo->Draw(\"sames\")"<<std::endl;
      return false;
    }
  statsh2->SetLineColor(histo2->GetLineColor());
  statsh2->SetTextColor(histo2->GetLineColor());

  /*need to move the stats box below the previous one, as by default they are stacked*/
  statsh2->SetX1NDC(0.72);
  statsh2->SetY1NDC(0.44);
  statsh2->SetX2NDC(0.92);
  statsh2->SetY2NDC(0.67);
  statsh2->Draw();
  
  return true;
}


void CLICdpLabel(std::string status){
  CLICdpLabel(0.20,0.86,status,kBlack);
}//end CLICdpLabel



// void CLICdpLabel(Double_t x=0.20, Double_t y=0.86, std::string status="work in progress", Color_t color=kBlack){

//   TLatex l; 
//   l.SetNDC();
//   l.SetTextFont(42);
//   l.SetTextColor(color);
//   l.SetTextSize(0.05);

//   std::string label = std::string("CLICdp ");
//   l.DrawLatex(x,y,label.c_str());

//   TLatex l2; 
//   l2.SetNDC();
//   l2.SetTextFont(42);
//   l2.SetTextColor(color);
//   l2.SetTextSize(0.035);

//   double dy = l2.GetTextSize()+0.005;

//   l2.DrawLatex(x,y-dy,status.c_str());

//   return;
// }//end CLICdpLabel


void CLICdpLabel(Double_t x, Double_t y, std::string status, Color_t color){

  TLatex l; 
  l.SetNDC();
  l.SetTextFont(42);
  l.SetTextColor(color);
  l.SetTextSize(0.05);

  std::string label = std::string("CLICdp ");
  l.DrawLatex(x,y,label.c_str());

  TLatex l2; 
  l2.SetNDC();
  l2.SetTextFont(42);
  l2.SetTextColor(color);
  l2.SetTextSize(0.035);

  //double dx = l2.GetTextSize()+0.005;
  double dx = 0.4*l.GetTextSize()*label.length();

  l2.DrawLatex(x+dx,y,status.c_str());

  return;
}//end CLICdpLabel
