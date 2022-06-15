from win32com.client import Dispatch
from enum import IntEnum
import win32com.client as win32
import structnra_com
import simnra_com
import time


class Color(IntEnum):
    DarkGreen = 1
    Navy = 2
    Blue = 3
    Pink = 4
    White = 5
    Purple = 6
    LightGreen = 7
    Cyan = 8


class StructNRA:
    app: structnra_com.IApp
    simnra: simnra_com.IApp
    struct: structnra_com.IStructure

    def __init__(self):
        self.app = Dispatch(structnra_com.App.CLSID)
        self.struct = Dispatch(structnra_com.Structure.CLSID)
        self.simnra = Dispatch(simnra_com.App.CLSID)
        # Nasty workaround for slow dispatch call
        time.sleep(1)


def example_1():
    snra = StructNRA()
    snra.app.Show()
    snra.app.Import("C:/dev/tmp/test.bmp")
    snra.app.Open("C:/dev/tmp/Michiel/test.snra")
    # snra.struct.SetMaterialDensity(int(Color.Navy), 5.02)
    start = time.time()
    snra.app.CalculateUniform()
    end = time.time()
    print("calculation took {} seconds".format(end-start))

    snra.app.SaveAs("C:/dev/tmp/output.snra")
    snra.simnra.Open("C:/dev/tmp/output.snra")
    snra.simnra.WriteSpectrumData("C:/dev/tmp/output_ascii.dat")


if __name__ == "__main__":
    example_1()
