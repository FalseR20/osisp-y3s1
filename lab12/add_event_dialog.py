from PyQt6 import QtCore, QtGui, QtWidgets


class AddEventDialog(QtWidgets.QDialog):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.setup()

    def accept(self) -> None:
        self.handler(self.formLayout)
        super().accept()

    def setup(self):
        self.setObjectName("AddEventDialog")
        self.resize(700, 400)
        self.formLayoutWidget = QtWidgets.QWidget(self)
        self.formLayoutWidget.setGeometry(QtCore.QRect(100, 100, 600, 300))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.RowWrapPolicy.WrapAllRows)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setVerticalSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.name = QtWidgets.QLabel(self.formLayoutWidget)
        self.name.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.name.setFont(font)
        self.name.setObjectName("name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.name)
        self.LineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.LineEdit.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.LineEdit.setFont(font)
        self.LineEdit.setAccessibleName("")
        self.LineEdit.setObjectName("LineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.LineEdit)
        self.begin = QtWidgets.QLabel(self.formLayoutWidget)
        self.begin.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.begin.setFont(font)
        self.begin.setObjectName("begin")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.begin)
        self.DateTimeEdit = QtWidgets.QDateTimeEdit(self.formLayoutWidget)
        self.DateTimeEdit.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.DateTimeEdit.setFont(font)
        self.DateTimeEdit.setObjectName("DateTimeEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.DateTimeEdit)
        self.end = QtWidgets.QLabel(self.formLayoutWidget)
        self.end.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.end.setFont(font)
        self.end.setObjectName("end")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.end)
        self.DateTimeEdit_2 = QtWidgets.QDateTimeEdit(self.formLayoutWidget)
        self.DateTimeEdit_2.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.DateTimeEdit_2.setFont(font)
        self.DateTimeEdit_2.setObjectName("DateTimeEdit_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.DateTimeEdit_2)

        self.retranslate()

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(0, 330, 600, 50))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel | QtWidgets.QDialogButtonBox.StandardButton.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.accept)  # type: ignore
        self.buttonBox.rejected.connect(self.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.name.setText(_translate("Dialog", "Название события"))
        self.begin.setText(_translate("Dialog", "Начало"))
        self.end.setText(_translate("Dialog", "Конец"))
