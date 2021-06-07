#!/usr/bin/python

import sys
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as pl


FILENAME = sys.argv[1]

#%matplotlib inline  # jupyter notebook



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# load the data sheet
df = pd.read_csv(f'{FILENAME}.csv')
# display 5 rows of dataset
df.head()
# Box Plot visualization MSSubClass with Pandas
plt.boxplot(df['sum(fitness)'])
plt.show()