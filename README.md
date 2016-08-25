
This repo provided utility tools to browse the videos and annotation files for <a href="http://thoth.inrialpes.fr/daly/index.php">DALY</a> dataset.

Main purpose to produce frame level annotation rather than time.

It requires you to download and place videos under ./videos directory and images will be extracted in ./images folder. There is an option in script to chnage the data directory.

Only dependency is ffmpeg.
 
All the helping files are places in hfiles folder. Which contains annotation file daly1.0.pkl, video_ids.txt, labels.txt and videoInfo.json.

Now let's go script by script.

First script is checkifdownloaded.py: As name suggest it check if all the files are downloaded; 
if some of the videos are missing then it will write the IDs of those video in ./hfiles/left.txt file.

Extraction.py script takes videos and extract frame and place them in ./images directory. You can control the quality of images/frame by chaneging -qscale:v 5 in ffmpeg command in extractframes function.
quality varies from 1-31; 1 being the best quality and 31 being the worst. PNG format is very storage heavy so I choose JPG. At -qscale:v 5 images will take alomst 145GB.
There is another function in Extraction.py, saveVidInfo uses ffprobe to get duration, framerate and number of frames information. It will save all the info into ./hfiles/vidinfo.json.

Basically, it relate time to frame numbers, as the annotation are provided in time, not in frame numbers/indexes. So using these tools you use framebased approcahes to train your methods.

If founf any then please report it me at guru094@gmail.com
