import re, os, json, math, struct
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree.ElementTree import Element, SubElement

from matrix3 import Matrix3, reverse_trans_rot_scale_pivot_matrix
from anim_util import *

class AnimBank():
    version = 4
    frame_rate = 30
    endianstring = "<"
    file_name = "anim"

    def __init__(self, anim=None):
        self.content = None
        self.data = {}

        if isinstance(anim, bytes):
            self.content = anim
        elif isinstance(anim, dict):
            self.data = anim

    def __add__(self, other):
        if not self.data:
            self.bin_to_json()
        if not other.data:
            other.bin_to_json()

        for bank_name, bank in other.data["banks"].items():
            if bank_name in self.data["banks"]:
                for anim_name, anim in bank.items():
                    if anim_name in self.data["banks"][bank_name]:
                        print(f"animtion over: {anim_name}")
                    self.data["banks"][bank_name][anim_name] = anim
            else:
                self.data["banks"][bank_name] = bank

        self.json_to_bin()

        return self

    def bin_to_json(self):
        if not self.content:
            return

        endianstring = self.endianstring
        self.data = {}

        anim_num = struct.unpack(endianstring + "I", self.content[20: 24])[0]

        data_content = self.content[24:]
        self.data["banks"] = {}
        elements = []
        for idx in range(anim_num):
            anim_name_len = struct.unpack(endianstring + "i", data_content[: 4])[0]
            anim_name = struct.unpack(endianstring + str(anim_name_len) + "s", data_content[4: 4 + anim_name_len])[0].decode("utf-8")
            facing_byte = struct.unpack(endianstring + "B", data_content[4 + anim_name_len: 5 + anim_name_len])[0]
            anim_root_hash = struct.unpack(endianstring + "I", data_content[5 + anim_name_len: 9 + anim_name_len])[0]
            framerate = int(struct.unpack(endianstring + "f", data_content[9 + anim_name_len: 13 + anim_name_len])[0])
            numframes = struct.unpack(endianstring + "I", data_content[13 + anim_name_len: 17 + anim_name_len])[0]

            if anim_root_hash not in self.data["banks"]:
                self.data["banks"][anim_root_hash] = {}

            anim_name += faceing_dir.get(facing_byte, "")
            self.data["banks"][anim_root_hash][anim_name] = {"framerate": framerate, "numframes": numframes, "frames":[]}

            data_content = data_content[17 + anim_name_len:]
            for idx in range(numframes):
                x, y, w, h = struct.unpack(endianstring + "ffff", data_content[: 16])
                event_num = struct.unpack(endianstring + "I", data_content[16: 20])[0]
                element_num = struct.unpack(endianstring + "I", data_content[20 + event_num * 4: 24 + event_num * 4])[0]

                frame_data = {"x": x, "y": y, "w": w, "h": h, "elements": []}

                data_content = data_content[24 + event_num * 4: ]
                for z_index in range(element_num):
                    element_name_hash = struct.unpack(endianstring + "I", data_content[: 4])[0]
                    frame = struct.unpack(endianstring + "I", data_content[4: 8])[0]
                    layername_hash = struct.unpack(endianstring + "I", data_content[8: 12])[0]
                    m_a, m_b, m_c, m_d, m_tx, m_ty, z = struct.unpack(endianstring + "fffffff", data_content[12: 40])

                    element = {"name": element_name_hash, "frame": frame, "layername": layername_hash, "m_a": m_a, "m_b": m_b, "m_c": m_c, "m_d": m_d, "m_tx": m_tx, "m_ty": m_ty, "z_index": z_index}
                    frame_data["elements"].append(element)
                    elements.append(element)
                    data_content = data_content[40: ]

                sorted(frame_data["elements"], key=lambda element: element["z_index"])
                self.data["banks"][anim_root_hash][anim_name]["frames"].append(frame_data)

        hash_dict = {}
        hash_dict_len = struct.unpack(endianstring + "I", data_content[: 4])[0]
        data_content = data_content[4: ]
        for idx in range(hash_dict_len):
            hash = struct.unpack(endianstring + "I", data_content[: 4])[0]
            name_len = struct.unpack(endianstring + "i", data_content[4: 8])[0]
            name = struct.unpack(endianstring + str(name_len) + "s",  data_content[8: 8 + name_len])[0].decode("utf-8")

            if hash in self.data["banks"]:
                self.data["banks"][name] = self.data["banks"][hash]
                del self.data["banks"][hash]

            hash_dict[hash] = name
            data_content = data_content[8 + name_len: ]

        for element in elements:
            element["name"] = hash_dict[element["name"]].lower()
            element["layername"] = hash_dict[element["layername"]]

    def json_to_bin(self):
        if not self.data:
            return

        endianstring = self.endianstring
        self.content = bytes()
        hash_dict = {}

        anim_num = 0
        frame_num = 0
        element_num = 0
        for bank_name, bank in self.data["banks"].items():
            anim_num += len(bank)
            for anim_name, anim in bank.items():
                frame_num += len(anim["frames"])
                facingbyte = FACING_RIGHT | FACING_LEFT | FACING_UP | FACING_DOWN | FACING_UPLEFT | FACING_UPRIGHT | FACING_DOWNLEFT | FACING_DOWNRIGHT
                for byte, type in faceing_dir.items():
                    result = re.search("(.*)" + type + "\\Z", anim_name)
                    if result:
                        anim_name = result.group(1)
                        facingbyte = byte
                        break

                anim_name = anim_name.encode("ascii")
                self.content += struct.pack(endianstring + "i" + str(len(anim_name)) + "s", len(anim_name), anim_name)
                self.content += struct.pack(endianstring + "B", facingbyte)
                self.content += struct.pack(endianstring + "I", strhash(bank_name, hash_dict))
                self.content += struct.pack(endianstring + "fI", float(anim["framerate"]), len(anim["frames"]))

                for frame in anim["frames"]:
                    element_num += len(frame["elements"])
                    elements = sorted(frame["elements"], key=lambda element: element["z_index"])

                    self.content += struct.pack(endianstring + "ffff", float(frame["x"]), float(frame["y"]), float(frame["w"]), float(frame["h"]))
                    self.content += struct.pack(endianstring + "I", 0)  # event
                    self.content += struct.pack(endianstring + "I", len(elements))

                    for idx, element in enumerate(elements):
                        self.content += struct.pack(endianstring + "I", strhash(element["name"], hash_dict))
                        self.content += struct.pack(endianstring + "I", element["frame"])
                        self.content += struct.pack(endianstring + "I", strhash(element["layername"], hash_dict))

                        z = idx / len(frame["elements"]) * EXPORT_DEPTH - EXPORT_DEPTH * .5
                        self.content += struct.pack(endianstring + "fffffff", float(element["m_a"]), float(element["m_b"]), float(element["m_c"]), float(element["m_d"]), float(element["m_tx"]), float(element["m_ty"]), float(z))

        self.content += struct.pack(endianstring + "I", len(hash_dict))
        for hash, name in hash_dict.items():
            self.content += struct.pack(endianstring + "I", hash)
            self.content += struct.pack(endianstring + "i" + str(len(name)) + "s", len(name), name.encode("ascii"))

        head = struct.pack(endianstring +  "cccci", b"A", b"N", b"I", b"M", self.version)
        head += struct.pack(endianstring + "I", element_num)
        head += struct.pack(endianstring + "I", frame_num)
        head += struct.pack(endianstring + "I", 0)
        head += struct.pack(endianstring + "I", anim_num)
        self.content = head + self.content

    def to_scml(self, scml: Element):
        for bank_idx, (bank_name, bank) in enumerate(self.data["banks"].items()):
            entity = SubElement(scml, "entity", id=str(bank_idx), name=bank_name)
            for anim_idx, (anim_name, anim) in enumerate(bank.items()):
                frame_duration = 1000 // anim["framerate"]
                length = frame_duration * max(1, anim["numframes"] - 1)

                animation = SubElement(entity, "animation", id=str(anim_idx), name=anim_name, length=str(length))

                mainline = SubElement(animation, "mainline")

                timeline_names = []
                layer_names = []
                for frame_idx, frame in enumerate(anim["frames"]):
                    element_name_num = {}
                    element_names = []
                    for element_idx, element in enumerate(frame["elements"]):
                        element_name_num[element_name] = element_name_num[element_name] + 1 if (element_name := (element["name"] + str(element["frame"]))) in element_name_num else 0
                        element_names.append([f"{element_name}_{element_name_num[element_name]:03d}", element["layername"]])

                    index = -1
                    for idx, element_data in enumerate(element_names):
                        if element_data[0] not in timeline_names:
                            if index == -1:
                                for _element_data in element_names[idx + 1: ]:
                                    if _element_data[0] in timeline_names:
                                        index = timeline_names.index(_element_data[0])
                                        timeline_names.insert(index, element_data[0])
                                        layer_names.insert(index, element_data[1])
                                        break
                                if index == -1:
                                    timeline_names.append(element_data[0])
                                    layer_names.append(element_data[1])
                            else:
                                timeline_names.insert(index + 1, element_data[0])
                                layer_names.insert(index + 1, element_data[1])
                        else:
                            index = timeline_names.index(element_data[0])

                timelines = {}
                layer_name_num = {}
                for timeline_idx, timeline_name in enumerate(timeline_names):
                    layer_name = layer_names[timeline_idx]
                    layer_name_num[layer_name] = layer_name_num[layer_name] + 1 if layer_name in layer_name_num else 0
                    timelines[timeline_name] = SubElement(animation, "timeline", id=str(timeline_idx), name=f"{layer_name}_{layer_name_num[layer_name]:03d}")

                last_timeline = {}
                for frame_idx, frame in enumerate(anim["frames"]):
                    element_name_num = {}
                    element_names = []

                    mainline_key = SubElement(mainline, "key", id=str(frame_idx), time=str(frame_idx * frame_duration))

                    for element_idx, element in enumerate(frame["elements"]):
                        element_name_num[_element_name] = element_name_num[_element_name] + 1 if (_element_name := (element["name"] + str(element["frame"]))) in element_name_num else 0
                        element_name = f"{_element_name}_{element_name_num[_element_name]:03d}"

                        m = Matrix3()
                        m.matrix[0][0], m.matrix[1][0] = element["m_a"], element["m_b"]
                        m.matrix[0][1], m.matrix[1][1] = element["m_c"], element["m_d"]
                        m.matrix[0][2], m.matrix[1][2] = element["m_tx"], element["m_ty"]

                        trans = m.get_translation()

                        first = False
                        if element_name not in last_timeline:
                            last_timeline[element_name] = {"scale_x": 1, "scale_y": 1, "angle": 0, "spin": 1}
                            first = True
                        last = last_timeline[element_name] = reverse_trans_rot_scale_pivot_matrix(m, last_timeline[element_name], first)
                        angle = math.degrees(last["angle"] if last["angle"] >= 0 else last["angle"] + 2 * math.pi)

                        key = SubElement(timelines[element_name], "key", id=str(frame_idx), time=str(frame_idx * frame_duration), spin=str(last["spin"]))
                        SubElement(key, "object", folder=scml.find(f"folder[@name='{element['name']}']").get("id"), file=str(element["frame"]), x=str(trans[0]), y=str(-trans[1]), scale_x=str(last["scale_x"]), scale_y=str(last["scale_y"]), angle=str(angle))
                        SubElement(mainline_key, "object_ref", id=str(element_idx), timeline=timelines[element_name].get("id"), key=str(frame_idx), z_index=str(len(frame["elements"]) - 1 - element_idx))

    def save_bin(self, output: str|ZipFile, name=None):
        if not self.content:
            self.json_to_bin()

        if isinstance(output, str):
            with open(os.path.join(output, f"{self.file_name}.bin"), "wb") as file:
                file.write(self.content)
        elif isinstance(output, ZipFile):
            output.writestr(name if name is not None else f"{self.file_name}.bin", self.content, compress_type=ZIP_DEFLATED)

        return output

    def save_json(self, output: str, indent="    "):
        if not self.data:
            self.bin_to_json()

        with open(os.path.join(output, f"{self.file_name}.json"), "w") as file:
            file.write("{\n" + indent + f'"type": "Anim", "version": {self.version},\n')
            file.write(indent + '"banks": {\n')

            bank_str = []
            for bank_name, bank in self.data["banks"].items():
                animation_str = []
                for anim_name, animation in bank.items():
                    frame_str = []
                    for frame in animation["frames"]:
                        frame_str.append(
                            5 * indent + "{\n"
                            + 6 * indent + f'"x": {frame["x"]}, "y": {frame["y"]}, "w": {frame["w"]}, "h": {frame["h"]},\n'
                            + 6 * indent + '"elements": [\n' + ",\n".join([7 * indent + json.dumps(element) for element in frame["elements"]]) + "\n" + 6 * indent + "]\n"
                            + 5 * indent + "}"
                        )

                    animation_str.append(
                        3 * indent + f'"{anim_name}": ' + "{\n"
                        + 4 * indent + f'"framerate": {animation["framerate"]}, "numframes": {animation["numframes"]},\n'
                        + 4 * indent + '"frames": [\n'
                        + ",\n".join(frame_str) + "\n"
                        + 4 * indent + "]\n"
                        + 3 * indent + "}"
                    )

                bank_str.append(
                    2 * indent + f'"{bank_name}": ' + "{\n"
                    + ",\n".join(animation_str) + "\n"
                    + 2 * indent + "}"
                )

            file.write(",\n".join(bank_str) + "\n")
            file.write(indent + "}\n")
            file.write("}")

        return output

    def convert(self, output: str|ZipFile):
        if not self.data:
            return self.save_json(output)
        else:
            return self.save_bin(output)
