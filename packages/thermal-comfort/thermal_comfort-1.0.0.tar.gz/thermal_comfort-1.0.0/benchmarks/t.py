from thermal_comfort import pet_static
import time

import warnings
warnings.filterwarnings("ignore")
import numpy as np
np.random.seed(0)
SHAPE = (8000, 8000)
ta = np.random.uniform(20, 50, size=SHAPE)
tg = np.random.uniform(10, 80, size=SHAPE)
mrt_value = np.random.uniform(3, 80, size=SHAPE)
va = np.random.uniform(0, 15, size=SHAPE)
rh = np.random.uniform(10, 100, size=SHAPE)
p = np.random.uniform(980, 1050, size=SHAPE)
d = np.random.uniform(0.05, 0.15, size=SHAPE)
e = np.random.uniform(0.5, 1, size=SHAPE)


start = time.monotonic()
pet_static(ta=ta, rh=rh, v=va, tmrt=mrt_value, p=p)
print((time.monotonic() - start))