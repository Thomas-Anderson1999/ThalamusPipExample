import json
import os
import sys


#+UI
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget
#-UI

#from ..qt_ui_lib.qt_ui_eledef import *
#from ..qtLigthTest import *

from qt_ui_eledef import *
from qtLigthTest import *

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        #+ UI Setting
        self.app_width = 1300

        self.mainGrid = QGridLayout()
        self.ui_dic_list = []

        pjttitle, captions, start_ele_lists = init_ui(self)

        for idx in range(len(start_ele_lists)):
            subgrid, start_dic = self.createGroupBox(captions[idx], start_ele_lists[idx])
            self.ui_dic_list.append(start_dic)
            self.mainGrid.addWidget(subgrid, idx, 0)


        self.setLayout(self.mainGrid)
        self.setWindowTitle(pjttitle)
        self.resize(self.app_width, -1)
        # - UI Setting

        self.LoadPreset()

    def createGroupBox(self, gbxName, UI_ele_list):
        groupBox = QGroupBox(gbxName)
        grid = QGridLayout()
        groupBox.setLayout(grid)

        tmp_dic = {}
        pos_i, pos_j = (0, 0)

        for element in UI_ele_list:
            if element.type is UIElementType.NEW_LINE:
                pos_j += 1
                pos_i = 0

            if element.type is UIElementType.EDIT:
                label = QLabel(self)
                label.setText(element.caption + ":")
                grid.addWidget(label, pos_j, pos_i)
                pos_i += 1

                edit = QLineEdit(self)
                if element.default_val is not None:
                    edit.setText(element.default_val)
                grid.addWidget(edit, pos_j, pos_i)
                pos_i += 1
                tmp_dic[element.caption] = edit

            if element.type is UIElementType.BUTTON:
                btn = QPushButton(element.caption, self)
                if element.default_val is not None:
                    btn.clicked.connect(element.default_val)
                grid.addWidget(btn, pos_j, pos_i)
                pos_i += 1

            if element.type is UIElementType.CHECK:
                cb = QCheckBox(element.caption, self)
                grid.addWidget(cb, pos_j, pos_i)
                pos_i += 1
                tmp_dic[element.caption] = cb
                if element.default_val is not None:
                    cb.setChecked(element.default_val)

            if element.type is UIElementType.COMBO:
                cb = QComboBox(self)
                grid.addWidget(cb, pos_j, pos_i)
                pos_i += 1
                for cap in element.caption:
                    cb.addItem(cap)
                tmp_dic["CB_"+element.caption[0]] = cb
                if element.default_val is not None:
                    cb.setCurrentText(element.default_val)

            if element.type is UIElementType.SLIDER:
                label = QLabel(self)
                label.setText(element.caption + ":")
                grid.addWidget(label, pos_j, pos_i)
                pos_i += 1

                slider = QSlider(Qt.Horizontal, self)
                slider.setMinimum(-100)
                slider.setMaximum(100)
                slider.setSingleStep(1)
                if element.default_val is not None:
                    slider.setValue(int(element.default_val * 100))  # float → int(퍼센트)
                grid.addWidget(slider, pos_j, pos_i)
                pos_i += 1

                tmp_dic[element.caption] = slider

        return groupBox, tmp_dic

    def getUIVal(self, key):
        res = []
        for ui_dic in self.ui_dic_list:
            ctl = ui_dic.get(key, None)
            if type(ctl) is QLineEdit:
                res.append(ctl.text())
            if type(ctl) is QCheckBox:
                res.append(ctl.isChecked())
            if type(ctl) is QComboBox:
                res.append(ctl.currentText())
            if type(ctl) is QSlider:
                res.append(ctl.value() / 100.0)
        return res

    def setUIVal(self, key, val):
        for ui_dic in self.ui_dic_list:
            ctl = ui_dic.get(key, None)
            if type(ctl) is QLineEdit:
                ctl.setText(val)
            if type(ctl) is QCheckBox:
                ctl.setChecked(val)
            if type(ctl) is QComboBox:
                ctl.setCurrentText(val)
            if type(ctl) is QSlider:
                ctl.setValue(int(val * 100))

    def SavePreset(self, path=""):
        if path is False:
            path = ""
        file_path = os.path.join(path, "preset.txt")
        with open(file_path, "w") as f:
            for diclist in self.ui_dic_list:
                tmp_dic = {}
                for k, v in diclist.items():
                    print(k, v)
                    if type(v) is QLineEdit:
                        tmp_dic[k] = v.text()
                    elif type(v) is QCheckBox:
                        tmp_dic[k] = v.isChecked()
                    elif type(v) is QComboBox:
                        tmp_dic[k] =v.currentText()
                    elif isinstance(v, QSlider):
                        tmp_dic[k] = v.value() / 100.0
                f.write(json.dumps(tmp_dic) + "\n")

    def LoadPreset(self):
        fname = "preset.txt"
        if os.path.isfile(fname):
            with open(fname, "r") as f:
                lines = f.readlines()
                for idx, line in enumerate(lines):
                    preset = json.loads(line)
                    print(preset)

                    for k, v in preset.items():
                        ctl = self.ui_dic_list[idx].get(k, None)
                        if type(ctl) is QLineEdit:
                            ctl.setText(v)
                        elif type(ctl) is QCheckBox:
                            ctl.setChecked(v)
                        elif type(ctl) is QComboBox:
                            ctl.setCurrentText(v)
                        elif isinstance(ctl, QSlider):
                            ctl.setValue(int(v * 100))  # float → int
    # -Function 1



if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = Window()
    clock.show()
    sys.exit(app.exec_())