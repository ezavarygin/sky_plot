from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from astropy.coordinates import SkyCoord
import sys


file_name = sys.argv[1]

# options --gal, --eq, --ham

projection_list = ['hammer', 'moll']
if '--ham' in sys.argv:
    projection = projection_list[0]
else:
    projection = projection_list[1]

p_size  = 2 # default rcParams['lines.markersize'] ** 2 which is 36
p_alpha = 1 #0.02 # transparency of the point to mimic a density map

# Coordinates
# -----------
cmb_l   = 263.99 # CMB dibole
cmb_b   = 48.26
cmb_c   = '#e41a1c' # color to use
alpha_l = 330.13 # Fine structure constant dipole (http://arxiv.org/abs/1202.4758)
alpha_b = -13.16
alpha_c = '#4daf4a'

dipoles =  {'CMB': [cmb_l,cmb_b,cmb_c], 'Alpha': [alpha_l,alpha_b,alpha_c]}

if '--eq' in sys.argv: # coordinates in file_name are (RA,DEC)
    ra_list, dec_list = np.loadtxt(file_name,unpack=True)
    gal_coord = SkyCoord(ra_list,dec_list,frame='fk5',unit='deg').galactic
    l_list = gal_coord.l.deg # longitude
    b_list = gal_coord.b.deg # latitude
elif '--gal' in sys.argv: # coordinates in file_name are (l,b)
    l_list, b_list = np.loadtxt(file_name,unpack=True)
    eq_coord = SkyCoord(l_list,b_list,frame='galactic',unit='deg').fk5
    ra_list  = eq_coord.ra.deg
    dec_list  = eq_coord.dec.deg


fig = plt.figure(figsize=(18,10))

ax1 = plt.subplot(121)
m = Basemap(projection=projection,lat_0=0,lon_0=0) #180)
m.drawparallels(np.arange(-90,90,30))
m.drawmeridians(np.arange(-180,180,60)) #(0,360,30))
ax1.set_title('Equatorial coordinates (RA, DEC) in degrees',y=1.08)
x, y = m(ra_list,dec_list)
m.scatter(x,y,s=p_size,marker='o',color='#377eb8',alpha=p_alpha)
# Markers:
gal_centre = SkyCoord(0.0,0.0,frame='galactic',unit='deg').fk5
gc_ra  = gal_centre.ra.degree
gc_dec = gal_centre.dec.degree
x, y = m(gc_ra,gc_dec)
m.scatter(x,y,s=50,marker='o',color='k') # Galactic centre
x, y = m(gc_ra+3.0,gc_dec-1.0)
ax1.text(x,y,'Gal Centre',color='black',fontsize=10,va='top',ha='left')
for key in dipoles.keys():
    dip_eq = SkyCoord(dipoles[key][0],dipoles[key][1],frame='galactic',unit='deg').fk5 # dipole
    dip_ra  = dip_eq.ra.degree
    dip_dec = dip_eq.dec.degree
    x, y = m(dip_ra,dip_dec) # direction
    m.scatter(x,y,s=50,marker='x',color=dipoles[key][2],lw=2.5)
    ax1.text(x,y,'{}'.format(key),color='black',fontsize=10,va='top',ha='right')
    x, y = m(dip_ra-180.0,-1.0*dip_dec) # anti-direction
    m.scatter(x,y,s=50,marker='x',color=dipoles[key][2],lw=2.5)
    #ax1.text(x,y,'{} South'.format(key),color='black',fontsize=10,va='bottom',ha='right')

ax2 = plt.subplot(122)
m = Basemap(projection=projection,lat_0=0,lon_0=0) #180)
m.drawparallels(np.arange(-90,90,30))
m.drawmeridians(np.arange(-180,180,60)) #(0,360,30))
ax2.set_title('Galactic coordinates (l, b) in degrees',y=1.08)
x, y = m(l_list,b_list)
m.scatter(x,y,s=p_size,marker='o',color='#377eb8',alpha=p_alpha)
# Markers:
x, y = m(0.0,0.0)
m.scatter(x,y,s=50,marker='o',color='k') # Galactic centre
x, y = m(3.0,-1.0)
ax2.text(x,y,'Gal Centre',color='black',fontsize=10,va='top',ha='left')
for key	in dipoles.keys():
    x, y = m(dipoles[key][0],dipoles[key][1]) # direction
    m.scatter(x,y,s=50,marker='x',color=dipoles[key][2],lw=2.5)
    ax2.text(x,y,'{}'.format(key),color='black',fontsize=10,va='top',ha='right')
    x, y = m(dipoles[key][0]-180.0,-1.0*dipoles[key][1]) # anti-direction
    m.scatter(x,y,s=50,marker='x',color=dipoles[key][2],lw=2.5)
    #ax1.text(x,y,'{} South'.format(key),color='black',fontsize=10,va='bottom',ha='right')

# Pole labels on the sphere
x,y = m(4,0)
ax1.text(x,y,r'(0,0)',color='black',fontsize=10,va='bottom',ha='left')
ax2.text(x,y,r'(0,0)',color='black',fontsize=10,va='bottom',ha='left')
x,y = m(180.01,0)
ax1.text(x,y,r'(180,0)',color='black',fontsize=10,va='center',ha='right')
ax2.text(x,y,r'(180,0)',color='black',fontsize=10,va='center',ha='right')
x,y = m(0,-90)
ax1.text(x,y,r'(0,-90)',color='black',fontsize=10,va='top',ha='center')
ax2.text(x,y,r'(0,-90)',color='black',fontsize=10,va='top',ha='center')
x,y = m(0,90)
ax1.text(x,y,r'(0,90)',color='black',fontsize=10,va='bottom',ha='center')
ax2.text(x,y,r'(0,90)',color='black',fontsize=10,va='bottom',ha='center')
x,y = m(180,0)
ax1.text(x,y,r'(180,0)',color='black',fontsize=10,va='center',ha='left')
ax2.text(x,y,r'(180,0)',color='black',fontsize=10,va='center',ha='left')
# Sub-labels on the axes:
for b in (-60,-30,30,60):
    x,y = m(180,b)
    if b<0:
        ax1.text(x,y,'$%d^{\circ}$'%b,color='black',fontsize=10,va='top',ha='left')
        ax2.text(x,y,'$%d^{\circ}$'%b,color='black',fontsize=10,va='top',ha='left')
    if b>0:
        ax1.text(x,y,r'$%d^{\circ}$'%b,color='black',fontsize=10,va='bottom',ha='left')
        ax2.text(x,y,r'$%d^{\circ}$'%b,color='black',fontsize=10,va='bottom',ha='left')
    for l in (60,120,240,300):
        x,y = m(l+1,0)
        ax1.text(x,y,r"$%d^{\circ}$"%l,color='black',fontsize=8,va='bottom',ha='left')
        ax2.text(x,y,r"$%d^{\circ}$"%l,color='black',fontsize=8,va='bottom',ha='left')

#plt.tight_layout()
plt.show()
