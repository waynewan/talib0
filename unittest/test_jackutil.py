# --
# --
# --
from pprint import pprint
from jackutil.configuration import configuration

basespec = { "a": { "x": 1, "y": 99 }, "pp":456 }
var = { "a/x": [ 23, 34] , ("a/y","pp"):[ (88,12), (77,33) ]}
cfg = configuration(basespec=basespec,variations=var)
vv = cfg.all_configurations()
print(vv)
print(len(vv))

# --
# --
# --
from datetime import datetime
import jackutil.microfunc as mf

nowdt = None
print(nowdt)
print( mf.date_only(nowdt) )

nowdt = datetime.utcnow()
print(nowdt)
print( mf.date_only(nowdt) )

# --
# --
# --
from jackutil import microfunc as mf
dt_str = '2021-01-03'
dt_dt = mf.dt_conv(dt_str, 'dt')
print(type(dt_dt), dt_dt)

dt_dt = mf.dt_conv(dt_str, 'dt64')
print(type(dt_dt), dt_dt)

dt_dt = mf.dt_conv(dt_str, 'ts')
print(type(dt_dt), dt_dt)

dt_dt = mf.dt_conv(dt_str, 'str')
print(type(dt_dt), dt_dt)

# --
# --
# --
from jackutil import auditedvalue
v1 = auditedvalue.AuditedValue()
v1.setvalue(33,date=datetime.utcnow(),msg="first value")
v1.setvalue(99,date=datetime.utcnow(),msg="second value")
pprint(v1.audit)
pprint(v1)

# --
# -- simple delta for configuraiton
# --
basespec = {
	"a" : 1,
	"b" : 2,
	"x" : { "c" : 3, "d" : 4 }
}
delta = { "a" : range(3, 20, 3) }
cc = configuration(basespec=basespec,variations=delta)
print("=" * 30)
for c in cc.all_configurations():
	pprint(c)

# --
# -- simple delta 2 for configuraiton
# --
basespec = {
	"a" : 1,
	"b" : 2,
	"x" : { "c" : 3, "d" : 4 }
}
delta = { 
	"a" : range(3, 20, 3),
	"x/c" : range(4, 20, 4),
	"b" : -1,
	"x/d" : "xyz",
}
cc = configuration(basespec=basespec,variations=delta)
print("=" * 30)
for c in cc.all_configurations():
	pprint(c)

# --
# -- vector delta
# --
delta = { 
	("x/d","x/c") : [
		(d,c)
		for d in range(3, 20, 3)
	 	for c in range(4, 20, 4) 
		if(d>c)
	]
}
cc = configuration(basespec=basespec,variations=delta)
print("=" * 30)
for c in cc.all_configurations():
	pprint(c)
