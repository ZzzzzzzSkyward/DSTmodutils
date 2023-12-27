import math
import re
import os
from copy import deepcopy
from .anim_bank import AnimBank
from .anim_build import AnimBuild
from .matrix3 import create_trans_rot_scale_pivot_matrix
from xml.etree.ElementTree import Element, ElementTree, indent


def rotate_point(x1, y1, x2, y2, theta):
    """
        Rotates a point (x1, y1) around another point (x2, y2) by an angle angle.
    """
    dx = x1 - x2
    dy = y1 - y2

    x_rotated = dx * math.cos(theta) - dy * math.sin(theta) + x2
    y_rotated = dx * math.sin(theta) + dy * math.cos(theta) + y2

    return x_rotated, y_rotated


def scale_point(x1, y1, x2, y2, scale_x, scale_y):
    """
    Scales a point (x, y) around another point (a, b) by a scale.
    """
    x_scaled = x2 + (x1 - x2) * scale_x
    y_scaled = y2 + (y1 - y2) * scale_y

    return x_scaled, y_scaled


def flatten(bone_frame: dict, bone_frames: list[dict]):
    if bone_frame["is_flattened"] or bone_frame["parent_id"] == -1:
        return

    for parent in bone_frames:
        if parent["id"] == bone_frame["parent_id"]:
            flatten(parent, bone_frames)

            bone_frame["scale_x"] *= parent["scale_x"]
            bone_frame["scale_y"] *= parent["scale_y"]

            sx = bone_frame["x"] * parent["scale_x"]
            sy = bone_frame["y"] * parent["scale_y"]
            s = math.sin(parent["angle"])
            c = math.cos(parent["angle"])

            bone_frame["x"] = parent["x"] + sx * c - sy * s
            bone_frame["y"] = parent["y"] + sx * s + sy * c
            bone_frame["angle"] += parent["angle"]

            break

    bone_frame["is_flattened"] = True

def TO_STR(element):
    """
    处理单个 XML 元素
    
    参数：
    element: 要处理的 XML 元素
    """
    # 处理整数类型
    for i,v in element.attrib.items():
        if type(i) is not str:
            print('not str attribute',i,v)
            # 将整数转换为字符串类型
            element.set(str(i),str(v))
            del element.attrib[i]
            continue
        if type(v) is not str:
            print('not str value',i,v)
            element.set(i,str(v))

    # 递归处理子元素
    for child in element:
        TO_STR(child)

