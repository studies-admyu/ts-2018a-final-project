#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from model.camera_shake_filter import CameraShakeFilter

import matplotlib.pylab as pl

if __name__ == '__main__':
    flt = CameraShakeFilter(m = 15, p_s = 0.9)
    
    pl.figure()
    pl.imshow(flt.get_kernel(117.0), cmap = 'gray')
    pl.show()
