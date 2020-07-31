from swmm5.swmm5tools import SWMM5Simulation
import tempfile
import os
from string import Template

KEYNODE='J30_BA109'
RUNDIR=os.getcwd()+os.sep+"run"

"""Use this as the main entry point. Provide a list of lists of numbers for 
us1, us2, sealevels as the only argument. 
data=(us1, us2, sealevels)
Lengths should be 
             min    max   type
us1          29     30    flow m3/s - daily data
us2          29     30     ""
selevels     690    720   sealevel m (above msl) - hourly data

returns: 
water head (level above msl) at node KEYNODE
"""
def get_depth(data):
        us1, us2,  sealevels=data
        with tempfile.TemporaryDirectory(prefix="rundir", dir=RUNDIR) as td:      
                fileset=_make_inputfile(us1, us2, sealevels, td) # once td goes out of scope, everything will be deleted. 
                res = _run_model(SWMM5Simulation, fileset)
        return list(res)


def _make_inputfile(us1, us2, sl1, td):
        with open(os.getcwd()+os.sep+"templates"+os.sep+"us.dat_") as inf:
                lines=inf.readlines() 
        
        bc1file=td+os.sep+"usbc1.dat"
        with open(bc1file, "w") as outf:
                _write(lines, outf, us1)
        bc2file=td+os.sep+"usbc2.dat"
        with open(td+os.sep+"usbc2.dat", "w") as outf:
                _write(lines, outf, us2)   
        with open(os.getcwd()+os.sep+"templates"+os.sep+"sl.dat_") as inf:
                lines=inf.readlines()   
        slbc1file=td+os.sep+"slbc1.dat"
        with open(slbc1file, "w") as outf:
                _write(lines, outf, sl1)         
        with open(os.getcwd()+os.sep+"templates"+os.sep+"template.inp_") as inf:
                inpdata=inf.read()
        inpfile=td+os.sep+"model.inp"
        with open(inpfile, "w") as outf:
                res=Template(inpdata).substitute(hsf=os.getcwd()+os.sep+"data"+os.sep+"HOTSTART.hsf",
                                                 us1=bc1file,
                                                 us2=bc2file,
                                                 sl1=slbc1file,)
                outf.write(res)
                
        return [td, inpfile, bc1file, bc2file, slbc1file]

def _write(lines, outf, us):
        li=lines[:len(us)]
        ou=[a.strip() + "\t" + str(b) + "\n" for a,b in zip(li,us)]  
        outf.writelines(ou)
        
def _run_model(SWMM5Simulation, fileset):
        st=SWMM5Simulation(fileset[1])
        res=st.Results('NODE',KEYNODE, 1)
        return res



def _make_test_data():
        with open("./templates/sl_test.txt") as inf:
                sealevels=[float(x.strip()) for x in inf.readlines()][:-23]
        with open("./templates/us_test.txt") as inf:
                us1=[float(x.strip()) for x in inf.readlines() ][:-1]
        us2=[150.0 for x in range(30) ]
        #us1=[x*2.0 for x in us1]
        sealevels=[x+.01 for x in sealevels]
        return (us1, us2, sealevels)


if __name__=="__main__":
        from time import perf_counter 
        t_start = perf_counter()  
        res = get_depth(_make_test_data())
        t_stop = perf_counter()  
        print(list(res))
        print(max(res))
        print("Elapsed time during the whole program in seconds:", 
              t_stop-t_start)         