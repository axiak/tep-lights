cimport cdmx
cimport python_exc

import traceback
import time
import os

cdef class RGBPixel:
    cdef cdmx.RGBPixel * _rgbpixel
    cdef int row
    cdef int col
    cdef int created

    def __cinit__(self, int row, int col, int create=1):
        if not create:
            self.created = 0
        else:
            self._rgbpixel = cdmx.rgbpixel_create(0, 0, 0, 1)
            self.created = 1
            if self._rgbpixel is NULL:
                python_exc.PyErr_NoMemory()

    def __dealloc__(self):
        if self.created and self._rgbpixel is not NULL:
            cdmx.rgbpixel_destroy(self._rgbpixel)

    property r:
        def __get__(self):
            return self._rgbpixel.red
        def __set__(self, float val):
            self._rgbpixel.red = val
    property g:
        def __get__(self):
            return self._rgbpixel.green
        def __set__(self, float val):
            self._rgbpixel.green = val
    property b:
        def __get__(self):
            return self._rgbpixel.blue
        def __set__(self, float val):
            self._rgbpixel.blue = val
    property alpha:
        def __get__(self):
            return self._rgbpixel.alpha
        def __set__(self, float val):
            self._rgbpixel.alpha = val

    property row:
        def __get__(self):
            return self.row
        def __set__(self, int val):
            self.row = val
    property col:
        def __get__(self):
            return self.col
        def __set__(self, int val):
            self.col = val

    def setrgb(self, float red, float green, float blue):
        cdmx.rgbpixel_setvalue(self._rgbpixel,
                               red, green, blue, self._rgbpixel.alpha)

    def sethue(self, float hue, float brightness, float saturation):
        cdmx.rgbpixel_sethbsvalue(self._rgbpixel,
                                  hue, brightness, saturation,
                                  self._rgbpixel.alpha)

    def __repr__(self):
         return "<RGBPixel (%0.3f, %0.3f, %0.3f)>" % (self.red, self.green, self.blue)

cdef class DefaultLightPanel:
    cdef cdmx.ColorLayer * layer
    cdef cdmx.LocalData * s
    cdef double t
    cdef list _lights

    def __cinit__(self, int id=222):
        cdef int r, c
        cdef bytes name = "boo"
        stack = traceback.extract_stack(limit=10)
        if stack:
            name = os.path.basename(stack[0][0])
            name = name.rsplit('.', 1)[0]
        self.s = cdmx.plugin_register(name, id)
        if self.s is NULL:
            raise RuntimeError("Unable to register plugin")

        self.layer = self.s.layer
        self.t = time.time()
        self._lights = []
        cdef list A
        cdef cdmx.RGBPixel * led
        cdef RGBPixel led2

        for r from 0 <= r < self.layer.height:
            A = []
            for c from 0 <= c < self.layer.width:
                led = cdmx.colorlayer_getpixel(self.layer, c, r)
                led.alpha = 1
                led2 = RGBPixel(r, c, 0)
                led2._rgbpixel = led
                A.append(led2)
            self._lights.append(A)

    def __dealloc__(self):
        self.layer = NULL
        cdmx.serverdata_destroy(self.s)


    property height:
        def __get__(self):
            return self.layer.height

    property width:
        def __get__(self):
            return self.layer.width

    def output(self):
        cdmx.serverdata_commitlayer(self.s)
        #cdmx.serverdata_update(self.s)


    def _wait(self, float fps):
        curtime = time.time()
        endtime = curtime - self.t
        if 1.0 / fps > endtime:
            time.sleep(1.0 / fps - endtime)
        self.t = time.time()

    def setall_rgb(self, float red, float green, float blue):
        cdmx.colorlayer_setall(self.layer, red, green, blue, 1)

    def setall_hbs(self, float hue, float brightness, float saturation):
        cdef cdmx.RGBPixel * led = cdmx.colorlayer_getpixel(self.layer, 0, 0)
        cdmx.rgbpixel_sethbsvalue(led, hue, brightness, saturation, 1)
        cdmx.colorlayer_setall(self.layer, led.red, led.green, led.blue, 1)

    def outputAndWait(self, float fps):
        self.output()
        self._wait(fps)


    property lights:
        def __get__(self):
            return self._lights

def getDefaultPanel():
    return DefaultLightPanel()
