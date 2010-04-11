
cdef extern from "cdmx/dmx.h":
    ctypedef struct RGBLed:
        float red
        float green
        float blue

    ctypedef struct LEDArray:
        RGBLed * led
        size_t size

    ctypedef struct DMXPanel:
        LEDArray * leds

    ctypedef struct DMXPanelCollection:
        DMXPanel ** panels
        int width
        int height
        int _ledwidth
        int _ledheight

cdef extern from "cdmx/ipcstructs.h":
    ctypedef struct RGBPixel:
        float red
        float green
        float blue
        float alpha

    RGBPixel * rgbpixel_create(float red, float green, float blue, float alpha)
    void rgbpixel_destroy(RGBPixel * pixel)
    RGBPixel * rgbpixel_sethbsvalue(RGBPixel * led, float hue, float brightness, float saturation, float alpha)
    RGBPixel * rgbpixel_setvalue(RGBPixel * pixel, float red, float green, float blue, float alpha)

    ctypedef struct ColorLayer:
        RGBPixel *pixels
        int width
        int height

    void colorlayer_setall(ColorLayer * layer, float red, float green, float blue, float alpha)
    RGBPixel * colorlayer_getpixel(ColorLayer * layer, int x, int y)
    ColorLayer * colorlayer_add(ColorLayer * dst, ColorLayer * src)
    ColorLayer * colorlayer_mult(ColorLayer * dst, ColorLayer * src)
    ColorLayer * colorlayer_superpose(ColorLayer * top, ColorLayer * bottom)
    ColorLayer * colorlayer_copy(ColorLayer * dst, ColorLayer * src)
    ColorLayer * colorlayer_create()
    void colorlayer_destroy(ColorLayer * layer)
    void colorlayer_pushtocollection(DMXPanelCollection * cltn, ColorLayer * layer)
    ColorLayer * colorlayer_addalpha(ColorLayer * dst, ColorLayer * src)

cdef extern from "cdmx/plugin.h":
    ctypedef struct LocalData:
         int shmid
         unsigned long old_frame_counter
         ColorLayer * layer

    LocalData * plugin_register(char * filename, int id)
    int serverdata_update(LocalData * data)
    void serverdata_destroy(LocalData * data)
    void serverdata_commitlayer(LocalData * data)
