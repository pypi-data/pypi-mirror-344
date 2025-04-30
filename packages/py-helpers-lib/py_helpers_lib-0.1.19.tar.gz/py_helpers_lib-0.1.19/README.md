# Python Helpers Library (No Black Box Definitions)

## Ecosystem

⭐ Portal:     https://bit.ly/finance_analytics  
📊 Blog:       https://slashpage.com/jh-analytics  

📈 Softrader:  https://pypi.org/project/softrader

🐍 Python:     https://github.com/jhvissotto/Project_Finance_Api_Python  
🐍 Pypi:       https://pypi.org/project/jh-finance-api  

🟦 TScript:    https://github.com/jhvissotto/Project_Finance_Api_TScript  
🟦 NPM:        https://www.npmjs.com/package/finance-analytics-api  

🧮 PyHelpers:  https://github.com/jhvissotto/Library_Python_Helpers  

🔌 Server:     https://bit.ly/jh_finance_api  
🔌 Swagger:    https://bit.ly/jh_finance_api_swagger  



## Install

```py
!pip install py-helpers-lib
```

```py
from py_helpers_lib import *
```


## System

```py
HEADERS = { 'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 'X-Requested-With':'XMLHttpRequest' }
```

```py
def _pickle(CASES:Lit['COMPUTE','RELOAD','LOAD'], Lambda, dirs=[], name='', ext='.pkl', *a,**b):

    path    = os.path.join(*dirs, name + ext)
    EXISTS  = os.path.exists(path)

    def _calc():    return Lambda(*a,**b)
    def _read():    return joblib.load(path)
    def _save(X):   joblib.dump(X, path);  return X

    if (CASES == 'COMPUTE'):    return _calc()
    if (CASES == 'RELOAD'):     return _save(_calc())
    if (CASES == 'LOAD'):
        if     EXISTS:          return _read()
        if not EXISTS:          return _save(_calc())


def _parquet(CASES:Lit['COMPUTE','RELOAD','LOAD'], Lambda, dirs=[], name='', ext='.parquet', *a,**b):

    path    = os.path.join(*dirs, name + ext)
    EXISTS  = os.path.exists(path)

    def _calc():    return Lambda(*a,**b)
    def _read():    return pd.read_parquet(path)
    def _save(Df):  Df.to_parquet(path, index=False);  return Df

    if (CASES == 'COMPUTE'):    return _calc()
    if (CASES == 'RELOAD'):     return _save(_calc())
    if (CASES == 'LOAD'):
        if     EXISTS:          return _read()
        if not EXISTS:          return _save(_calc())
```


## Casting
```py
_to_bool()  -> (     bool    )
_as_bool()  -> (None|bool    )
_to_logic() -> (     bool|int)
_as_logic() -> (None|bool|int)
```
```py
def _to_bool(x:None|bool|int|float|str, extend:bool): 

    if            str(x).lower() in ['true','1','1.0','t','y','yes']:   return True
    if            str(x).lower() in ['false','0','0.0','f','n','no']:   return False
    if extend and str(x).lower() in ['none','null','nan','']:           return False

    raise Exception('CASTING_BOOLEAN_FAILED')
```
```py
def _as_bool(x:None|bool|int|float|str, extend:bool, undefine:bool): 

    if            str(x).lower() in ['true','1','1.0','t','y','yes']:   return True
    if            str(x).lower() in ['false','0','0.0','f','n','no']:   return False
    if extend and str(x).lower() in ['none','null','nan','']:           return False
    if undefine:                                                        return None

    raise Exception('CASTING_BOOLEAN_FAILED')
```
```py
def _to_logic(x:None|bool|int|float|str, astype:Lit['bool','int'], extend:bool) -> (bool|int): 

    if            str(x).lower() in ['true','1','1.0','t','y','yes']:   return { 'bool':True,  'int':1 }[astype]
    if            str(x).lower() in ['false','0','0.0','f','n','no']:   return { 'bool':False, 'int':0 }[astype]
    if extend and str(x).lower() in ['none','null','nan','']:           return { 'bool':False, 'int':0 }[astype]

    raise Exception('CASTING_BOOLEAN_FAILED')
```
```py
def _as_logic(x:None|bool|int|float|str, astype:Lit['bool','int'], extend:bool, undefine:bool) -> (None|bool|int): 

    if            str(x).lower() in ['true','1','1.0','t','y','yes']:   return { 'bool':True,  'int': 1 }[astype]
    if            str(x).lower() in ['false','0','0.0','f','n','no']:   return { 'bool':False, 'int': 0 }[astype]
    if extend and str(x).lower() in ['none','null','nan','']:           return { 'bool':False, 'int': 0 }[astype]
    if undefine:                                                        return { 'bool':None,  'int':-1 }[astype]

    raise Exception('CASTING_BOOLEAN_FAILED')
```


