#+ui
from qt_ui_eledef import *
from functools import partial
from PyQt5.QtWidgets import QMessageBox
#-ui

import cv2

from ThalamusEngine.Interface import *

def init_ui(self):
    start_ele_list1 = [
        UIElement(_type=UIElementType.BUTTON, _caption="SavePreset", _default_val=self.SavePreset),
        UIElement(_type=UIElementType.BUTTON, _caption="LoadPreset", _default_val=self.LoadPreset),
        UIElement(_type=UIElementType.NEW_LINE),
        UIElement(_type=UIElementType.EDIT, _caption="Script", _default_val="Script.txt"),
        UIElement(_type=UIElementType.BUTTON, _caption="EngineStart", _default_val=partial(EngineStart, self)),
        UIElement(_type=UIElementType.BUTTON, _caption="Redraw", _default_val=partial(Redraw, self)),
    ]

    start_ele_list2 = [
        #UIElement(_type=UIElementType.CHECK, _caption="Check1", _default_val=True),
        #UIElement(_type=UIElementType.CHECK, _caption="Check2", _default_val=False),
        # UIElement(_type=UIElementType.COMBO, _caption=["ITEM1", "ITEM2", "ITEM3", ], _default_val="ITEM1"),

        UIElement(_type=UIElementType.EDIT, _caption="ObjID", _default_val="0"),
        UIElement(_type=UIElementType.NEW_LINE),
        UIElement(_type=UIElementType.EDIT, _caption="Light1_Ambient", _default_val="0.0"),
        UIElement(_type=UIElementType.SLIDER, _caption="Ambient1", _default_val=0.0),
        UIElement(_type=UIElementType.EDIT, _caption="Light1_Diffuse", _default_val="0.0"),
        UIElement(_type=UIElementType.SLIDER, _caption="Diffus1", _default_val=0.0),
        UIElement(_type=UIElementType.EDIT, _caption="Light1_Specular", _default_val="0.0"),
        UIElement(_type=UIElementType.SLIDER, _caption="Specular1", _default_val=0.0),
        UIElement(_type=UIElementType.NEW_LINE),
        UIElement(_type=UIElementType.EDIT, _caption="Interval_PosX1", _default_val="300"),
        UIElement(_type=UIElementType.EDIT, _caption="Interval_PosY1", _default_val="300"),
        UIElement(_type=UIElementType.EDIT, _caption="Interval_PosZ1", _default_val="300"),
        UIElement(_type=UIElementType.EDIT, _caption="Base_PosX1", _default_val="300"),
        UIElement(_type=UIElementType.EDIT, _caption="Base_PosY1", _default_val="300"),
        UIElement(_type=UIElementType.EDIT, _caption="Base_PosZ1", _default_val="300"),
        UIElement(_type=UIElementType.NEW_LINE),
        UIElement(_type=UIElementType.EDIT, _caption="Light1_PosX", _default_val="0.0"),
        UIElement(_type=UIElementType.SLIDER, _caption="PosX1", _default_val=0.0),
        UIElement(_type=UIElementType.EDIT, _caption="Light1_PosY", _default_val="0.0"),
        UIElement(_type=UIElementType.SLIDER, _caption="PosY1", _default_val=0.0),
        UIElement(_type=UIElementType.EDIT, _caption="Light1_PosZ", _default_val="0.0"),
        UIElement(_type=UIElementType.SLIDER, _caption="PosZ1", _default_val=0.0),
        UIElement(_type=UIElementType.NEW_LINE),
    ]

    self.isLoadEngine = False
    return "Light Test", ["Engine Setting","Light1 Setting"], [start_ele_list1, start_ele_list2]


def _enginestart(AsmFileName):
    SimWindowText = "Modeling Debug"
    SimWindowText = SimWindowText.encode('UTF-8')
    if True == LoadThalamusInterface():
        errCode = InitEngine(AsmFileName, 1280, 720, 0)
        if errCode != 0:
            errMsg = ""
            if errCode & 1 != 0:
                errMsg += "env.txt "
            if errCode & 2 != 0:
                errMsg += "script"
            return False

        StartExt3DEngine(AsmFileName, SimWindowText)
    else:
        return False
    return True

def EngineStart(self):
    if self.isLoadEngine is True:
        return

    AsmFileName = self.getUIVal("Script")[0].encode('UTF-8')
    if _enginestart(AsmFileName):
        self.isLoadEngine = True

def Redraw(self):
    if self.isLoadEngine is False:
        AsmFileName = self.getUIVal("Script")[0].encode('UTF-8')
        if _enginestart(AsmFileName):
            self.isLoadEngine = True

    #print(self.getUIVal("Edit1")[0], self.getUIVal("Check1")[0], self.getUIVal("Check2")[0], self.getUIVal("Weight")[0], self.getUIVal("CB_ITEM1")[0])
    SrcPosX, SrcPosY, SrcWidth, SrcHeight, DestWidth, DestHeight, ObjID, CPUCore = (0,0,1280,720,640,480,-1,12)
    Color_width = DestWidth
    Color_Height = DestHeight

    Color_image = np.zeros((Color_Height, Color_width, 3), np.uint8)
    Depth_Map = np.zeros((Color_Height, Color_width), np.float32)
    Depth_Mask = np.zeros((Color_Height, Color_width, 3), np.uint8)

    t0 = time.monotonic()
    InitializeRenderFacet(-1, -1)  # refresh
    t1 = time.monotonic()
    GetRasterizedImage(Color_image.ctypes, Depth_Map.ctypes, Depth_Mask.ctypes,
                       Color_width, Color_Height, CPUCore, SrcPosX, SrcPosY, SrcWidth, SrcHeight, ObjID)
    t2 = time.monotonic()
    print("render Time elapsed: ", t1-t0, t2-t1, t2-t0)

    cv2.imshow("Rasterizing Color Image", Color_image)

    ObjIDMask, FaceIDMask, EdgeMask = cv2.split(Depth_Mask)
    Depth_Map = cv2.normalize(Depth_Map, None, alpha=0, beta=1.0, norm_type=cv2.NORM_MINMAX)
    cv2.imshow("Depth Map", Depth_Map)
    cv2.imshow("Depth Mask", EdgeMask)
