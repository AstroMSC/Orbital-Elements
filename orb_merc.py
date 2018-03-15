import glob
import math
import numpy as np

sim_dir = raw_input("Enter the filepath to the big.dmp files (eg /users/yourname/mercury/*) :")
grav = 4. * math.pi * math.pi

def orb(dmp_f):
    sim_loc = dmp_f.replace('big.in','')
    orbits = sim_loc + 'orbits.txt'
    orbit=open(orbits,'a')
    line=np.asarray(['body','a','e','i','long','arg','mean','mass'])
    line.tofile(orbit,sep=' ',format='%10s')
    orbit.write('\n')
    with open(dmp_f,'r') as file:
        data = file.readlines()
    for k in range(6):
        del data[0]
    for l in range(int(len(data)/4.)):
        name = data[l*4].split(' ',1)[0]
        mass = data[l*4].split('m= ',1)[-1]
        mass = mass.split()
        mass = float(mass[0]) / 0.000003003
        xyz = data[(l*4)+1]
        uvw = data[(l*4)+2]
        xyz = xyz.split()
        uvw = uvw.split()
        r = (float(xyz[0])**2 + float(xyz[1])**2 + float(xyz[2])**2)**.5
        v2 = (float(uvw[0])*365.25)**2 + (float(uvw[1])*365.25)**2 + (float(uvw[2])*365.25)**2
        a = (grav*r)/((2*grav) - (r*v2))
        rv = (float(xyz[0])*float(uvw[0])) + (float(xyz[1])*float(uvw[1])) + (float(xyz[2])*float(uvw[2]))
        hx = (float(xyz[1])*float(uvw[2])*365.25)-(float(xyz[2])*float(uvw[1])*365.25)
        hy = (float(xyz[2])*float(uvw[0])*365.25)-(float(xyz[0])*float(uvw[2])*365.25)
        hz = (float(xyz[0])*float(uvw[1])*365.25)-(float(xyz[1])*float(uvw[0])*365.25)
        h2 = hx**2 + hy**2 + hz**2
        ci = hz / (h2**.5)
        if abs(ci) < 1.:
            inc = math.acos(ci) * 360. / 2. / math.pi
            long = np.arctan2(hx,-hy)
            if long < 0.:
                long = long + (2.*math.pi)
        else:
            long = 0.
            if ci > 0.:
                inc = 0.
            if ci < 0.:
                inc = 180.
        e2 = 1. - (h2/grav/a)
        if e2 <= 0.:
            e = 0.
        else:
            e = e2**.5
        if hy != 0.:
            to = -hx/hy
            temp = (1. - ci) * to
            tmp2 = to * to
            true = np.arctan2((float(xyz[1])*(1.+(tmp2*ci))-(float(xyz[0])*temp)),((float(xyz[0])*(tmp2+ci))-(float(xyz[1])*temp)))
        else:
            true = np.arctan2(float(xyz[1]) * ci, float(xyz[0]))
        if ci < 0.:
            true = true + math.pi
        if e < 3.e-8:
            p = 0.
            l = true
        else:
            ce = (v2*r - grav) / (e*grav)
            if e < 1.:
                if ce > 1.:
                    ce = 1.
                if ce < -1.:
                    ce = -1.
                bige = np.arccos(ce)
                if rv < 0.:
                    bige = (2.*math.pi) - bige
                l = bige - (e*np.sin(bige))
            #else Hyperbolic orbit
            s = h2/grav
            cf = (s - r) / (e*r)
            if cf > 1.:
                cf = 1.
            if cf < -1.:
                cf = -1.
            f = np.arccos(cf)
            if rv < 0.:
                f = (2.*math.pi) - f
            p = true - f
            p = np.mod(p, 2*math.pi)
        l = np.mod(l,2*math.pi)
        arg = np.mod((p - long)*360./2./math.pi,360.)
        mean = l*360./2./math.pi
        long = long*360./2./math.pi
        line=np.asarray([name,str(a),str(e),str(inc),str(long),str(arg),str(mean),str(mass)])
        line.tofile(orbit,sep=' ',format='%10s')
        orbit.write('\n')

for dump in glob.glob(sim_dir + '/big.in'):
    orb(dump)
