from trollsched.satpass import Pass, Mapper
from trollsched.boundary import AreaDefBoundary
from satpy.resample import get_area_def
from datetime import datetime
import matplotlib.pyplot as plt

def read_time(timestr):
    return datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%S.%f')

n19tle = ["1 33591U 09005A   17340.57650845  .00000094  00000-0  76245-4 0  9991", "2 33591  99.1170 310.0500 0014454 144.4325 215.7812 14.12234917454722"]

npptle = ["1 37849U 11061A   17341.18384787 -.00000170  00000-0 -59794-4 0  9990",
"2 37849  98.7173 277.4064 0001444  51.2876 308.8431 14.19554784316634"]

aquatle = ["1 27424U 02022A   17340.60803505  .00000124  00000-0  37565-4 0  9994", "2 27424  98.2224 279.4549 0000867   0.5694 121.8047 14.57112403829339"]

n15tle = ["1 25338U 98030A   17340.56480162  .00000017  00000-0  25914-4 0  9991", "2 25338  98.7780 351.7884 0011511  68.7192 291.5215 14.25829330 17314"]

mbtle = ["1 38771U 12049A   17340.57962451  .00000010  00000-0  24541-4 0  9997", "2 38771  98.7014  38.0881 0002160 108.6009 358.0369 14.21488767270773"]

n18tle = ["1 28654U 05018A   17340.55743082 -.00000000  00000-0  25127-4 0  9990", "2 28654  99.1682   6.8676 0013581 310.4609  49.5377 14.12359673646491"]


p2 = Pass('Suomi NPP', read_time('2017-12-07T13:01:35.0'), read_time('2017-12-07T13:15:26.35'), tle1=npptle[0], tle2=npptle[1])

p3 = Pass('EOS Aqua', read_time('2017-12-07T13:16:08.5'), read_time('2017-12-07T13:28:23.16'), tle1=aquatle[0], tle2=aquatle[1])

p4 = Pass('NOAA-15', read_time('2017-12-07T13:22:50.1'), read_time('2017-12-07T13:34:19.65'), tle1=n15tle[0], tle2=n15tle[1])

p5 = Pass('Metop B', read_time('2017-12-07T13:26:19.5'), read_time('2017-12-07T13:35:51.45'), tle1=mbtle[0], tle2=mbtle[1])

p6 = Pass('NOAA-18', read_time('2017-12-07T13:28:11.3'), read_time('2017-12-07T13:39:01.85'), tle1=n18tle[0], tle2=n18tle[1])

p1 = Pass('NOAA-19', read_time('2017-12-07T13:47:16.0'), read_time('2017-12-07T14:03:02.5'), tle1=n19tle[0], tle2=n19tle[1])


#plt.clf()

ar = AreaDefBoundary(get_area_def('euron1'))

cm = plt.get_cmap('plasma')
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111)
NUM_COLORS=6
ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

def frpass(satpass):
    return satpass.satellite + " " + satpass.uptime.strftime('%H:%M:%S')

with Mapper() as mapper:
    water = (.97, .99, 1)
    mapper.drawmapboundary(fill_color=water)
    mapper.fillcontinents(color=(.97, .99, .97),lake_color=water, zorder=2)
    #mapper.shadedrelief()
    lon = 16.2
    lat = 58.6
    x,y = mapper(lon, lat)
    mapper.plot(x, y, 'r*', markersize=15)
    p2.draw(mapper, '-', label=frpass(p2))
    p3.draw(mapper, ':', label=frpass(p3))
    p4.draw(mapper, ':', label=frpass(p4))
    p5.draw(mapper, '-', label=frpass(p5))
    p6.draw(mapper, ':', label=frpass(p6))
    p1.draw(mapper, '-', label=frpass(p1))
    ar.contour_poly.draw(mapper, '--r', label='Area of Interest')

    ax.legend()
#plt.show()
plt.savefig('destination_path.pdf', format='pdf')
