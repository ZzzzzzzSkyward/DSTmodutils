import os, re, math, struct, json, copy
from PIL import Image
from zipfile import ZipFile, ZIP_DEFLATED
from tempfile import TemporaryDirectory
from xml.etree.ElementTree import Element, SubElement

from .anim_util import *
from .anim_bank import AnimBank
from .symbol_map import GetSwapSymbol
from . import atlas_image, optimize_image
from .ktech import tex_to_png, png_to_tex

class AnimBuild():
    version = 6
    endianstring = "<"
    file_name = "build"

    def __init__(self, build: bytes|dict=None, atlas: str|ZipFile=None, images: str|dict=None) -> None:
        self.temp_dir = TemporaryDirectory()
        self.temp_path = self.temp_dir.name
        self.content = None
        self.data = {}
        self.symbol_images: dict[str: Image] = {}
        self.atlases: list[Image.Image] = []

        if isinstance(build, bytes):
            self.content = build
        elif isinstance(build, dict):
            self.data = build

        if atlas is not None:
            self._parse_atlas(atlas)
        if images is not None:
            self._parse_images(images)

    def __add__(self, other):
        if not self.data:
            self.bin_to_json()
        if not other.data:
            other.bin_to_json()

        self.data["scale"] = min(self.data["scale"], other.data["scale"])
        for symbol_name, symbol in other.data["Symbol"].items():
            if symbol_name in self.data["Symbol"]:
                frame_data = {_frame["framenum"]: idx for idx, _frame in enumerate(self.data["Symbol"][symbol_name])}
                for frame in symbol:
                    if (framenum := frame["framenum"]) in frame_data:
                        print(f"symbol over: {symbol_name}-{framenum}")
                        self.data["Symbol"][symbol_name][frame_data[framenum]] = frame
                    else:
                        self.data["Symbol"][symbol_name].append(frame)
                self.data["Symbol"][symbol_name] = sorted(self.data["Symbol"][symbol_name], key=lambda frame: frame["framenum"])
            else:
                self.data["Symbol"][symbol_name] = symbol

        if other.symbol_images:
            if not self.symbol_images:
                self.symbol_images = {}
            for frame_name in other.symbol_images:
                if frame_name in self.symbol_images:
                    self.symbol_images[frame_name].close()
                self.symbol_images[frame_name] = other.symbol_images[frame_name]

        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def _parse_images(self, fp: str|dict):
        self.symbol_images = {}
        if isinstance(fp, str):
            root, symbol_dirs, files = next(os.walk(fp), (None, None, []))
            for symbol_dir in symbol_dirs:
                symbol_root, dirs, image_files = next(os.walk(os.path.join(root, symbol_dir)), (None, None, []))
                for image in image_files:
                    if image.find(".png") != -1 and image.find("(missing)") == -1 and re.search(r"(duration\'(.+?)\')", image) is None:
                        self.symbol_images[f"{os.path.splitext(image)[0]}".lower()] = Image.open(os.path.join(symbol_root, image)).convert("RGBA")
        elif isinstance(fp, dict):
            self.symbol_images = {name.lower(): Image.open(path) for name, path in fp.items() if path.find(".png") != -1 and path.find("(missing)") == -1 and re.search(r"(duration\'(.+?)\')", path) is None}

    def _parse_atlas(self, fp: str|ZipFile):
        if isinstance(fp, ZipFile):
            for file_name in fp.namelist():
                if file_name.find(".tex") != -1:
                    fp.extract(file_name, path=self.temp_path)
            fp = self.temp_path

        for atlas in self.atlases:
            atlas.close()
        self.atlases = []
        root, dirs, files = next(os.walk(fp), (None, None, []))
        for file_name in sorted([file_name for file_name in files if file_name.find(".tex") != -1], key=lambda s: int(s.split('-')[1].split('.')[0])):
            image_path = os.path.join(self.temp_path, file_name.replace(".tex", ".png"))
            tex_to_png(os.path.join(root, file_name), image_path)
            self.atlases.append(Image.open(image_path).convert("RGBA"))

    def set_build_name(self, name: str):
        self.data["name"] = name

    def atlas_images(self, name="atlas"):
        if not self.data:
            self.bin_to_json()

        images = []
        for symbol_name, frames in self.data["Symbol"].items():
            for frame in frames:
                frame_name = f'{symbol_name}-{frame["framenum"]}'
                self.symbol_images[frame_name] = optimize_image.OptimizeImage(self.symbol_images[frame_name], 32)
                setattr(self.symbol_images[frame_name], "name", frame_name)
                images.append(self.symbol_images[frame_name])

        scale_factor = self.data.get("scale",1)
        atlases = atlas_image.Atlas(images, name, scale_factor=scale_factor)

        self.data["Vert"] = []
        symbol_names = sorted(self.data["Symbol"], key=lambda name: strhash(name, {}))
        for symbol_name in symbol_names:
            for frame in self.data["Symbol"][symbol_name]:
                frame_name = f'{symbol_name}-{frame["framenum"]}'

                x_offset = frame["x"] - frame["w"] / 2
                y_offset = frame["y"] - frame["h"] / 2

                frame["alphaidx"] = len(self.data["Vert"])
                frame["alphacount"] = 0

                for idx, atlas in enumerate(atlases):
                    bboxes = atlas.bboxes

                    atlas_width = float(atlas.mips.im.size[0])
                    atlas_height = float(atlas.mips.im.size[1])

                    if frame_name not in atlas.src_images:
                        continue
                    image = atlas.src_images[frame_name]

                    for src_regions in [image.regions.alpha, image.regions.opaque]:
                        dest_bbox = bboxes[frame_name]

                        regions_x_offset =  image.x_offset if hasattr(image, "x_offset") else 0
                        regions_y_offset = image.y_offset if hasattr(image, "y_offset") else 0
                        for region in src_regions:
                            assert region.x <= image.really_size[0]
                            assert region.y <= image.really_size[1]
                            assert region.x + region.w <= image.really_size[0]
                            assert region.y + region.h <= image.really_size[1]

                            left = x_offset + region.x
                            right = left + region.w
                            top = y_offset + region.y
                            bottom = top + region.h

                            umin = max( 0.0, min( 1.0, (dest_bbox.x + region.x - regions_x_offset) / atlas_width ) )
                            umax = max( 0.0, min( 1.0, (dest_bbox.x + region.x - regions_x_offset + region.w) / atlas_width ) )
                            vmin = max( 0.0, min( 1.0, 1 - (dest_bbox.y + region.y - regions_y_offset) / atlas_height ) )
                            vmax = max( 0.0, min( 1.0, 1 - (dest_bbox.y + region.y - regions_y_offset + region.h) / atlas_height ) )

                            assert 0 <= umin and umin <= 1
                            assert 0 <= umax and umax <= 1
                            assert 0 <= vmin and vmin <= 1
                            assert 0 <= vmax and vmax <= 1

                            self.data["Vert"].append({"x": left, "y": top, "z": 0, "u": umin, "v": vmin, "w": idx})
                            self.data["Vert"].append({"x": right, "y": top, "z": 0, "u": umax, "v": vmin, "w": idx})
                            self.data["Vert"].append({"x": left, "y": bottom, "z": 0, "u": umin, "v": vmax, "w": idx})
                            self.data["Vert"].append({"x": right, "y": top, "z": 0, "u": umax, "v": vmin, "w": idx})
                            self.data["Vert"].append({"x": right, "y": bottom, "z": 0, "u": umax, "v": vmax, "w": idx})
                            self.data["Vert"].append({"x": left, "y": bottom, "z": 0, "u": umin, "v": vmax, "w": idx})

                            frame["alphacount"] += 6

        for atlas in self.atlases:
            atlas.close()
        self.atlases = []
        self.data["Atlas"] = []
        for atlas_data in atlases:
            width = (mip_img := atlas_data.mips[1]).size[0] * scale_factor
            height = mip_img.size[1] * scale_factor
            mip_img = mip_img.resize((int(math.ceil(width)), int(math.ceil(height))), Image.LANCZOS)
            self.atlases.append(mip_img)

            self.data["Atlas"].append(atlas_data.mips.name + ".tex")
    def noatlas_images(self, name="atlas"):
        if not self.data:
            self.bin_to_json()

        images = []
        for symbol_name, frames in self.data["Symbol"].items():
            for frame in frames:
                frame_name = f'{symbol_name}-{frame["framenum"]}'
                self.symbol_images[frame_name] = Image(self.symbol_images[frame_name])
                setattr(self.symbol_images[frame_name], "name", frame_name)
                images.append(self.symbol_images[frame_name])

        scale_factor = self.data.get("scale",1)
        atlases = atlas_image.Atlas(images, name, scale_factor=scale_factor)

        self.data["Vert"] = []
        symbol_names = sorted(self.data["Symbol"], key=lambda name: strhash(name, {}))
        for symbol_name in symbol_names:
            for frame in self.data["Symbol"][symbol_name]:
                frame_name = f'{symbol_name}-{frame["framenum"]}'

                x_offset = frame["x"] - frame["w"] / 2
                y_offset = frame["y"] - frame["h"] / 2

                frame["alphaidx"] = len(self.data["Vert"])
                frame["alphacount"] = 0

                for idx, atlas in enumerate(atlases):
                    bboxes = atlas.bboxes

                    atlas_width = float(atlas.mips.im.size[0])
                    atlas_height = float(atlas.mips.im.size[1])

                    if frame_name not in atlas.src_images:
                        continue
                    image = atlas.src_images[frame_name]

                    for src_regions in [image.regions.alpha, image.regions.opaque]:
                        dest_bbox = bboxes[frame_name]

                        regions_x_offset =  image.x_offset if hasattr(image, "x_offset") else 0
                        regions_y_offset = image.y_offset if hasattr(image, "y_offset") else 0
                        for region in src_regions:
                            assert region.x <= image.really_size[0]
                            assert region.y <= image.really_size[1]
                            assert region.x + region.w <= image.really_size[0]
                            assert region.y + region.h <= image.really_size[1]

                            left = x_offset + region.x
                            right = left + region.w
                            top = y_offset + region.y
                            bottom = top + region.h

                            umin = max( 0.0, min( 1.0, (dest_bbox.x + region.x - regions_x_offset) / atlas_width ) )
                            umax = max( 0.0, min( 1.0, (dest_bbox.x + region.x - regions_x_offset + region.w) / atlas_width ) )
                            vmin = max( 0.0, min( 1.0, 1 - (dest_bbox.y + region.y - regions_y_offset) / atlas_height ) )
                            vmax = max( 0.0, min( 1.0, 1 - (dest_bbox.y + region.y - regions_y_offset + region.h) / atlas_height ) )

                            assert 0 <= umin and umin <= 1
                            assert 0 <= umax and umax <= 1
                            assert 0 <= vmin and vmin <= 1
                            assert 0 <= vmax and vmax <= 1

                            self.data["Vert"].append({"x": left, "y": top, "z": 0, "u": umin, "v": vmin, "w": idx})
                            self.data["Vert"].append({"x": right, "y": top, "z": 0, "u": umax, "v": vmin, "w": idx})
                            self.data["Vert"].append({"x": left, "y": bottom, "z": 0, "u": umin, "v": vmax, "w": idx})
                            self.data["Vert"].append({"x": right, "y": top, "z": 0, "u": umax, "v": vmin, "w": idx})
                            self.data["Vert"].append({"x": right, "y": bottom, "z": 0, "u": umax, "v": vmax, "w": idx})
                            self.data["Vert"].append({"x": left, "y": bottom, "z": 0, "u": umin, "v": vmax, "w": idx})

                            frame["alphacount"] += 6

        for atlas in self.atlases:
            atlas.close()
        self.atlases = []
        self.data["Atlas"] = []
        for atlas_data in atlases:
            width = (mip_img := atlas_data.mips[1]).size[0] * scale_factor
            height = mip_img.size[1] * scale_factor
            mip_img = mip_img.resize((int(math.ceil(width)), int(math.ceil(height))), Image.LANCZOS)
            self.atlases.append(mip_img)

            self.data["Atlas"].append(atlas_data.mips.name + ".tex")

    def split_altas(self):
        scale, scale_num = 0, 0

        for symbol_name in self.data["Symbol"]:
            for frame in self.data["Symbol"][symbol_name]:
                image_name = f"{symbol_name}-{frame['framenum']}"

                verts = self.data["Vert"][frame["alphaidx"]: frame["alphaidx"] + frame["alphacount"]]
                x_offset, y_offset = frame["x"] - (w := frame["w"]) / 2, frame["y"] - (h := frame["h"]) / 2

                if len(verts) == 0 or max(u_list := [vert["u"] for vert in verts] or [0]) == min(u_list):
                    self.symbol_images[image_name] = Image.new("RGBA", (w, h))
                    continue

                region_verts = [verts[i: i + 6] for i in range(0, len(verts), 6)]

                region_left = min(verts[0]["x"] for verts in region_verts)
                region_right = max(verts[1]["x"] for verts in region_verts)
                region_top = min(verts[0]["y"] for verts in region_verts)
                region_bottom = max(verts[2]["y"] for verts in region_verts)

                region_x = round_up(region_left - x_offset)
                region_y = round_up(region_top - y_offset)
                region_w = round_up(region_right - region_left)
                region_h = round_up(region_bottom - region_top)

                atlas = self.atlases[int(verts[0]["w"])]
                cropped = atlas.crop((
                    min(u_list) * atlas.width,
                    (1 - max(v_list := [vert["v"] for vert in verts] or [0])) * atlas.height,
                    max(u_list) * atlas.width,
                    (1 - min(v_list)) * atlas.height
                ))
                if cropped.width != region_w or cropped.height != region_h:
                    scale_num += 2
                    scale += cropped.width / region_w + cropped.height / region_h
                    cropped = cropped.resize((region_w, region_h))
                if cropped.width != w or cropped.height != h:
                    if cropped.width + region_x > w or cropped.height + region_y > h:
                        print(f"Waring, can't resize {image_name} to recorded size")
                    else:
                        new_image = Image.new("RGBA", (w, h))
                        new_image.paste(cropped, (region_x, region_y))
                        cropped = new_image

                self.symbol_images[image_name] = cropped

            self.data["scale"] = scale / scale_num if scale_num > 0 else 1

    def bin_to_json(self):
        if not self.content:
            return

        endianstring = self.endianstring

        symbol_num = struct.unpack(endianstring + "I", self.content[8: 12])[0]
        build_name_len = struct.unpack(endianstring + "I", self.content[16: 20])[0]
        self.data["name"] = struct.unpack(endianstring + str(build_name_len) + "s", self.content[20: 20 + build_name_len])[0].decode("utf-8")

        atlas_num = struct.unpack(endianstring + "I", self.content[20 + build_name_len: 24 + build_name_len])[0]
        data_content = self.content[24 + build_name_len: ]

        self.data["Atlas"] = []
        for atlas_idx in range(atlas_num):
            atlas_name_len = struct.unpack(endianstring + "I", data_content[: 4])[0]
            atlas_name = struct.unpack(endianstring + str(atlas_name_len) + "s", data_content[4: 4 + atlas_name_len])[0].decode("utf-8")
            data_content = data_content[4 + atlas_name_len: ]
            self.data["Atlas"].append(atlas_name)

        self.data["Symbol"] = {}
        for symbol_idx in range(symbol_num):
            symbol_name_hash = struct.unpack(endianstring + "I", data_content[: 4])[0]
            frames_len = struct.unpack(endianstring + "I", data_content[4: 8])[0]
            self.data["Symbol"][symbol_name_hash] = []
            data_content = data_content[8:]

            for frame_idx in range(frames_len):
                framenum = struct.unpack(endianstring + "I", data_content[0: 4])[0]
                duration = struct.unpack(endianstring + "I", data_content[4: 8])[0]
                x, y, w, h = struct.unpack(endianstring + "ffff", data_content[8: 24])
                alphaidx = struct.unpack(endianstring + "I", data_content[24: 28])[0]
                alphacount = struct.unpack(endianstring + "I", data_content[28: 32])[0]
                self.data["Symbol"][symbol_name_hash].append({"framenum": framenum, "duration": duration, "x": x, "y": y, "w": int(w), "h": int(h), "alphaidx": alphaidx, "alphacount": alphacount})
                data_content = data_content[32:]
            sorted(self.data["Symbol"][symbol_name_hash], key=lambda frame: frame["framenum"])

        verts_len = struct.unpack(endianstring + "I", data_content[: 4])[0]
        data_content = data_content[4: ]
        self.data["Vert"] = []
        for vert_idx in range(verts_len):
            x, y, z, u, v, w = struct.unpack(endianstring + "ffffff", data_content[: 24])
            self.data["Vert"].append({"x": x, "y": y, "z": z, "u": u, "v": v, "w": w})
            data_content = data_content[24: ]

        hash_dict_len = struct.unpack(endianstring + "I", data_content[: 4])[0]
        data_content = data_content[4: ]

        for hash_idx in range(hash_dict_len):
            hash = struct.unpack(endianstring + "I", data_content[: 4])[0]
            hash_str_len = struct.unpack(endianstring + "i", data_content[4: 8])[0]
            hash_str = struct.unpack(endianstring + str(hash_str_len) + "s", data_content[8: 8 + hash_str_len])[0].decode("utf-8")

            if hash in self.data["Symbol"]:
                self.data["Symbol"][hash_str.lower()] = self.data["Symbol"][hash]
                del self.data["Symbol"][hash]

            data_content = data_content[8 + hash_str_len: ]

        if self.atlases:
            self.split_altas()

    def json_to_bin(self):
        if not self.data:
            return

        endianstring = self.endianstring
        hash_dict = {}

        self.content = bytes()
        self.content += struct.pack(endianstring + "cccci", b"B", b"I", b"L", b"D", self.version)
        self.content += struct.pack(endianstring + "I", len(symbols := self.data["Symbol"]))
        self.content += struct.pack(endianstring + "I", sum([len(frames) for frames in self.data["Symbol"].values()]))
        self.content += struct.pack(endianstring + "i" + str(len(buildname := self.data["name"].encode("ascii"))) + "s", len(buildname), buildname)
        self.content += struct.pack(endianstring + "I", len(atlases := self.data["Atlas"]))
        for atlas_name in atlases:
            self.content += struct.pack(endianstring + "i" + str(len(atlas_name)) + "s", len(atlas_name), atlas_name.encode("ascii"))

        symbol_hash_dict = sorted([strhash(symbol_name, hash_dict) for symbol_name in symbols])
        for hash in symbol_hash_dict:
            self.content += struct.pack(endianstring + "I", hash)
            self.content += struct.pack(endianstring + "I", len(frames := symbols[hash_dict[hash]]))

            for frame in frames:
                self.content += struct.pack(endianstring + "I", frame["framenum"])
                self.content += struct.pack(endianstring + "I", frame["duration"])
                self.content += struct.pack(endianstring + "ffff", frame["x"], frame["y"], frame["w"], frame["h"])
                self.content += struct.pack(endianstring + "I", frame["alphaidx"])
                self.content += struct.pack(endianstring + "I", frame["alphacount"])

        self.content += struct.pack(endianstring + "I", len(self.data["Vert"]))
        for vert in self.data["Vert"]:
            self.content += struct.pack(endianstring + "ffffff", float(vert["x"]), float(vert["y"]), float(vert["z"]), float(vert["u"]), float(vert["v"]), float(vert["w"]))

        self.content += struct.pack(endianstring + "I", len(hash_dict))
        for hash, name in hash_dict.items():
            self.content += struct.pack(endianstring + "I", hash)
            self.content += struct.pack(endianstring + "i" + str(len(name)) + "s", len(name), name.encode("ascii"))

    def to_scml(self, scml: Element, banks: AnimBank, output: str, mapping: bool=False):
        folders = {}

        for symbol_name, symbol in self.data["Symbol"].items():
            map_name = GetSwapSymbol(symbol_name) if mapping else symbol_name
            folders[map_name] = {frame["framenum"]: copy.deepcopy(frame) for frame in symbol}
            if map_name != symbol_name:
                for framenum in folders[map_name]:
                    if (name := f"{symbol_name}-{framenum}") in self.symbol_images:
                        self.symbol_images[f"{map_name}-{framenum}"] = self.symbol_images[name].copy()

        for bank in banks.data["banks"].values():
            for anim in bank.values():
                for frame in anim["frames"]:
                    for element in frame["elements"]:
                        if (element_name := element["name"]) not in folders:
                            folders[element_name] = {}

                        if element["frame"] not in folders[element_name]:
                            folders[element_name][element["frame"]] = {"framenum": element["frame"], "duration": 1, "x": 0, "y": 0, "w": int(frame["w"]), "h": int(frame["h"])}

        for folder_idx, (folder_name, symbol) in enumerate(folders.items()):
            folder = SubElement(scml, "folder", id=str(folder_idx), name=folder_name)

            folder_path = os.path.join(output, folder_name)
            try_makedirs(folder_path)

            max_framenum = max([framenum for framenum in symbol]) if len(symbol) else -1
            continue_ids = []
            for framenum in range(max_framenum + 1):
                if framenum in continue_ids:
                    continue

                complement_frame = list(symbol.values())[0]
                if framenum not in symbol:
                    symbol[framenum] = {"framenum": framenum, "duration": 1, "x": 0, "y": 0, "w": complement_frame["w"], "h": complement_frame["h"]}

                frame = symbol[framenum]
                file_name = frame_name = f"{folder_name}-{framenum}"
                x, y = frame["x"], frame["y"]
                width, height = frame["w"], frame["h"]
                pivot_x, pivot_y = 0.5 - x / width, 0.5 + y / height

                if frame_name in self.symbol_images:
                    self.symbol_images[frame_name].save(os.path.join(folder_path, f"{frame_name}.png"))
                else:
                    #file_name = f"{file_name}(missing)"
                    with Image.new("RGBA", (width, height)) as image:
                        image.save(os.path.join(folder_path, f"{file_name}.png"))

                SubElement(folder, "file", id=str(framenum), name=f"{folder_name}/{file_name}.png", width=str(width), height=str(height), pivot_x=str(pivot_x), pivot_y=str(pivot_y))

                for duration in range(1, symbol[framenum]["duration"]):
                    framenum_duration = framenum + duration
                    continue_ids.append(framenum_duration)
                    file_name = f"{folder_name}-{framenum_duration}(duration'{framenum}')"
                    self.symbol_images[frame_name].save(os.path.join(folder_path, f"{file_name}.png"))
                    SubElement(folder, "file", id=str(framenum_duration), name=f"{folder_name}/{file_name}.png", width=str(width), height=str(height), pivot_x=str(pivot_x), pivot_y=str(pivot_y))

    def convert(self, output: str|ZipFile):
        if not self.data:
            return self.save_json(output)
        else:
            return self.save_bin(output)

    def save_bin(self, output: str|ZipFile, name=None):
        if self.symbol_images:
            self.atlas_images()

        if not self.content:
            self.json_to_bin()

        if self.atlases and isinstance(output, str):
            name = name if name is not None else self.data["name"]
            output = ZipFile(os.path.join(output, name + ".zip"), "w")
            self.save_atlas(output)

        if isinstance(output, str):
            with open(os.path.join(output, f"{self.file_name}.bin"), "wb") as file:
                file.write(self.content)
        elif isinstance(output, ZipFile):
            output.writestr("build.bin", self.content, compress_type=ZIP_DEFLATED)

        return output
    def save_bin_noatlas(self, output: str|ZipFile, name=None):
        if self.symbol_images:
            self.noatlas_images()

        if not self.content:
            self.json_to_bin()

        if self.atlases and isinstance(output, str):
            name = name if name is not None else self.data["name"]
            output = ZipFile(os.path.join(output, name + ".zip"), "w")
            self.save_atlas(output)

        if isinstance(output, str):
            with open(os.path.join(output, f"{self.file_name}.bin"), "wb") as file:
                file.write(self.content)
        elif isinstance(output, ZipFile):
            output.writestr("build.bin", self.content, compress_type=ZIP_DEFLATED)

        return output

    def save_atlas(self, output: str|ZipFile):
        for atlas_idx, atlas in enumerate(self.data["Atlas"]):
            atlas_tex = os.path.join(self.temp_path, atlas)
            atlas_path = atlas_tex.replace(".tex", ".png")
            self.atlases[atlas_idx].save(atlas_path)
            if isinstance(output, ZipFile):
                png_to_tex(atlas_path, atlas_tex)
                output.writestr(f"atlas-{atlas_idx}.tex", open(atlas_tex, "rb").read(), compress_type=ZIP_DEFLATED)
            else:
                png_to_tex(atlas_path, os.path.join(output, atlas))

    def save_json(self, output: str, indent: str="    "):
        if not self.data:
            self.bin_to_json()

        if self.symbol_images:
            output = os.path.join(output, self.data["name"])
            try_makedirs(output)
            self.save_symbol_images(output)

        with open(os.path.join(output, f"{self.file_name}.json"), "w") as file:
            if "scale" not in self.data:
                self.data["scale"] = 1
            file.write("{\n" + indent + f'"type": "Build", "version": {self.version}, "name": "{self.data["name"]}", "scale": {self.data["scale"]},\n')
            file.write(indent + '"Atlas": [' + ", ".join([f"\"{atlas}\"" for atlas in self.data["Atlas"]]) + "],\n")
            file.write(indent + '"Symbol": {\n')
            symbol_str = []
            for symbol_name, frames in self.data["Symbol"].items():
                symbol_str.append(
                    indent * 2 + f'"{symbol_name}": [\n'
                    + ",\n".join([indent * 3 + json.dumps(frame) for frame in frames])
                    + f"\n{indent * 2}]"
                )
            file.write(",\n".join(symbol_str)+ f"\n{indent}" + "},\n")
            file.write(indent + '"Vert": [\n')
            file.write(",\n".join([indent * 2 + "{" + ", ".join([f'"{k}": {v}' for k, v in vert.items()]) + "}" for vert in self.data["Vert"]]) + "\n")
            file.write(indent + "]\n}")

        return output

    def save_symbol_images(self, output_path, auto_completion=False):
        for symbol_name, frames in self.data["Symbol"].items():
            symbol_path = os.path.join(output_path, symbol_name)
            try_makedirs(symbol_path)
            for frame in frames:
                frame_name = f"{symbol_name}-{frame['framenum']}"
                self.symbol_images[frame_name].save(os.path.join(symbol_path, f"{symbol_name}-{frame['framenum']}.png"))
                if auto_completion:
                    for duration in range(1, frame["duration"]):
                        self.symbol_images[frame_name].save(os.path.join(symbol_path, f"{symbol_name}-{frame['framenum'] + duration}'(duration{frame['framenum']}').png"))

    def close(self):
        for atlas in self.atlases:
            atlas.close()
        for frame_name, image in self.symbol_images.items():
            image.close()

        self.temp_dir.cleanup()
