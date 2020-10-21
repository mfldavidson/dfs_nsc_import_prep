# Prepare an NSC Data Return File for Import into DRDFS Salesforce
[Detroit Regional Dollars for Scholars](https://drdfs.org/) gets data from the 
National Student Clearinghouse on its alumni outcomes using the 
[StudentTracker service](https://www.studentclearinghouse.org/colleges/studenttracker/). 
This program takes a file returned from NSC as input, manipulates the data 
into the format needed to import it into DRDFS's student information system 
(Salesforce CoPilot), and outputs a file ready to be imported.

Refer to the Jupyter Notebook (`ipynb` file) for details on how the program 
works and the inputs and outputs.

## Initial Setup (First time only)
These instructions assume that you have installed Python 3 and are using a bash 
shell (Git Bash for Windows, Terminal for Mac).

1. Clone this repo to your computer by using the command line to navigate to 
the directory/folder where you want it and entering `git clone 
https://github.com/mfldavidson/dfs_nsc_import_prep.git`.

1. Create a new file in the repo named `creds.py`, paste the following code,
and fill in the places indicated with your Salesforce credentials (admin 
access to Salesforce AND CoPilot required). Save the file.
    ```buildoutcfg
    from simple_salesforce import Salesforce
    
    sf = Salesforce(username='YOUR SALESFORCE USERNAME (EMAIL)',
                    password='YOUR SALESFORCE PASSWORD',
                    security_token='YOUR SALESFORCE SECURITY TOKEN',
                    domain='detroitdfs.my')
    ```

1. _If using virtual environments only:_ Create a virtual environment 
(`python3 -m venv whateveryouwanttonameit`) wherever you keep your virtual 
environments. Activate the virtual environment 
(`source whateveryounamedthevirtualenv/bin/activate` if you are on a Mac, 
or `source whateveryounamedthevirtualenv/Scripts/activate` if you are on a PC).

1. Install all necessary libraries by navigating to the repo and then running 
the command `pip install -r requirements.txt`.

1. _If using virtual environments only:_ Enter `python -m ipykernel install 
--user --name=dfs_nsc` in your command line. You should get `Installed 
kernelspec dfs_nsc in [path]`. Then enter `jupyter notebook`. In the window 
that opens, click on the `ipynb` file. Select Kernel>Change kernel>dfs_nsc.

1. Create a folder in `dfs_nsc_import_prep` named `data`.

## Running the Program

1. Put the file returned from the NSC in the `data` folder and name it 
`NSC_Return.csv`.

1. Ensure you are in the `dfs_nsc_import_prep` directory in your command line.

1. Enter `jupyter notebook` in your command line.

1. In the window that opens, click on the `ipynb` file.

1. Click Cells>Run All.

1. Take the two output files and upload them in DataLoader using the mappings
in `data_loader_files`.
