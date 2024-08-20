import qrcode
from PIL import Image
import csv
import numpy as np
import pandas as pd
pd.set_option("display.max_columns",None)
pd.set_option("display.max_rows",None)
data_file = pd.read_csv('costumer_info.csv')
names = data_file["name"].tolist()
numbers = data_file["number"].tolist()

for i in range(len(names)):
    img = qrcode.make(numbers[i])
    img.save(names[i]+'.png')
