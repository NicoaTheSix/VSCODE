import re
import pandas as pd
class Read():
    def asm():
        with open('0AnoOZDNbPXIr2MRBSCJ.asm',encoding="utf-8", errors="ignore") as file:
            return file.read()
class Section:
    """
    Save a section's attributions.
    """
    def __init__(self) -> None:
        self.name: str = ""
        self.virtual_size: int = 0
        self.raw_size: int = 0
        self.executable: bool = False
        self.writable: bool = False

    @staticmethod
    def load():
        """
        Extract a sample's section attributions.
        """
        asm = Read.asm()
        sctns = []
        for attr in call_rgx.findall(asm):
            sctn = Section()
            sctn.name, sctn.virtual_size, sctn.raw_size, access = attr[0].lower(), int(attr[1]), int(attr[2]), set(attr[3].split())
            if "Executable" in access:
                sctn.executable = True
            if "Writable" in access:
                sctn.writable = True
            sctns.append(sctn)
        return sctns
call_rgx = re.compile(r"\scall\s+(?:ds:)(?:__imp_)?([^\s]+)", flags=re.IGNORECASE)
call_rgx.findall(Read.asm())

print(type(call_rgx.findall(Read.asm())))
print(list(call_rgx.findall(Read.asm())))