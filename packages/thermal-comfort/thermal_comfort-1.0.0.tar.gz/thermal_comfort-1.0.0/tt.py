import numpy as np
import time
from thermal_comfort import _utci_approx, pet_static

SHAPE = (3889, 3434)
ta = np.random.uniform(20, 50, size=SHAPE)
tg = np.random.uniform(10, 80, size=SHAPE)
mrt_value = np.random.uniform(-29, 69, size=SHAPE)
v = np.random.uniform(0.5, 17, size=SHAPE)
rh = np.random.uniform(10, 100, size=SHAPE)
p = np.random.uniform(980, 1050, size=SHAPE)

orig_shape = ta.shape


# reshape arrays to be 1-dimensional
tair_raster = np.ravel(ta)
tmrt_raster = np.ravel(mrt_value)
windspeed_10m_raster = np.ravel(v)
rh_raster = np.ravel(rh)
p_raster = np.ravel(p)
breakpoint()

s = time.monotonic()
_utci_approx(
    ta=tair_raster,
    tmrt=tmrt_raster,
    v=windspeed_10m_raster,
    rh=rh_raster,
)
print(time.monotonic() - s)

s = time.monotonic()
pet_static(
    ta=tair_raster,
    tmrt=tmrt_raster,
    v=windspeed_10m_raster,
    rh=rh_raster,
    p=np.repeat(1013, tair_raster.shape),
)
print(time.monotonic() - s)

# single core
# 0.5402650130054099
# 30.2023619879983
# parallel