class Scml(ElementTree):
    def __init__(self, file=None):
        if file is None:
            ElementTree.__init__(
                self,
                Element(
                    "spriter_data",
                    scml_version="1.0",
                    generator="BrashMonkey Spriter",
                    generator_version="b5"))
        else:
            self.path = file
            ElementTree.__init__(self, file=file)

    def writr(self, output):
        indent(self, space="  ")
        TO_STR(self.getroot())
        if type(output) is str:
            output=open(output,'wb')
        ElementTree.write(self, output, encoding="utf-8")
        output.close()

    def build_image(self, scale: float = 1) -> tuple[dict, dict]:
        build_path = os.path.split(self.path)[0]
        build_name = os.path.splitext(os.path.basename(self.path))[0]

        build_data = {
            "type": "Build",
            "version": AnimBuild.version,
            "name": build_name,
            "scale": scale,
            "Symbol": {}}
        symbols_images = {}

        folders = self.findall("folder")
        for folder in folders:
            folder_name = folder.get("name", "???").lower()

            files = [
                file for file in folder.findall("file") if file.get(
                    "name", "???").find("(missing)") == -1]
            if files:
                build_data["Symbol"][folder_name] = []

            jump_frame = []
            for file in files:
                if (framenum := int(file.get("id", "0"))) in jump_frame:
                    continue

                duration = int(file.get("duration", 1))
                for i in range(1, duration):
                    jump_frame.append(framenum + i)

                if (match := re.search(r"(duration\'(.+?)\')",
                                       file.get("name", "???"))) is not None:
                    duration = int(re.findall(r'\d+', match.group(1))[0])
                    for frame in build_data["Symbol"][folder_name]:
                        if frame["framenum"] == duration:
                            frame["duration"] += 1
                            break
                    continue

                w, h = int(file.get("width", 0)), int(file.get("height", 0))

                x = w // 2 - float(file.get("pivot_x", "0")) * w
                y = h // 2 - float(file.get("pivot_y", "0")) * h
                y = -y

                build_data["Symbol"][folder_name].append(
                    {"framenum": framenum, "duration": duration, "x": x, "y": y, "w": w, "h": h})
                symbols_images[f"{folder_name}-{framenum}"] = os.path.join(
                    build_path, file.get("name", "???"))

        return build_data, symbols_images

    def build_scml(self, output, scale: float = 1):
        scml_root = deepcopy(self.getroot())

        anim_data = {"type": "Anim", "version": 4, "banks": {}}
        build_data, symbols_images = self.build_image(scale)

        frame_duration = 1000 // AnimBank.frame_rate

        for entity in scml_root.findall("entity"):
            entity_name = entity.get("name", "???")
            anim_data["banks"][entity_name] = {}

            for animation in entity.findall("animation"):
                mainline = animation.find("mainline")
                animation_name = animation.get("name", "???")
                anim_data["banks"][entity_name][animation_name] = {
                    "framerate": AnimBank.frame_rate, "frames": []}

                mainline_keys = mainline.findall("key")
                last_time = 0
                for mainline_key in mainline_keys:
                    time = int(mainline_key.get("time", 0))
                    if (time - last_time) % frame_duration != 0:
                        print(
                            f"{animation_name} error, The frame duration must be {frame_duration}",
                            (time - last_time))
                    last_time = time

                    Frame = {"elements": []}

                    frame_verts = []
                    frame_positions = []

                    object_refs = mainline_key.findall("object_ref")
                    object_ref_cont = len(object_refs)
                    for object_ref in object_refs:
                        timeline = animation.find(
                            f"timeline[@id='{object_ref.get('timeline')}']")
                        timeline_key = timeline.find(
                            f"key[@id='{object_ref.get('key')}']")
                        timeline_key_object = timeline_key.find("object")
                        file = scml_root.find(
                            f"folder[@id='{timeline_key_object.get('folder')}']/file[@id='{timeline_key_object.get('file')}']")

                        pivot_x, pivot_y = float(
                            file.get(
                                "pivot_x", 0)), float(
                            file.get(
                                "pivot_y", 0))
                        w, h = float(
                            file.get(
                                "width", 0)), float(
                            file.get(
                                "height", 0))

                        element_name = scml_root.find(
                            f"folder[@id='{timeline_key_object.get('folder', '0')}']").get("name", "???")
                        layer_name = re.sub(
                            r"_\d+$", "", timeline.get("name", ""))
                        frame_num = int(timeline_key_object.get("file", "0"))

                        pivot_x, pivot_y = float(
                            timeline_key_object.get(
                                "pivot_x", pivot_x)), float(
                            timeline_key_object.get(
                                "pivot_y", pivot_y))
                        position_x, position_y = float(
                            timeline_key_object.get(
                                "x", 0)), float(
                            timeline_key_object.get(
                                "y", 0))
                        scale_x, scale_y = float(
                            timeline_key_object.get(
                                "scale_x", 1)), float(
                            timeline_key_object.get(
                                "scale_y", 1))
                        angle = math.radians(
                            float(timeline_key_object.get("angle", 0)))
                        z_index = object_ref_cont - \
                            int(object_ref.get("z_index", 0)) - 1

                        frame_positions.append((position_x, position_y))

                        verts = []
                        verts.append((position_x - pivot_x * w,
                                     position_y - (1 - pivot_y) * h))
                        verts.append((position_x + (1 - pivot_x) * w,
                                     position_y - (1 - pivot_y) * h))
                        verts.append(
                            (position_x - pivot_x * w, position_y + pivot_y * h))
                        verts.append((position_x + (1 - pivot_x)
                                     * w, position_y + pivot_y * h))

                        for vert in verts:
                            vert = rotate_point(
                                vert[0], vert[1], position_x, position_y, angle)
                            vert = scale_point(
                                vert[0], vert[1], position_x, position_y, scale_x, scale_y)
                            frame_verts.append(vert)

                        matrix = create_trans_rot_scale_pivot_matrix(
                            (position_x, -position_y), angle, (scale_x, scale_y), (0, 0))
                        m = matrix.matrix

                        Frame["elements"].append(
                            {
                                "name": element_name,
                                "frame": frame_num,
                                "layername": layer_name,
                                "m_a": m[0][0],
                                "m_b": m[1][0],
                                "m_c": m[0][1],
                                "m_d": m[1][1],
                                "m_tx": m[0][2],
                                "m_ty": m[1][2],
                                "z_index": z_index})

                    x_vert = [vert[0] for vert in frame_verts]
                    y_vert = [vert[1] for vert in frame_verts]
                    left, right, up, down = min(x_vert) if x_vert else 0, max(
                        x_vert) if x_vert else 0, min(y_vert) if y_vert else 0, max(y_vert) if y_vert else 0
                    frame_pivot_x = sum([position[0] for position in frame_positions]) / len(
                        frame_positions) if frame_positions else 0
                    frame_pivot_y = sum([position[1] for position in frame_positions]) / len(
                        frame_positions) if frame_positions else 0
                    frame_w, frame_h = right - left, down - up
                    frame_x = frame_w / 2 - (frame_pivot_x - left)
                    frame_y = frame_h / 2 - (frame_pivot_y - up)
                    Frame["x"], Frame["y"], Frame["w"], Frame["h"] = frame_x, -frame_y, frame_w, frame_h

                    anim_data["banks"][entity_name][animation_name]["frames"].append(
                        Frame)
                    anim_data["banks"][entity_name][animation_name]["numframes"] = len(
                        Frame)
        from .anim import DSAnim
        with DSAnim(anim_data) as anim:
            anim.parse_file(build_data, symbols_images)
            anim.save_bin(output)

    @staticmethod
    def fetch_image(name, framenum, builddata):
        framenum = int(framenum)
        dirdata = builddata['Symbol'].get(name)
        if not dirdata:
            return
        image_index = -1
        for i, img in enumerate(dirdata):
            num = int(img.get("framenum", 1))
            dur = int(img.get("duration", 1))
            start, stop = num, num + dur
            if framenum >= start and framenum < stop:
                image_index = i
                break
        if image_index == -1:
            return
        return dirdata[image_index]

    @staticmethod
    def apply_matrix_transform(verts, a, b, c, d, tx, ty, x, y):
        for i in range(len(verts)):
            v = verts[i]
            transformed_x = a * (v[0] - x) + c * (v[1] - y)
            transformed_y = b * (v[0] - x) + d * (v[1] - y)
            verts[i] = (transformed_x + tx, transformed_y + ty)

    @staticmethod
    def rebuild_anim(animdata: dict, builddata: dict):
        #input: anim.json and build.json
        for bank in animdata["banks"].values():
            for animation in bank.values():
                for frame in animation['frames']:
                    frame_verts = []
                    sum_tx = 0
                    sum_ty = 0
                    length = 0
                    for layer in frame['elements']:
                        a, b, c, d, tx, ty = layer['m_a'], layer['m_b'], layer[
                            'm_c'], layer['m_d'], layer['m_tx'], layer['m_ty']
                        sum_tx += tx
                        sum_ty += ty
                        img = Scml.fetch_image(
                            layer['name'], layer['frame'], builddata)
                        if not img:
                            continue
                        x, y, w, h = img['x'], img['y'], img['w'], img['h']
                        verts = [(-w / 2, -h / 2), (w / 2, h / 2),
                                 (w / 2, -h / 2), (-w / 2, h / 2)]
                        Scml.apply_matrix_transform(
                            verts, a, b, c, d, tx, ty, x, y)
                        frame_verts.extend(verts)
                        length += 1
                    if length > 0:
                        x_vert, y_vert = zip(*frame_verts)
                        left, right, up, down = min(x_vert), max(
                            x_vert), min(y_vert), max(y_vert)
                        frame_pivot_x = sum_tx / length
                        frame_pivot_y = sum_ty / length
                        frame_w, frame_h = right - left, down - up
                        frame_x = frame_pivot_x - left - frame_w / 2
                        frame_y = frame_pivot_y - up - frame_h / 2
                        frame.update({"x": frame_x, "y": frame_y,
                                     "w": frame_w, "h": frame_h})
