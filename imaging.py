import numpy as np; 
import seaborn as sns; 
import pandas as pd;
import sys


################ Author's Notes ################

# Requires Additional Library Support, namely Seaborn
# and runs only on python 2.7x. Unfortunately, creating
# a heatmap without additional library support is beyond 
# the scope of this project.
#
# To run in command line: 
# 	python imaging.py FILE_PATH.csv
#
# Note: CSV files must include at top of file: Y-Axis, X-Axis, Number of Hits

if __name__ == '__main__' and len(sys.argv) == 2:
	file_path = sys.argv[1]
	sns.set()
	data = pd.read_csv(file_path)
	data = data.pivot('Y-Axis', 'X-Axis', 'Number of Hits')
	ax = sns.heatmap(data)
	sns.plt.show()