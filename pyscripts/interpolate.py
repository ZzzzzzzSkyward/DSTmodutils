import json
import sys
import matplotlib.bezier as bz


def interpolate_bezier(c1, c2, c3, c4, t):
    fn = bz.BezierSegment([[0, 0], [c1, c2], [c3, c4], [1, 1]])
    return fn.point_at_t(t)[1]


def interpolate_linear(v1, v2, t):
    isangle = False
    # print(v1,v2,t,isangle)
    # Handle angles near 0 and 360 degrees
    if v1 > 350 and v2 < 10:
        isangle = True
        v2 = v2 + 360
    elif v2 > 350 and v1 < 10:
        isangle = True
        v1 = v1 + 360
    # Calculate linear interpolation
    if isangle:
        return v1 + (v2 - v1) * t % 360
    else:
        return v1 + (v2 - v1) * t


def processscon(filepath):
    data = None
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if data:
        processroot(data)
    return data


def processroot(r, framerate=30):
    for i in r['entity']:
        for j in i['animation']:
            processanim(j, framerate)
            j['interval'] = int(1000 / framerate)
           # j['length']=


def processanim(a, framerate=30):
    timelines = a['timeline']
    a['timeline'] = []
    for id, i in enumerate(timelines):
        intp = interpolate(i['key'], framerate)
        newtl = {
            'id': id,
            'key': intp
        }
        a['timeline'].append(newtl)
    mainline = a['mainline']
    processmainline(mainline)
    return a


def processmainline(m):
    key = m['key']
    # m['key']=[]
    for i in key:
        pass


def interpolate(data, framerate=30):
    frames = []
    framerate = 1000 / framerate
    frame_rate = 1 / framerate
    if 'time' not in data[0]:
        data[0]['time'] = 0
    for frame in range(0, int(data[-1]['time'] * frame_rate + 1)):

        # Find keyframes between which this frame falls
        keyframe1 = None
        keyframe2 = None
        for keyframe in data:
            if frame >= frame_rate * keyframe['time']:
                keyframe1 = keyframe
            else:
                if not keyframe2:
                    keyframe2 = keyframe
                    break

        if not keyframe1 or not keyframe2:
            print("Invalid keyframe: frame=", frame, "t=", frame * framerate)
            raise ValueError("Invalid keyframe")
            continue
        t = (frame - frame_rate * keyframe1['time']) / \
            (keyframe2['time'] - keyframe1['time']) * framerate
        print(
            f'frame {frame:02d}:time {frame*framerate:.0f}<-{keyframe1["time"]}-{keyframe2["time"]}')
        assert (frame == 0 and t == 0) or (frame != 0 and t != 0)
        object = {}

        if keyframe1.get('curve_type') == 'bezier':
            c1 = keyframe1.get('c1')
            c2 = keyframe1.get('c2')
            c3 = keyframe1.get('c3')
            c4 = keyframe1.get('c4')

            object['x'] = interpolate_linear(keyframe1['object']['x'],
                                             keyframe2['object']['x'],
                                             interpolate_bezier(c1, c2, c3, c4, t))

            object['y'] = interpolate_linear(keyframe1['object']['y'],
                                             keyframe2['object']['y'],
                                             interpolate_bezier(c1, c2, c3, c4, t))
            if frame == 16:
                print(keyframe1['object']['y'],
                      keyframe2['object']['y'], c1, c2, c3, c4, t,
                      interpolate_bezier(c1, c2, c3, c4, t))
            object['angle'] = interpolate_linear(keyframe1['object']['angle'],
                                                 keyframe2['object']['angle'],
                                                 interpolate_bezier(c1, c2, c3, c4, t))

            object['scale_x'] = interpolate_linear(keyframe1['object']['scale_x'],
                                                   keyframe2['object']['scale_x'],
                                                   interpolate_bezier(c1, c2, c3, c4, t))

            object['scale_y'] = interpolate_linear(keyframe1['object']['scale_y'],
                                                   keyframe2['object']['scale_y'],
                                                   interpolate_bezier(c1, c2, c3, c4, t))
        else:
            object['x'] = interpolate_linear(keyframe1['object']['x'],
                                             keyframe2['object']['x'],
                                             t)
            object['y'] = interpolate_linear(keyframe1['object']['y'],
                                             keyframe2['object']['y'],
                                             t)
            object['angle'] = interpolate_linear(keyframe1['object']['angle'],
                                                 keyframe2['object']['angle'],
                                                 t)
            object['scale_x'] = interpolate_linear(keyframe1['object']['scale_x'],
                                                   keyframe2['object']['scale_x'],
                                                   t)
            object['scale_y'] = interpolate_linear(keyframe1['object']['scale_y'],
                                                   keyframe2['object']['scale_y'],
                                                   t)
        # Copy other properties from previous keyframe
        object['file'] = keyframe1['object']['file']
        object['folder'] = keyframe1['object']['folder']

        dat = {
            'time': int(frame * framerate),
            'object': object,
        }
        try:
            dat['spin'] = keyframe1['spin']
        except BaseException:
            pass
        frames.append(dat)

    # Reassign ids and times
    for i, frame in enumerate(frames):
        frame['id'] = i

    return frames


def savedata(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def main():
    if len(sys.argv) < 2:
        print("Usage: python interpolate.py input.scon [output_interp.scon]")
        sys.exit(0)
    args = sys.argv[1:]
    inputfile = args[0]
    outputfile = args[1] if len(args) > 1 else inputfile.replace(".", "_interp")
    data = processscon(inputfile)
    savedata(outputfile, data)


if '__main__' == __name__:
    main()
