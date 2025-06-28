## PoTo
PoTo: A Hybrid Andersen's Points-to Analysis for Python


## Python scripts and directories

##### Stable version code
- stable.py: to reproduce paper results from stable logs
- utils.py: auxiliary, called from stable.py
- stable_log/: directory with older logs

##### Poto and type inference code
- poto.py: to run PoTo and produce .pkl files in poto_result/
- infer.py: to run DLInfer and Pytype and compare PoTo+ to Pytype, DL-ST, DL-ML, and DL-DY
- infer_shallow_type.py: auxiliary, used in infer.py to augment with PoTo+
- pt_engine/: PoTo code

##### Data directories
- DLInfer_data/: DLInfer result files, from DLInfer's artifact
- orig_pro_dynamic/: code directory from DLInfer's artifact with modified /test/ suits for PoTo; contains packages cerberus, mtgjson, pygal, sc2, zfsp, anaconda, invoke, wemake_python_styleguide, bokeh, and ansible
- type_data/: contains Manual_verdict\* files for alignment of type name strings across tools

##### Result directories, created by analysis
- poto\_result/: running poto.py writes PTonly\_{package\_name}.txt files here
- dlinfer\_result/: running infer.py creates DLInfer files in required format 
- reveal\_orig\_pro\_dynamic/: instrumented code to run Pytype and collect Pytype data
- type\_result/: running infer.py writes comparison output; main comparison output on stdout

#### Sample run on included packages

1. To run PoTo we recomment hardcoding the package name at the top of the file, e.g., cerberus, then run python3.9 poto.py. Smaller packages (cerberus, mtgjson, pygal, zfsp, sc2, anaconda and wemake) run in 1-5 minutes. However, bokeh runs for more than an hour and it may require a restart after the N-th test file to continue completion. Due to dynamic evaluation invoke may require Ctrl-C to continue. Result dumps files into poto\_result/ directory. NOTE: Dynamic evaluation may create files in current directory. 

2. Set choice = 1 in infer.py then run python3.9 infer.py to generate DLInfer files in dlinfer_result/
3. Set choice = 2 in infer.py to generate another batch of DLInfer files, also written in dlinfer_result/
4. Set choice = 4 in infer.py then run python3.9 infer.py to create PTonly\_{package\_name}.txt files in poto\_result/
5. Set choice = 5 in infer.py then run python3.9 infer.py. The step runs Pytype and this step takes a long time even for smaller packages. It takes a day on the larger packages bokeh and ansible (on a commodity laptop). This choice then compares PoTo+ with the baselines and creates comparison data files. It produces comparison outut on stdout. We recommend running per package

#### Running PoTo on new packages

To run PoTo on a new package, e.g., sklearn, adjust code directories and importanlty, adjust the test suites. PoTo expects test-suite file in the form of fixture followed by calls to functions on fixture receiver, or a file of test functions calling different functions in the package. PoTo cannot interpret pytest tests and will produce suboptimal results on pytest suites. 

## Notes
- The results may not reproduce exactly as they depend on the Python module environment currently loaded in one's system
- "as well as some cases of processings that depends on the path 
    - ex: if '/Users/ingkarat/Documents/GitHub/xxxxx' in x: return x.replace("/Users/ingkarat/Documents/GitHub/xxxxx", "...")

## WARNING
- "Dynamic evaluation may create files in current dir"
- Concrete evaluation may run dangerous codes
