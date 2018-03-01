#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import numpy.random as npr

from skimage.draw import line_aa

class CameraShakeFilter:
    PI = np.arctan(1.0) * 4.0
    COMPLEX_COMPONENTS_COUNT = 2
    
    def __init__(self, m = 2000, l_max = 60, p_s = 0.001):
        assert isinstance(m, int)
        assert isinstance(l_max, int)
        float(p_s)
        assert m > 1
        assert l_max > 0
        
        self._m = m
        self._l_max = l_max
        self._p_s = np.abs(p_s)
        self._STEP_LENGTH = float(self._l_max) / (self._m - 1)
    
    @staticmethod
    def complex_multiply(a, b):
        original_shape = a.shape if len(a.shape) > len(b.shape) else b.shape
        
        a = np.atleast_2d(a)
        b = np.atleast_2d(b)
        
        assert a.shape[0] == b.shape[0]
        assert a.shape[1] == CameraShakeFilter.COMPLEX_COMPONENTS_COUNT
        assert b.shape[1] == CameraShakeFilter.COMPLEX_COMPONENTS_COUNT
        
        result = np.zeros(a.shape)
        result[:, 0] = a[:, 0] * b[:, 0] - a[:, 1] * b[:, 1]
        result[:, 1] = a[:, 0] * b[:, 1] + a[:, 1] * b[:, 0]
        return np.reshape(result, original_shape)
    
    def get_kernel(self, noise):
        npr.seed(int(noise))
        
        phi = 0.2 * self.PI
        v = np.array([np.cos(phi), np.sin(phi)]) * self._STEP_LENGTH
        
        # For code correction mistakes
        assert v.size == self.COMPLEX_COMPONENTS_COUNT
        
        x = np.zeros((self._m, self.COMPLEX_COMPONENTS_COUNT))
        next_dir = np.zeros(self.COMPLEX_COMPONENTS_COUNT)
        
        for i in range(self._m - 1):
            p_b = npr.uniform(0.0, 0.2)
            p_g = npr.uniform(0.0, 0.7)
            I = npr.uniform(0.0, 0.2)
            
            next_dir[:] = 0.0
            if npr.rand() < p_b * self._p_s:
                phi = self.PI + npr.rand() - 0.5
                next_dir = self.complex_multiply(
                    2.0 * v, np.array([np.cos(phi), np.sin(phi)])
                )
            
            dv = next_dir + self._p_s * self.complex_multiply(
                p_g * npr.rand(self.COMPLEX_COMPONENTS_COUNT),
                I * self._STEP_LENGTH * x[i, :]
            )
            
            v += dv
            v *= self._STEP_LENGTH / np.linalg.norm(v)
            
            x[i + 1, :] = x[i, :] + v
        
        kernel_size = self._l_max + (self._l_max + 1) % 2
        kernel = np.zeros((kernel_size, kernel_size))
        
        x = (x - x.mean(axis = 0)).astype(np.int)
        x += kernel_size // 2 + 1
        
        last_x = x[0, :].copy()
        for i in range(1, self._m):
            if (last_x != x[i, :]).any():
                rr, cc, vl = line_aa(last_x[0], last_x[1], x[i, 0], x[i, 1])
                kernel[rr, cc] = vl
                
                last_x = x[i, :].copy()
        
        return kernel
