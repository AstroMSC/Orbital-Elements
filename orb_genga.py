import glob
import math
import numpy as np
import os

sim_dir = str(raw_input("Enter path to Out*.dat files (eg: /home/yourname/genga/simulations/*/): ")
grav = 4. * math.pi * math.pi

for gpu in glob.glob(sim_dir):
    orbits = gpu + 'orbits.txt'
    if os.path.exists(orbits):
        os.remove(orbits)
    orbit=open(orbits,'a')
    line=np.asarray(['body','a','e','i','mass'])
    line.tofile(orbit,sep=' ',format='%10s')
    orbit.write('\n')
    outputs = glob.glob(gpu+'Out*.dat')
    if len(outputs) == 0:
        data=[]
    else:
        outputs.sort()
        lastout = outputs[-1]
        with open(lastout,'r') as file:
            data = file.readlines()
    #time = str(float(data[0].split()[0])/1.e6)[:6]
    for l in range(int(len(data))):
        name=data[l].split()[1]
        mass = float(data[l].split()[2])/.000003003
        xyz = [float(data[l].split()[4]),float(data[l].split()[5]),float(data[l].split()[6])]
        uvw = [float(data[l].split()[7]),float(data[l].split()[8]),float(data[l].split()[9])]
        r = (float(xyz[0])**2 + float(xyz[1])**2 + float(xyz[2])**2)**.5
        v2 = (float(uvw[0])*365.25*0.0172020989)**2 + (float(uvw[1])*365.25*0.0172020989)**2 + (float(uvw[2])*365.25*0.0172020989)**2
        a = (grav*r)/((2*grav) - (r*v2))
        h2 = ((float(xyz[1])*float(uvw[2])*365.25*0.0172020989)-(float(xyz[2])*float(uvw[1])*365.25*0.0172020989))**2 + ((float(xyz[2])*float(uvw[0])*365.25*0.0172020989)-(float(xyz[0])*float(uvw[2])*365.25*0.0172020989))**2 + ((float(xyz[0])*float(uvw[1])*365.25*0.0172020989)-(float(xyz[1])*float(uvw[0])*365.25*0.0172020989))**2
        ci = ((float(xyz[0])*float(uvw[1])*365.25*0.0172020989)-(float(xyz[1])*float(uvw[0])*365.25*0.0172020989)) / (h2**.5)
        if abs(ci) < 1.:
            inc = math.acos(ci) * 360. / 2. / math.pi
        else:
            if ci > 0.:
                inc = 0.
            if ci < 0.:
                inc = 180.
        e2 = 1. - (h2/grav/a)
        if e2 <= 0.:
            e = 0.
        else:
            e = e2**.5
        if mass*50000.>25.:
            print mass
        if mass > .05:
            line=np.asarray([name,str(a),str(e),str(inc),str(mass)])
            line.tofile(orbit,sep=' ',format='%10s')
            orbit.write('\n')
~                               
