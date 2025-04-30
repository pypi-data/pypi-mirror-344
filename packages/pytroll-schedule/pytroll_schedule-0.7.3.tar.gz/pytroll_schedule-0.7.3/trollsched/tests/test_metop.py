from trollsched.tests.test_satpass import AREA_DEF_EURON1
from datetime import datetime, timedelta
from trollsched.satpass import Pass
from pytest import approx

def test_swath_coverage_metop():

    # ASCAT and AVHRR on Metop-B:
    tstart = datetime.strptime("2019-01-02T10:19:39", "%Y-%m-%dT%H:%M:%S")
    tend = tstart + timedelta(seconds=180)
    tle1 = '1 38771U 12049A   19002.35527803  .00000000  00000+0  21253-4 0 00017'
    tle2 = '2 38771  98.7284  63.8171 0002025  96.0390 346.4075 14.21477776326431'

    mypass = Pass('Metop-B', tstart, tend, instrument='ascat', tle1=tle1, tle2=tle2)
    cov = mypass.area_coverage(AREA_DEF_EURON1)
    assert cov == approx(0.322812, 1e-5)

    mypass = Pass('Metop-B', tstart, tend, instrument='avhrr', tle1=tle1, tle2=tle2)
    cov = mypass.area_coverage(AREA_DEF_EURON1)
    assert cov == approx(0.357324, 1e-5)

"""
ipdb> self.boundary.contour_poly.vertices
array([[-0.42303348,  1.28939237],
       [ 0.41048049,  1.21683896],
       [ 0.66291943,  1.11905917],
       ...,
       [-0.41794432,  1.27818009],
       [-0.41958141,  1.28191909],
       [-0.42127703,  1.28565653]])

ipdb> area_boundary.vertices
array([[-0.61051451,  1.28079079],
       [-0.59339491,  1.28413708],
       [-0.54370727,  1.29298512],
       [-0.49084709,  1.3011214 ],
       [-0.43482446,  1.30847522],
       [-0.37572982,  1.31497506],
       [-0.31374904,  1.3205508 ],
       [-0.24917444,  1.32513648],
ipdb> instrument
'ascat'
ipdb> scans_nb
674
ipdb> scanpoints
array([ 0, 41])
ipdb> scan_step
1
ipdb> scan_angle
55.25
ipdb> 

"""
