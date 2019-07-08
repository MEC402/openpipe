#!/usr/bin/python

#run tests on series of images to find out their overlap numbers

#from skimage.measure import compare_ssim
import imgoverlap


#testOverlap('side1.png','side2.png');
#two bases
imgoverlap.chkOverlapTime('o:/panmasters/cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c/P1140647.RW2',
            "o:/panmasters\cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c\P1140648.RW2");

#random
imgoverlap.chkOverlapTime('o:/panmasters/cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c/P1140656.RW2',
            "o:/panmasters\cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c\P1140657.RW2");


# first get statistics for two identical black images
imgoverlap.chkOverlapTime('o:/panmasters/cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c/P1140572.RW2',
            "o:/panmasters\cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c\P1140573.RW2");

# check two identical images but not black
imgoverlap.chkOverlapTime('o:/panmasters/cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c/P1140590.RW2',
            "o:/panmasters\cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c\P1140590.RW2");

#check black against another image
imgoverlap.chkOverlapTime('o:/panmasters/cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c/P1140573.RW2',
            "o:/panmasters\cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c\P1140580.RW2");

#check two extremely different images
imgoverlap.chkOverlapTime('o:/panmasters/cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c/P1140646.RW2',
            "o:/panmasters\cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c\P1140647.RW2");

#check rotated but mismatched images
imgoverlap.chkOverlapTime('o:/panmasters/cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c/P1140627.RW2',
            "o:/panmasters\cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c\P1140628.RW2");

#blue sky to pano base
imgoverlap.chkOverlapTime('o:/panmasters/cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c/P1140817.RW2',
            "o:/panmasters\cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c\P1140818.RW2");
