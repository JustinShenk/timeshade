# Nightshade

### Shade nighttime dark on plots

### Install

`pip install timeshade`

### Usage

```python
import timeshade; import pandas as pd

# create timeseries
idx = pd.date_range("2018-01-01", periods=100, freq="H")
ts = pd.Series(range(len(idx)), index=idx)

# shade
import tshade
timeshade.shade(ts)

# plot
import matplotlib.pyplot as plt
plt.show()
```

![timeshade](timeshade.png)
