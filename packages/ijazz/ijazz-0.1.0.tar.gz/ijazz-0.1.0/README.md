# IJazZ_2p0

This repo includes the fitter part only. To use the full workflow, use [`law_ijazz`](https://gitlab.cern.ch/pgaigne/law_ijazz2p0).

## Install package using conda
Clone the repo
```
git clone https://gitlab.cern.ch/fcouderc/ijazz_2p0.git
cd ijazz_2p0
```
Create conda env
```
conda create -n ijazz python=3.9
conda activate ijazz
```
Install package in editable mode
```
pip install -e .
```

## Derive Scale and Smearing

```
ijazz_sas config/sas_config.yaml
```

where the config file is `config/sas_config.yaml` :
```
file_dt: data/cms/2022/higgs_dna_2022PreEE.pho.data.TimeCorr.parquet
file_mc: data/cms/2022/higgs_dna_2022PreEE.pho.mc.parquet
dir_results: results/test/
cset_name: "EtaR9"  # name of the correction (appended to the file name if correction
cat_latex: # latex names for parameters plots
  ScEta: "SuperCluster $\eta$"
  AbsScEta: "SuperCluster $|\eta|$"
  r9: "Seed Cluster R9"
  pt: "$p_T$ (GeV)"
dset_name: "TestDataSet" # dataset name
scale_flat_syst: 0.5e-3  # added in quadrature to the full list of scale systematics
smear_flat_syst: 0       # added in quadrature to the full list of smear systematics

syst: # list of systematics to be computed
  win_mll: # name of systematic
    # parameters to be overwritten
    fitter:
      win_z_mc: [65, 115]
      win_z_dt: [70, 110]
  cut_variation: # name of systematic
    # parameters to be overwritten
    sas:
      cut: pt1 > 30 and pt2 > 30
corrlib:
  cset_description: "EM object scale and smearing vs eta / r9"
  cset_version: 1
  
sas:
  use_rpt: true         # - when categories include pt, fit with the relative pt 
  hess: numerical       # - hessian matrix: null, numerical, analytical (not advised)
  learning_rate: 1.0e-3 # - learning rate to the keras optimizer 
  name_pt_var: pt       # - name of the pt variable in case used in categorisation and to be corrected
  err_mc: true          # - compute the uncertainty due to limited MC statistics
  correct_data: true    # - correct the data
  correct_mc: true      # - smear the MC
  categories:
      ScEta: [-3.0, -2.0, -1.49, -1.0, 0.0, 1.0, 1.49, 2.0, 3.0]
      r9: [-.Inf, 0.97, .inf]
  # - cut to apply in the input dataframes
  cut: null
fitter:
  win_z_mc: [70, 110]      # - mass range of the dilepton mass to fit
  win_z_dt: [80, 100]      # - larger mass range to consider MC events
  min_nevt_region_mc: 100  # - minimum number of mc events per category
  min_nevt_region_dt: 20   # - minimum number of data events per category
  bin_width_dt: 'Q'        # - binning width for the data, 'Q' for quantile binning
  bin_width_mc: 0.1        # - binning width for the MC
  name_cat: cat            # - name of the category variable
  name_weights: null       # - name of the weights variable for MC
  name_mll: 'mass'         # - name of the di-lepton mass variable  
minimizer:
  dnll_tol: 0.01           # - tolerance for the change in -2logL to determine convergence
  max_epochs: 500          # - maximum number of epochs for optimization
  init_rand: False         # - if True, initializes variables (resp, reso) randomly.
  nepoch_print: 100        # - number of epochs to print the loss
  batch_size: 200          # - size of the batch for likelihood computation
  batch_training: True     # - use batch 
  device: GPU              # - device to use for the minimizer
  minimizer: Adam          # - optimization method, either 'Adam' or a SciPy minimizer (e.g., 'TNC').


```

## Input ntuples

Input files must be `parquet` files with a column for the dilepton mass `name_mll` and columns for variables of each electrons `var1` and `var2`. MC weights can be used using `name_weights`. For example:
- `mass`, `weight_central`, `ScEta1`, `ScEta2`, `r91`, `r92`, `pt1` and `pt2`.

A reader to convert Higgs DNA output files to IJazZ input files is provided in [`law_ijazz`](https://gitlab.cern.ch/pgaigne/law_ijazz2p0).