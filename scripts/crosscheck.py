''''
Author: Gurkirt Singh
Date: 20:08:2016

Main purpose of this script to help produce framelevel annotations for DALY dataset
This script helps to extract frames from video and store useful info about videos.

'''
import os as os
import numpy as np
import json,shutil,pickle

actions = ['ApplyingMakeUpOnLips', 'BrushingTeeth', 'CleaningFloor', 'CleaningWindows', 'Drinking', 'FoldingTextile', 'Ironing', 'Phoning', 'PlayingHarmonica', 'TakingPhotosOrVideos']

basedir = '../'; # you chaneg to the place whre you videos and images should be.

def extractframes(vids): # take all .mp4 videos and extract frames using ffmpeg
    for vid in vids:
        vidfile = basedir+'videos/'+vid+'.mp4'
        imgdir = basedir+'images/'+vid+'/'
        if not os.path.isdir(imgdir):
            os.mkdir(imgdir)
        cmd = 'ffmpeg -i {} -qscale:v 5 -vf decimate=-0:99999 {}%05d.jpg'.format(vidfile,imgdir); #-vsync 0
        print cmd
        os.system(cmd)
            # PNG format is very storage heavy so I choose jpg.
            # images will be generated in JPG format with quality scale = 5; you can adjust according to you liking 
            # In appearence it doen't look that deblurred as opposed to default settings by ffmpeg
            # @v 5 images will take alomst 145GB
            

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
        
        # ffdata = ffdata["streams"][0]
        os.remove('temp{}.json'.format('0'))
        vinfo = dict();
        vinfo['duration']=float(ffdata['duration']);
        vinfo['nbframes']=len(imglist) #int(ffdata['nb_frames']);
        vinfo['ffprobeNbFrames']=int(ffdata['nb_frames']); #ffprobeNbFrames and nbframes are not always same (in case of variable fps vidoes)
        vinfo['frame_rate_info'] = ffdata['r_frame_rate']+'/'+ffdata['avg_frame_rate'] # frame rate info provided by ffprobe doen't match with ffmpeg number of frames always
        vinfo['fps'] = float(vinfo['nbframes'])/vinfo['duration']; # compute fps
        vidinfo[vid] = vinfo;
        print vinfo
    
    
    #with open('../hfiles/videoInfo.json','w') as f:
    #     json.dump(vidinfo,f)
        
if __name__ == '__main__':
    #downloaded = os.listdir(basedir+'videos') # get list of file
    #downloaded = [d for d in downloaded if d.endswith('.mp4')]  # keep only .mp4 files.
    #print 'number of videos downloded are ', len(downloaded) 
    with open('../hfiles/video_ids.txt') as f: 
        vids = f.readlines(); # read video ids 
    vids = [d.rstrip('\n') for d in vids]  # remove \n
    with open('../hfiles/daly1.1.0.pkl') as f:
        daly = pickle.load(f);
    with open('../hfiles/videoInfo.json') as f:
        jdaly = json.load(f);
    metadata = daly['metadata'];
    count =0;
    tempvids = [];
    for vid in vids:
        
        imgdir = basedir+'rgb-images/'+vid+'/'
        #flowdir = basedir+'motion-images/'+vid+'/'
        if not os.path.isdir(imgdir):
             os.mkdir(imgdir)
        #if not os.path.isdir(flowdir):
        #     os.mkdir(flowdir)
        imglist = os.listdir(imgdir)
        imglist = [i for i in imglist if i.endswith('.jpg')];
        num_frames = len(imglist);
        nbframes_ffmpeg = metadata[vid+'.mp4']['nbframes_ffmpeg']
        duration =  metadata[vid+'.mp4']['duration']
        #duration = metadata[vid+'.mp4']['duration']
        jduration = jdaly[vid]['duration']
        #duration = metadata[vid+'.mp4']['nbframes_ffmpeg']
        diffs = abs(metadata[vid+'.mp4']['nbframes_ffmpeg']  - num_frames);
        if abs(duration-jduration)>0.2:
            #shutil.rmtree(imgdir)
            #shutil.rmtree(flowdir)
            tempvids.append(vid)
            print vid, '.mp4 nbframes_ffmpeg ', nbframes_ffmpeg,  ' duration ', metadata[vid+'.mp4']['duration'] , ' fps ', metadata[vid+'.mp4']['fps'] , ' number of extracted frames ',num_frames,  ' duration ',jduration,' fps ', jdaly[vid]['fps']
            count +=1;
    print 'diff in ', count
    # for v in tempvids:
    #     cmd = "wget --user privateuser --password pltbd21aocolnq http://pascal.inrialpes.fr/data2/daly_cache/cache/"+v+".mp4 -O /mnt/jupiter-beta/DALY/videos/"+v+".mp4"
    #     os.system(cmd)
    # extractframes(tempvids)
    
        
    
        
        
