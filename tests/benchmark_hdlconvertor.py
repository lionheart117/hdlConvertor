import sys
import time
import hdlConvertor
from hdlConvertorAst.language import Language
#from hdlConvertorAst.to.verilog.verilog2005 import ToVerilog2005
#from hdlConvertor import HdlConvertor

filelist = sys.argv[1]
include_dirs = []
c = hdlConvertor.HdlConvertor()
ISOTIMEFORMAT = "%Y%m%d%H%M%S"
logfilename = 'benchmark_hdlconvertor_log' + str(time.strftime(ISOTIMEFORMAT))
flog = open(logfilename,'w')
sum_cnt = 0
err_cnt = 0
with open(filelist,'r') as fp:
    for filename in fp:
        sum_cnt += 1
        try:
            d = c.parse(filename.replace("\n",""), Language.SYSTEM_VERILOG, include_dirs, hierarchyOnly=False, debug=True)
        except hdlConvertor._hdlConvertor.ParseException as e:
            err_cnt += 1
            flog.write(("No.%d:Error occurs:" % sum_cnt) + e.__str__())
            continue

flog.write("\nBenchmark Result:\nsum number: %d\n" % sum_cnt)
flog.write("err number: %d\n" % err_cnt)
flog.close()
#tv = ToVerilog2005(sys.stdout)
#tv.visit_HdlContext(d)

#for o in d.objs:
#    print(o)