## Text Functions

```py
def _between(txt:str, A:str, Z:str):
    return txt.split(A)[1].split(Z)[0]


def _replaces(txt:str, args:List[Tuple[str, str]]):
    
    for (old, new) in args:
        txt = txt.replace(old, new)

    return txt
```



## Math Formulas 1

```py
def _step(X, stp=nan): 
    if isinstance(stp, int) and (stp < 0 or 1 < stp):
            return X[::stp]
    else:   return X

def _round(x, R=nan):
    if isinstance(R, int) and (R >= 0):
            return np.round(x, R)
    else:   return x
```


```py
def _count(x):      return pd.Series(x).count()

def _sum(x):        return np.nansum(x)
def _prod(x):       return np.nanprod(x)

def _cumsum(x):     return np.nancumsum(x)
def _cumprod(x):    return np.nancumprod(x)

def _mean(x):       return np.nanmean(x)
def _std(x):        return np.nanstd(x)

def _gmean(x):      return exp(np.nanmean(log(x)))
def _gstd(x):       return exp(np.nanstd(log(x)))

def _med(x):        return np.nanmedian(x)
def _mad(x):        return sp_stats.median_abs_deviation(x, nan_policy='omit')

def _max(x):        return np.nanmax(x)
def _min(x):        return np.nanmin(x)

def _Q3(x):         return np.nanpercentile(x, 75)
def _Q1(x):         return np.nanpercentile(x, 25)

def _pct_prod(x):     return    _prod(1+x/100)
def _pct_cumprod(x):  return _cumprod(1+x/100)
def _pct_gmean(x):    return   _gmean(1+x/100)*100-100
def _pct_gstd(x):     return    _gstd(1+x/100)*100-100

```


```py
def _range(Max, Min):               return (Max - Min)
def _IQR(Q3, Q1):                   return (Q3 - Q1)

def _minmax(Val, Min, Range):       return (Val - Min) / Range *100
def _robust(val, med, IQR):         return (val - med) / IQR   *100

def _zscore(val, avg, dev):         return (val - avg) / dev
def _pscore(val, series):           return sp_stats.percentileofscore(series, val, 'mean', 'omit')

def _log1p_zscore(val, avg, dev):   return (log(1+val/100) - log(1+avg/100)) / log(1+dev/100)
```


## Math Formulas 2

```py
def _groupby(Df, By=''):
    if By:  return Df.groupby(By, sort=0, group_keys=0, dropna=0)
    else:   return Df

def _apply(Df,      Lambda,            By='', stp=nan, R=nan):  return _round(_groupby(_step(Df, stp), By)                        .apply(Lambda),                       R)
def   _cum(Df, Col, Lambda,            By='', stp=nan, R=nan):  return _round(_groupby(_step(Df, stp), By)[Col].expanding()       .apply(Lambda).reset_index(0,drop=1), R)
def  _roll(Df, Col, Lambda, win, wmin, By='', stp=nan, R=nan):  return _round(_groupby(_step(Df, stp), By)[Col].rolling(win, wmin).apply(Lambda).reset_index(0,drop=1), R)
```


