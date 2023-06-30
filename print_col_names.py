import argparse
import ROOT

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="print_col_names",
        description="Prints out collection ID and name of all collections in an EDM4hep file",
    )
    parser.add_argument("filename")
    args = parser.parse_args()

    f = ROOT.TFile(args.filename)
    f.metadata.SetScanField(0)
    f.metadata.Scan("CollectionIDs.m_collectionIDs:CollectionIDs.m_names")

