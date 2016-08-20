''''
Author: Gurkirt Singh
Date: 20:08:2016

Main purpose of this script to help produce framelevel annotations for DALY dataset
This script helps to extract frames from video and store useful info about videos.

'''
import os as os
import numpy as np
import json,shutil

actions = ['ApplyingMakeUpOnLips', 'BrushingTeeth', 'CleaningFloor', 'CleaningWindows', 'Drinking', 'FoldingTextile', 'Ironing', 'Phoning', 'PlayingHarmonica', 'TakingPhotosOrVideos']

basedir = '../'; # you chaneg to the place whre you videos and images should be.

def extractframes(vids): # take all .mp4 videos and extract frames using ffmpeg
    for vid in vids:
        vidfile = basedir+'videos/'+vid+'.mp4'
        imgdir = basedir+'images/'+vid+'/'
        if not os.path.isdir(imgdir):
            os.mkdir(imgdir)
            cmd = 'ffmpeg -i {} -qscale:v 5 {}%05d.jpg'.format(vidfile,imgdir); #-vsync 0
            # PNG format is very storage heavy so I choose jpg.
            # images will be generated in JPG format with quality scale = 5; you can adjust according to you liking 
            # In appearence it doen't look that deblurred as opposed to default settings by ffmpeg
            # @v 5 images will take alomst 145GB
            print cmd
            os.system(cmd)

def saveVidInfo(vids):
    vidinfo = dict();
    count = 0;
    for vid in vids:
        vidfile = basedir+'videos/'+vid+'.mp4'
        imgdir = basedir+'images/'+vid+'/'
        imglist = os.listdir(imgdir);
        imglist = [i for i in imglist if i.endswith('.jpg')];
        cmd  = 'ffprobe -v quiet -print_format json  -show_streams -count_frames {} >>temp{}.json'.format(vidfile,'0')
        # -count_frames option takes the most of the time to run ffprobe
        print cmd
        os.system(cmd)
        with open('temp{}.json'.format(count)) as f:
            ffdata = json.load(f)

        if ffdata["streams"][0]['codec_type'] == 'video':
            ffdata = ffdata["streams"][0]
        else:
            ffdata = ffdata["streams"][1]
    
        os.remove('temp{}.json'.format('0'))
        vinfo = dict();
        vinfo['duration']=float(ffdata['duration']);
        vinfo['nbframes']=len(imglist) #int(ffdata['nb_frames']);
        vinfo['ffprobeNbFrames']=int(ffdata['nb_frames']); #ffprobeNbFrames and nbframes are not always same (in case of variable fps vidoes)
        vinfo['frame_rate_info'] = ffdata['r_frame_rate']+'/'+ffdata['avg_frame_rate'] # frame rate info provided by ffprobe doen't match with ffmpeg number of frames always
        vinfo['fps'] = float(vinfo['nbframes'])/vinfo['duration']; # compute fps
        vidinfo[vid] = vinfo;
        print vinfo       
    
    with open('../hfiles/videoInfo.json','w') as f:
         json.dump(vidinfo,f)
        
if __name__ == '__main__':
    downloaded = os.listdir(basedir+'videos') # get list of file
    downloaded = [d for d in downloaded if d.endswith('.mp4')]  # keep only .mp4 files
    print 'number of videos downloded are ', len(downloaded) 
    with open('../hfiles/video_ids.txt') as f: 
        vids = f.readlines(); # read video ids 
    vids = [d.rstrip('\n') for d in vids]  # remove \n
    
    ############################
    #extractframes(vids)
    ###########################
    
    saveVidInfo(vids)