```py
def      _shift(Df, Col, P,   By=''                          ):  return        _groupby(      Df,       By)[Col]      .shift(P)
def       _diff(Df, Col, P=1, By='',           stp=nan, R=nan):  return _round(_groupby(_step(Df, stp), By)[Col]       .diff(P),           R)
def _pct_change(Df, Col, P=1, By='', base=100, stp=nan, R=nan):  return _round(_groupby(_step(Df, stp), By)[Col] .pct_change(P).mul(base), R)
```


```py
def _cum_count      (Df, Col,            By=''                 ):  return  _cum(Df, Col, _count,                By)
def _cum_pct_prod   (Df, Col,            By=''                 ):  return  _cum(Df, Col, _pct_prod,             By)

def _roll_mean      (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _mean,      win, wmin, By, stp, R)
def _roll_std       (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _std,       win, wmin, By, stp, R)

def _roll_gmean     (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _gmean,     win, wmin, By, stp, R)
def _roll_gstd      (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _gstd,      win, wmin, By, stp, R)

def _roll_pct_gmean (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _pct_gmean, win, wmin, By, stp, R)
def _roll_pct_gstd  (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _pct_gstd,  win, wmin, By, stp, R)

def _roll_med       (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _med,       win, wmin, By, stp, R)
def _roll_mad       (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _mad,       win, wmin, By, stp, R)

def _roll_max       (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _max,       win, wmin, By, stp, R)
def _roll_min       (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _min,       win, wmin, By, stp, R)

def _roll_Q3        (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _Q3,        win, wmin, By, stp, R)
def _roll_Q1        (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _roll(Df, Col, _Q1,        win, wmin, By, stp, R)

def _roll_range     (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _round(_range(Max=_roll_max(Df, Col, win, wmin, By, stp), Min=_roll_min(Df, Col, win, wmin, By, stp)), R)
def _roll_iqr       (Df, Col, win, wmin, By='', stp=nan, R=nan):   return _round(  _IQR( Q3= _roll_Q3(Df, Col, win, wmin, By, stp),  Q1= _roll_Q1(Df, Col, win, wmin, By, stp)), R)
```


```py
def _roll_minmax     (Df, Col, win, wmin, By='', stp=nan, R=nan):  return _round(      _minmax(Val=Df[Col],  Min=      _roll_min(Df, Col, win, wmin, By, stp),  Range= _roll_range(Df, Col, win, wmin, By, stp)), R)
def _roll_robust     (Df, Col, win, wmin, By='', stp=nan, R=nan):  return _round(      _robust(val=Df[Col],  med=      _roll_med(Df, Col, win, wmin, By, stp),  IQR=     _roll_iqr(Df, Col, win, wmin, By, stp)), R)
def _roll_zscore     (Df, Col, win, wmin, By='', stp=nan, R=nan):  return _round(      _zscore(val=Df[Col],  avg=     _roll_mean(Df, Col, win, wmin, By, stp),  dev=     _roll_std(Df, Col, win, wmin, By, stp)), R)
def _roll_pct_gscore (Df, Col, win, wmin, By='', stp=nan, R=nan):  return _round(_log1p_zscore(val=Df[Col],  avg=_roll_pct_gmean(Df, Col, win, wmin, By, stp),  dev=_roll_pct_gstd(Df, Col, win, wmin, By, stp)), R)

def _roll_pscore     (Df, Col, win, wmin, By='', stp=nan, R=nan):  return _roll(Df, Col, lambda X: _pscore(val=X.tail(1), series=X), win, wmin, By, stp, R)
```


## Pandas Dataframe


```py
def _columns(Df, A, Z): 
    return Df.loc[:, A:Z].columns

def _insert(Df, idx, Col, Val):
    if Col in Df:   Df[Col] = Val
    else:           Df.insert(idx, Col, Val)

def _get_group(Df, Get, By):
    return _groupby(Df, By).get_group(Get) .reset_index(0,drop=1)
```

```py
def _rank      (Df, Col, By, method='dense', ascending=True): return _groupby(Df, By)[Col].rank(method,  ascending)
def _rank_high (Df, Col, By, method='dense'):                 return _groupby(Df, By)[Col].rank(method, False)
def _rank_low  (Df, Col, By, method='dense'):                 return _groupby(Df, By)[Col].rank(method,  True)
```