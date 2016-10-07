__subzoom__ = "subzoom"
__version__ = "0.1.0"

import sys
import re

def main():
    print( 'subzoom ver {0}, a simple adjuster for subtitle\'s timeline.'.format(__version__) )
    do()

def printUsage():
    print( 'Usage: {0} --from hh:mm:ss.xxx-hh:mm:ss.xxx --to hh:mm:ss.xxx-hh:mm:ss.xxx subtitle.ass'
        .format(__subzoom__) )

def formatTime( time ):
    h = time // 360000
    time = time % 360000
    m = time // 6000
    time = time % 6000
    s = time // 100
    f= time % 100
    return '{:1d}:{:02d}:{:02d}.{:02d}'.format(h,m,s,f)

def do():
    if len(sys.argv)!=6 or sys.argv[1]!='--from' or sys.argv[3]!='--to':
        printUsage()
        return None
    patTime = '(\\d{1,2}):([0-5][0-9]):([0-5][0-9])\.(\\d{2})'
    reTime = re.compile(patTime+'-'+patTime)
    match = reTime.match(sys.argv[2])
    if match:
        fromBegin = ((int(match.groups()[0])*60+int(match.groups()[1]))*60+int(match.groups()[2]))*100+ \
            int(match.groups()[3]+'0'*(2-len(match.groups()[3])))
        fromEnd = ((int(match.groups()[4])*60+int(match.groups()[5]))*60+int(match.groups()[6]))*100+ \
            int(match.groups()[7]+'0'*(2-len(match.groups()[7])))
    else:
        printUsage()
        return None
    match = reTime.match(sys.argv[4])
    if match:
        toBegin = ((int(match.groups()[0])*60+int(match.groups()[1]))*60+int(match.groups()[2]))*100+ \
            int(match.groups()[3]+'0'*(2-len(match.groups()[3])))
        toEnd = ((int(match.groups()[4])*60+int(match.groups()[5]))*60+int(match.groups()[6]))*100+ \
            int(match.groups()[7]+'0'*(2-len(match.groups()[7])))
    else:
        printUsage()
        return None
    zoom = (toEnd-toBegin)/(fromEnd-fromBegin)
    offset = toBegin-(fromBegin*zoom)
    count = 0
    with open(sys.argv[5], encoding='utf-8', mode='r') as src, open(sys.argv[5]+'.new.ass', encoding='utf-8', mode='w') as dest:
        for line in src:
            reSub = re.compile('(.*)\\b'+patTime+'\\b(.+)\\b'+patTime+'\\b(.*)')
            match = reSub.match(line)
            if match:
                fromSub = ((int(match.groups()[1])*60+int(match.groups()[2]))*60+int(match.groups()[3]))*100+ \
                    int(match.groups()[4]+'0'*(2-len(match.groups()[4])))
                toSub = ((int(match.groups()[6])*60+int(match.groups()[7]))*60+int(match.groups()[8]))*100+ \
                    int(match.groups()[9]+'0'*(2-len(match.groups()[9])))
                fromSub = int((fromSub+offset)*zoom)
                toSub = int((toSub+offset)*zoom)
                dest.write(match.groups()[0]+formatTime(fromSub)+match.groups()[5]+formatTime(toSub)+match.groups()[10]+'\r\n')
                count+=1
            else:
                dest.write(line+'\r\n')
    print('Adjusted {} lines.'.format(count))
    

