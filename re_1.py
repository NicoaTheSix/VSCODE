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
        for attr in sctn_attr_rgx.findall(asm):
            sctn = Section()
            sctn.name, sctn.virtual_size, sctn.raw_size, access = attr[0].lower(), int(attr[1]), int(attr[2]), set(attr[3].split())
            if "Executable" in access:
                sctn.executable = True
            if "Writable" in access:
                sctn.writable = True
            sctns.append(sctn)
        return sctns
sctn_attr_rgx = re.compile(r"([A-Za-z]+):[\dA-F]{8}\s+;\s+Virtual\s+size\s+:\s+[\dA-F]{8}\s+\(\s*(\d+)\.[\s\S]+?Section\s+size\s+in\s+file\s+:\s+[\dA-F]{8}\s+\(\s*(\d+)\.[\s\S]+?;\s+Flags\s+[\dA-F]{8}:[\s\S]+?\s+((?:Executable|Readable|Writable|\s)+)", flags=re.IGNORECASE)
sctn_attr_rgx.findall(Read.asm())
print(type(sctn_attr_rgx.findall(Read.asm())))
print(list(sctn_attr_rgx.findall(Read.asm())))
for i in range(3):
    print(Section.load()[i])
    print(type(Section.load()[i]))
    print("name:",Section.load()[i].name)
    print("virtual_size:",Section.load()[i].virtual_size)
    print("raw_size",Section.load()[i].raw_size)
    print("executable",Section.load()[i].executable)
    print("writable",Section.load()[i].writable)

    rwe_cols = [f"{i}-{j}" for i in ["Executable", "Writable", "Readable"] for j in ["Virtual", "Raw", "Ratio"]]
    rwe = pd.DataFrame(columns=["ID"] + rwe_cols, dtype=float).set_index("ID")
    sctn = pd.DataFrame(columns=["ID"], dtype=float).set_index("ID")