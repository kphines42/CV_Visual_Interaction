import cv2
import numpy as np

def build_filters(n):

    filters = []
    ksize = 31
    for theta in np.arange(0, np.pi, np.pi / n):
        params = {'ksize':(ksize, ksize), 'sigma':1.0, 'theta':theta, 'lambd':15.0,
                  'gamma':0.02, 'psi':0, 'ktype':cv2.CV_32F}
        kern = cv2.getGaborKernel(**params)
        kern /= 1.5*kern.sum()
        filters.append((kern,params))
    return filters
