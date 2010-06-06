#!/usr/bin/python
# Copyright 2004 Michael Edwards
# Licensed under the GPL.  See attached LICENSE.txt
# based on this perl script:
# http://www.geo.fmi.fi/~tmakinen/bin/kwrgb.cgi
# by Teemu Makinen (teemu.makinen@fmi.fi)

import math, string, cgi

class kwrgb:
    cie = (
      ( 390,  (1.83970E-3, -4.53930E-4,  1.21520E-2 )),
      ( 395,  (4.61530E-3, -1.04640E-3,  3.11100E-2 )),
      ( 400,  (9.62640E-3, -2.16890E-3,  6.23710E-2 )),
      ( 405,  (1.89790E-2, -4.43040E-3,  1.31610E-1 )),
      ( 410,  (3.08030E-2, -7.20480E-3,  2.27500E-1 )),
      ( 415,  (4.24590E-2, -1.25790E-2,  3.58970E-1 )),
      ( 420,  (5.16620E-2, -1.66510E-2,  5.23960E-1 )),
      ( 425,  (5.28370E-2, -2.12400E-2,  6.85860E-1 )),
      ( 430,  (4.42870E-2, -1.99360E-2,  7.96040E-1 )),
      ( 435,  (3.22200E-2, -1.60970E-2,  8.94590E-1 )),
      ( 440,  (1.47630E-2, -7.34570E-3,  9.63950E-1 )),
      ( 445, (-2.33920E-3,  1.36900E-3,  9.98140E-1 )),
      ( 450, (-2.91300E-2,  1.96100E-2,  9.18750E-1 )),
      ( 455, (-6.06770E-2,  4.34640E-2,  8.24870E-1 )),
      ( 460, (-9.62240E-2,  7.09540E-2,  7.85540E-1 )),
      ( 465, (-1.37590E-1,  1.10220E-1,  6.67230E-1 )),
      ( 470, (-1.74860E-1,  1.50880E-1,  6.10980E-1 )),
      ( 475, (-2.12600E-1,  1.97940E-1,  4.88290E-1 )),
      ( 480, (-2.37800E-1,  2.40420E-1,  3.61950E-1 )),
      ( 485, (-2.56740E-1,  2.79930E-1,  2.66340E-1 )),
      ( 490, (-2.77270E-1,  3.33530E-1,  1.95930E-1 )),
      ( 495, (-2.91250E-1,  4.05210E-1,  1.47300E-1 )),
      ( 500, (-2.95000E-1,  4.90600E-1,  1.07490E-1 )),
      ( 505, (-2.97060E-1,  5.96730E-1,  7.67140E-2 )),
      ( 510, (-2.67590E-1,  7.01840E-1,  5.02480E-2 )),
      ( 515, (-2.17250E-1,  8.08520E-1,  2.87810E-2 )),
      ( 520, (-1.47680E-1,  9.10760E-1,  1.33090E-2 )),
      ( 525, (-3.51840E-2,  9.84820E-1,  2.11700E-3 )),
      ( 530,  (1.06140E-1,  1.03390, -4.15740E-3 )),
      ( 535,  (2.59810E-1,  1.05380, -8.30320E-3 )),
      ( 540,  (4.19760E-1,  1.05120, -1.21910E-2 )),
      ( 545,  (5.92590E-1,  1.04980, -1.40390E-2 )),
      ( 550,  (7.90040E-1,  1.03680, -1.46810E-2 )),
      ( 555,  (1.00780,  9.98260E-1, -1.49470E-2 )),
      ( 560,  (1.22830,  9.37830E-1, -1.46130E-2 )),
      ( 565,  (1.47270,  8.80390E-1, -1.37820E-2 )),
      ( 570,  (1.74760,  8.28350E-1, -1.26500E-2 )),
      ( 575,  (2.02140,  7.46860E-1, -1.13560E-2 )),
      ( 580,  (2.27240,  6.49300E-1, -9.93170E-3 )),
      ( 585,  (2.48960,  5.63170E-1, -8.41480E-3 )),
      ( 590,  (2.67250,  4.76750E-1, -7.02100E-3 )),
      ( 595,  (2.80930,  3.84840E-1, -5.74370E-3 )),
      ( 600,  (2.87170,  3.00690E-1, -4.27430E-3 )),
      ( 605,  (2.85250,  2.28530E-1, -2.91320E-3 )),
      ( 610,  (2.76010,  1.65750E-1, -2.26930E-3 )),
      ( 615,  (2.59890,  1.13730E-1, -1.99660E-3 )),
      ( 620,  (2.37430,  7.46820E-2, -1.50690E-3 )),
      ( 625,  (2.10540,  4.65040E-2, -9.38220E-4 )),
      ( 630,  (1.81450,  2.63330E-2, -5.53160E-4 )),
      ( 635,  (1.52470,  1.27240E-2, -3.16680E-4 )),
      ( 640,  (1.25430,  4.50330E-3, -1.43190E-4 )),
      ( 645,  (1.00760,  9.66110E-5, -4.08310E-6 )),
      ( 650,  (7.86420E-1, -1.96450E-3,  1.10810E-4 )),
      ( 655,  (5.96590E-1, -2.63270E-3,  1.91750E-4 )),
      ( 660,  (4.43200E-1, -2.62620E-3,  2.26560E-4 )),
      ( 665,  (3.24100E-1, -2.30270E-3,  2.15200E-4 )),
      ( 670,  (2.34550E-1, -1.87000E-3,  1.63610E-4 )),
      ( 675,  (1.68840E-1, -1.44240E-3,  9.71640E-5 )),
      ( 680,  (1.20860E-1, -1.07550E-3,  5.10330E-5 )),
      ( 685,  (8.58110E-2, -7.90040E-4,  3.52710E-5 )),
      ( 690,  (6.02600E-2, -5.67650E-4,  3.12110E-5 )),
      ( 695,  (4.14800E-2, -3.92740E-4,  2.45080E-5 )),
      ( 700,  (2.81140E-2, -2.62310E-4,  1.65210E-5 )),
      ( 705,  (1.91170E-2, -1.75120E-4,  1.11240E-5 )),
      ( 710,  (1.33050E-2, -1.21400E-4,  8.69650E-6 )),
      ( 715,  (9.40920E-3, -8.57600E-5,  7.43510E-6 )),
      ( 720,  (6.51770E-3, -5.76770E-5,  6.10570E-6 )),
      ( 725,  (4.53770E-3, -3.90030E-5,  5.02770E-6 )),
      ( 730,  (3.17420E-3, -2.65110E-5,  4.12510E-6 )))
    
    def convertKRGB(self,kelvinRef,kelvinCon, returnWeb = 0): 
        if kelvinRef < 500:
            kelvinRef = 4000
        
        colorRef = [0,0,0]
        colorCon = [0,0,0]
        colorRGB = [0,0,0]
        
        for wavelength in kwrgb.cie:
            waveMilli = wavelength[0] * 1.0E-6 
            convertFactorRef = 1/((waveMilli * 1.0E3)**3 * (math.exp(14.3877/(kelvinRef*waveMilli))-1))
            convertFactorCon = 1/((waveMilli * 1.0E3)**3 * (math.exp(14.3877/(kelvinCon*waveMilli))-1))
            for component in range(0,3):
                colorRef[component] = colorRef[component] + convertFactorRef * wavelength[1][component]
                colorCon[component] = colorCon[component] + convertFactorCon * wavelength[1][component]
        
        maxComponent = 0

        for component in range(0,3):
            colorCon[component] = colorCon[component]/colorRef[component]
            if colorCon[component] < 0:
                colorCon[component] = 0
            if colorCon[component] >  maxComponent:
                maxComponent = colorCon[component]
        
        if maxComponent > 0:
            for component in range(0,3):
                colorRGB[component] = int(int(colorCon[component] * 65535/maxComponent + 0.5)/256 - 0.5)
                
        #print "R: %d G: %d B: %d" % (colorRGB[0],colorRGB[1],colorRGB[2])
        colorWeb = "#%s%s%s" % (hex(colorRGB[0])[2:],hex(colorRGB[1])[2:],hex(colorRGB[2])[2:])
        if returnWeb:
            return colorWeb
        else:
            return (colorRGB[0],colorRGB[1],colorRGB[2])


