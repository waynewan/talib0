import pandas as pd
import numpy as np
import numba as nb
# from jackutil.microfunc import if_else

# --
# -- TA implementation, as a replacement for TA-Lib
# --

# --
# -- exact match to talib.atr
# --
@nb.jit(nopython=True,cache=True)
def ____atr_loop____(timeperiod,true_range):
	avg_true_range = np.full_like(true_range,np.nan)
	avg_true_range[timeperiod] = true_range[1:timeperiod+1].mean()
	for nn in range(timeperiod+1,len(true_range)):
		avg_true_range[nn] = ( avg_true_range[nn-1]*(timeperiod-1)+true_range[nn] ) / timeperiod
	return avg_true_range

def nojit____atr_loop____(timeperiod,true_range):
	avg_true_range = pd.Series(index=high_vals.index)
	avg_true_range.iloc[timeperiod] = true_range[1:timeperiod+1].mean()
	for nn in range(timeperiod+1,len(high_vals)):
		avg_true_range.iloc[nn] = ( avg_true_range.iloc[nn-1]*(timeperiod-1)+true_range.iloc[nn] ) / timeperiod
	return avg_true_range

def ATR(high_vals,low_vals,close_vals,timeperiod):
	if(timeperiod>=len(close_vals)):
		# --
		# -- not enough data
		# --
		return np.nan
	# --
	# --
	# --
	true_range = pd.concat([
		high_vals - low_vals,
		np.abs(high_vals - close_vals.shift(1)),
		np.abs(low_vals - close_vals.shift(1)),
	],axis=1).max(axis=1)
	return ____atr_loop____(timeperiod,true_range.to_numpy())
	# return nojit____atr_loop____(timeperiod,true_range)

# --
# -- exact match to talib.sar
# --
@nb.jit(nopython=True,cache=True)
def SAR(high,low,accel,max_accel):
	# --
	# --
	# --
	calc = []
	# --
	# -- init row0 [*_1 is for prev day]
	# --
	psar_b_1 = np.nan
	psar_1 = high[0]
	down_trend_1 = True
	extreme_pt_1 = low[0]
	factor_1 = accel
	psar_f_1 = (psar_1 - extreme_pt_1) * factor_1
	# --
	# -- iniit row1
	# --
	psar_b_0 = max(psar_1-psar_f_1,high[0])
	psar_0 = psar_b_0 if(psar_b_0>high[1]) else extreme_pt_1 
	down_trend_0 = psar_0>high[1]
	extreme_pt_0 = min(extreme_pt_1,low[1]) if down_trend_0 else max(extreme_pt_1,high[1])
	factor_0 = accel if(down_trend_0 !=down_trend_1) else (factor_1 if(extreme_pt_0 !=extreme_pt_1) else min(factor_1+accel,max_accel))
	psar_f_0 = (psar_0 - extreme_pt_0) * factor_0
	# --
	calc.append([ psar_b_1, psar_1, down_trend_1, extreme_pt_1, factor_1, psar_f_1 ])
	calc.append([ psar_b_0, psar_0, down_trend_0, extreme_pt_0, factor_0, psar_f_0 ])
	# --
	# -- 0 is current day; 1 is prev day; 2 is prev 2 days
	# !! set first value (psar_1) to nan to match TA-Lib behavior !!
	# --
	psar = [np.nan, psar_0]
	for nn in range(2,len(high)):
		psar_1 = psar_0
		down_trend_1 = down_trend_0
		extreme_pt_1 = extreme_pt_0
		factor_1 = factor_0
		psar_f_1 = psar_f_0
		day0_high,day1_high,day2_high = high[nn],high[nn-1],high[nn-2]
		day0_low,day1_low,day2_low = low[nn],low[nn-1],low[nn-2]
		# --
		psar_b_0 = max(psar_1-psar_f_1,day1_high,day2_high) if down_trend_1 else min(psar_1-psar_f_1,day1_low,day2_low)
		pivot_pt = (psar_b_0>day0_high) if down_trend_1 else (psar_b_0<day0_low)
		psar_0 = psar_b_0 if pivot_pt else extreme_pt_1
		down_trend_0 = psar_0>day0_high
		extreme_pt_0 = min(extreme_pt_1,day0_low) if down_trend_0 else max(extreme_pt_1,day0_high)
		factor_0 = accel if(down_trend_0 !=down_trend_1) else (factor_1 if extreme_pt_0==extreme_pt_1 else min(factor_1+accel,max_accel))
		# --
		psar_f_0 = (psar_0 - extreme_pt_0) * factor_0
		psar.append(psar_0)
		calc.append([ psar_b_0, psar_0, down_trend_0, extreme_pt_0, factor_0, psar_f_0 ])
	return psar

