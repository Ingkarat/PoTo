from pygal.stats import erfinv
from pygal.stats import norm_ppf
from pygal.stats import ppf
from pygal.stats import confidence_interval_continuous
from pygal.stats import confidence_interval_dichotomous
from pygal.stats import xxx

def test_PT_erfinv():
    erfinv(1.23)

def test_PT_norm_ppf():
    norm_ppf(0.23)

def test_PT_ppf():
    ppf(1,2)

def test_PT_confidence_interval_continuous():
    confidence_interval_continuous(1.23,4.56,5,.95)

def test_PT_confidence_interval_dichotomous():
    confidence_interval_dichotomous(1.23,5,0.95,False,True)

def test_PT_confidence_interval_manual():
    confidence_interval_manual(1.23,1,10)