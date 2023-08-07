import os, json, struct
from zipfile import ZipFile

from anim_util import *
from anim_bank import AnimBank
from anim_build import AnimBuild
from scml import Scml

class DSAnim():
    endianstring = "<"

    def __init__(self, fp: str|dict|bytes|AnimBank|AnimBuild=None, images: str|dict=None, endianstring: str="<"):
        self.bank: AnimBank = None
        self.build: AnimBuild = None

        self.endianstring = endianstring
        if fp:
            self.parse_file(fp, images)

    def __add__(self, other):
        if other.build is not None:
            if self.build is None:
                self.build = other.build
            else:
                self.build += other.build
        if other.bank is not None:
            if self.bank is None:
                self.bank = other.bank
            else:
                self.bank += other.bank

        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def _parse_zip_file(self, fp: str):
        with ZipFile(fp) as zip_file:
            if "anim.bin" in (namelist := zip_file.namelist()):
                self.bank = AnimBank(zip_file.read("anim.bin"))
            if "build.bin" in namelist:
                self.build = AnimBuild(zip_file.read("build.bin"), atlas=zip_file)

    def _parse_bin_file(self, fp: str|bytes):
        if isinstance(fp, bytes):
            content = fp
        elif isinstance(fp, str):
            with open(fp, "rb") as buffer:
                content = buffer.read()

        head = struct.unpack(self.endianstring + "cccci", content[:8])
        if head == (b"A", b"N", b"I", b"M", AnimBank.version):
            self.bank = AnimBank(content)
        elif head == (b"B", b"I", b"L", b"D", AnimBuild.version):
            self.build = AnimBuild(content, atlas=os.path.split(fp)[0])

    def _parse_json_file(self, fp: str|dict, images: str|dict=None):
        if isinstance(fp, dict):
            data = fp
        elif isinstance(fp, str):
            with open(fp, "r") as file:
                data = json.load(file)

        if data["type"] == "Anim":
            self.bank = AnimBank(data)
        elif data["type"] == "Build":
            self.build = AnimBuild(data, images=images)

    def parse_file(self, fp: str|dict|bytes|AnimBank|AnimBuild, images: str|dict=None):
        if isinstance(fp, AnimBank):
            self.bank = fp
        elif isinstance(fp, AnimBuild):
            self.build = fp
        elif isinstance(fp, bytes) or ((isstring := isinstance(fp, str)) and (file_type := os.path.splitext(fp)[1]) == ".bin"):
            self._parse_bin_file(fp)
        elif isinstance(fp, dict) or (isstring and file_type == ".json"):
            self._parse_json_file(fp, images)
        elif isstring:
            if file_type == ".zip":
                self._parse_zip_file(fp)
            elif file_type == "":  # input a path
                root, symbol_dirs, files = next(os.walk(fp), (None, None, []))
                if "build.json" in files:
                    self._parse_json_file(os.path.join(fp, "build.json"), fp if images is None else images)
                if "anim.json" in files:
                    self._parse_json_file(os.path.join(fp, "anim.json"))

    def bin_to_json(self):
        if self.build is not None:
            self.build.bin_to_json()
        if self.bank is not None:
            self.bank.bin_to_json()

    def save_json(self, output: str):
        if self.build is not None:
            output = self.build.save_json(output)
        if self.bank is not None:
            self.bank.save_json(output)

    def save_bin(self, output: str|ZipFile, name=None):
        if self.build is not None:
            output = self.build.save_bin(output, name)
        if self.bank is not None:
            self.bank.save_bin(output, name)

    def to_scml(self, output: str, mapping: bool=False, name: str=None):
        if self.bank is None:
            print("missing bank")
            return
        if self.build is None:
            print("missing build")
            return

        if not self.bank.data:
            self.bank.bin_to_json()
        if not self.build.data:
            self.build.bin_to_json()

        if name is not None:
            self.build.set_build_name(name)

        scml = Scml()
        scml_root = scml.getroot()
        dir=os.path.dirname(output)
        self.build.to_scml(scml_root, self.bank, dir, mapping)
        self.bank.to_scml(scml_root)
        if not output:
            output=os.path.join(output, self.build.data["name"] + ".scml")
        scml.writr(output)

    def convert(self, output: str|ZipFile):
        if self.build is not None:
            output = self.build.convert(output)
        if self.bank is not None:
            self.bank.convert(output)

        if isinstance(output, ZipFile):
            output.close()

    def close(self):
        if self.build is not None:
            self.build.close()