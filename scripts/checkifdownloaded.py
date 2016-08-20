''''
Author: Gurkirt Singh
Date: 20:08:2016

Main purpose of this script to help produce framelevel annotations for DALY dataset

As name suggest it check if all the files are downloaded; if some of the videos are
missing then it will write the IDs of those video in ../hfiles/left.txt file.
'''
import os as os

def checkendswih(vid,dnwmldd):
    for d in dnwmldd:
        if d.endswith(vid):
            return True
    else:
        return False
    
downloaded = os.listdir('../videos') # get list of file
downloaded = [d for d in downloaded if d.endswith('.mp4')]  # keep only .mp4 files

print 'number of videos downloded are ', len(downloaded) 

with open('../hfiles/video_ids.txt') as f: 
    vids = f.readlines(); # read video ids 

count= 0;
fid = open('../hfiles/left.txt','w');
for vid in vids:
    vid1 = vid.rstrip('\n')+'.mp4'
    if not vid1 in downloaded : # check if videos are present in downloaded directory
        if not checkendswih(vid1,downloaded): ## check for special case where video id starts with "-"
            count +=1
            print vid1,
            fid.write(vid) # write video id if not downloaded

fid.close()
print '\nNumber of videos left are', count