def main():
    import sys
    kcon = kwrgb()
    kelvinRef,  kelvinCon = int(sys.argv[1]), int(sys.argv[2])
    bgColor = kcon.convertKRGB(kelvinRef,kelvinCon, False)
    print bgColor

if __name__ == "__main__":
    main()
    import sys
    sys.exit(0)
    def writeForm(kelvinRef = 4000, kelvinCon = 4000, bgColor = (255,255,255)):
    	bgHex = "#%s%s%s" % (hex(bgColor[0])[2:],hex(bgColor[1])[2:],hex(bgColor[2])[2:])
        print "Content-type: text/html\n\n"
        print """<HTML>
            <TITLE>Kelvin to RGB converter</TITLE>"""
        print "             <BODY BGCOLOR=\"%s\">" % bgHex
        print """                <FORM ACTION="kwrgb.py" METHOD="get">
                    <LABEL>Kelvin reference: </LABEL>
                    <INPUT NAME="kelvinRef"/><BR/>
                    <LABEL>Kelvin color to convert: </LABEL>
                    <INPUT NAME="kelvinCon"/>
                    <INPUT TYPE="submit"/>
                </FORM>
	"""
	print "<br/>RGB: R: %d G: %d B: %d" % bgColor
	print """</BODY>
        </HTML>"""

    kcon = kwrgb()
    form = cgi.FieldStorage()
    if form.has_key("kelvinRef") and form.has_key("kelvinCon"):
        kelvinRef = int(form["kelvinRef"].value)
        kelvinCon = int(form["kelvinCon"].value)
    else:
        kelvinRef = 15000
        kelvinCon = 15000        
    print kelvinRef, kelvinCon
    bgColor = kcon.convertKRGB(kelvinRef,kelvinCon, False)
    writeForm(kelvinRef, kelvinCon, bgColor)
    
