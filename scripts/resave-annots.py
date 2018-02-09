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

basedir = '../' # you chaneg to the place whre you videos and images should be.

# ffdata = ffdata["streams"][0]
# os.remove('temp{}.json'.format('0'))
# vinfo = dict();
# vinfo['duration']=float(ffdata['duration']);
# vinfo['nbframes']=len(imglist) #int(ffdata['nb_frames']);
# vinfo['ffprobeNbFrames']=int(ffdata['nb_frames']); #ffprobeNbFrames and nbframes are not always same (in case of variable fps vidoes)
# vinfo['frame_rate_info'] = ffdata['r_frame_rate']+'/'+ffdata['avg_frame_rate'] # frame rate info provided by ffprobe doen't match with ffmpeg number of frames always
# vinfo['fps'] = float(vinfo['nbframes'])/vinfo['duration']; # compute fps
# vidinfo[vid] = vinfo;
# print vinfo

def pre_proocess_split(split_vids, vids):
    testvideos = []
    for sv in split_vids[0]:
        sv = sv.split('.')[0]
        if sv in vids:
            testvideos.append(sv)
        else:
            print(sv, ' is not part of videolist')

if __name__ == '__main__':
    #downloaded = os.listdir(basedir+'videos') # get list of file
    #downloaded = [d for d in downloaded if d.endswith('.mp4')]  # keep only .mp4 files.
    #print 'number of videos downloded are ', len(downloaded)
    finalannots = dict()
    with open('../hfiles/video_ids.txt','r') as f:
        vids = f.readlines()
    vids = [d.rstrip('\n') for d in vids]  # remove \n
    with open('../hfiles/daly1.1.0.pkl','rb') as f:
        daly = pickle.load(f,  encoding='latin1')
    with open('../hfiles/videoInfo.json','r') as f:
        jdaly = json.load(f)
    metadata = daly['metadata']
    count =0
    tempvids = []

    finalannots['labels'] = daly['labels']

    labelstoclass = dict()
    for i,label in enumerate(daly['labels']):
        labelstoclass[label] = i

    finalannots['labelstoclass'] = labelstoclass
    finalannots['joints'] = daly['joints']
    finalannots['objects'] = daly['objectList']
    finalannots['version'] = daly['version']
    finalannots['testvideos'] = pre_proocess_split(daly['splits'], vids)
    finalannots['vidList'] = vids
    annot_db = dict()
    danoots = daly['annot']
    for vid in vids:
        imgdir = basedir+'rgb-images/'+vid+'/'
        if not os.path.isdir(imgdir):
             os.mkdir(imgdir)
        imglist = os.listdir(imgdir)
        imglist = [i for i in imglist if i.endswith('.jpg')]
        num_frames = len(imglist)
        nbframes_ffmpeg = metadata[vid+'.mp4']['nbframes_ffmpeg']

        metadata[vid+'.mp4']['nbframes_real'] = num_frames
        metadata[vid+'.mp4']['nbframes_ffprobe'] = jdaly[vid]['ffprobeNbFrames']
        metadata[vid+'.mp4']['duration_real'] = jdaly[vid]['duration']

        duration =  metadata[vid+'.mp4']['duration']
        jduration = jdaly[vid]['duration']
        diffs = abs(metadata[vid+'.mp4']['nbframes_ffmpeg']  - num_frames)

        vid_info = dict()
        vid_info['duration'] = duration
        vid_info['duration_real'] = jdaly[vid]['duration']
        vid_info['numf'] = num_frames
        fps = num_frames/duration
        vid_info['fps'] = fps
        vid_info['orginal_fps'] = metadata[vid+'.mp4']['fps']

        print(vid, '.mp4 nbframes_ffmpeg ', nbframes_ffmpeg,  ' duration ', metadata[vid+'.mp4']['duration'] ,
              ' fps ', metadata[vid+'.mp4']['fps'] , ' number of extracted frames ',num_frames,
              ' duration ',jduration,' fps ', jdaly[vid]['fps'])
        annotations = []
        base_annots = danoots[vid+'.mp4']
        vid_info['video_label'] = base_annots['suggestedClass']
        vid_info['class'] = labelstoclass[base_annots['suggestedClass']]
        base_annots = base_annots['annot']
        for label in base_annots.keys():
            label_annots = base_annots[label]
            for l_annot in label_annots:
                flags = l_annot['flags']
                if not (flags['isReflection'] or flags['isAmbiguous']):
                    tube = dict()
                    tube['class'] = labelstoclass[label]
                    tube['flags'] = flags
                    tube['et'] = l_annot['endTime']
                    tube['st'] = l_annot['beginTime']
                    tube['sf'] = int(tube['st'] * fps)
                    tube['ef'] = int(tube['et'] * fps)
                    bboxes = []
                    times = []
                    frames = []
                    for keyframe in l_annot['keyframes']:
                        bbox = list(keyframe['boundingBox'][0])
                        bbox = [float(b) for b in bbox]
                        bboxes.append(bbox)
                        times.append(keyframe['time'])
                        frames.append(int(keyframe['time']*fps))
                    tube['bboxes'] = bboxes
                    tube['times'] = times
                    tube['frames'] = frames
                    annotations.append(tube)
        vid_info['annotations'] = annotations
        annot_db[vid] = vid_info

    finalannots['annots'] = annot_db
    daly['metadata'] = metadata

    with open('../hfiles/finalAnnots.json','w') as f:
        json.dump(finalannots, f)
