from logging import getLogger

from data_module import CalendarEvent
from PyQt6 import QtCore, QtGui, QtWidgets


class CalendarEventDialog(QtWidgets.QDialog):
    def __init__(self, current_date: QtCore.QDate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = getLogger(self.__class__.__module__)
        self.setWindowTitle("CalendarEventDialog")
        self.resize(700, 330)

        self.formLayoutWidget = QtWidgets.QWidget(self)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 20, 660, 300))

        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.RowWrapPolicy.WrapAllRows)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setVerticalSpacing(10)

        labels_font = QtGui.QFont("Segoe UI", 12)
        fields_font = QtGui.QFont("Segoe UI", 15)

        now_time = QtCore.QTime.currentTime()
        default_date_time = QtCore.QDateTime(current_date, QtCore.QTime(now_time.hour(), now_time.minute()))

        # Description
        self.description_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.description_label.setMinimumSize(QtCore.QSize(0, 30))
        self.description_label.setFont(labels_font)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.description_label)

        self.description_field = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.description_field.setMinimumSize(QtCore.QSize(0, 30))
        self.description_field.setFont(fields_font)
        self.description_field.setAccessibleName("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.description_field)

        # Begin time
        self.begin_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.begin_label.setMinimumSize(QtCore.QSize(0, 30))
        self.begin_label.setFont(labels_font)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.begin_label)

        self.begin_field = QtWidgets.QDateTimeEdit(self.formLayoutWidget)
        self.begin_field.setDateTime(default_date_time)
        self.begin_field.setMinimumSize(QtCore.QSize(0, 30))
        self.begin_field.setFont(fields_font)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.begin_field)

        # End time
        self.end_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.end_label.setMinimumSize(QtCore.QSize(0, 30))
        self.end_label.setFont(labels_font)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.end_label)

        self.end_field = QtWidgets.QDateTimeEdit(self.formLayoutWidget)
        self.end_field.setDateTime(default_date_time)
        self.end_field.setMinimumSize(QtCore.QSize(0, 30))
        self.end_field.setFont(fields_font)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.end_field)
        self.end_field.dateTimeChanged.connect(self._end_validation_event)  # type: ignore
        self.begin_field.dateTimeChanged.connect(self.end_field.setDateTime)  # type: ignore

        # Retranslate
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.description_label.setText(_translate("Dialog", "Название события"))
        self.begin_label.setText(_translate("Dialog", "Начало"))
        self.end_label.setText(_translate("Dialog", "Конец"))

        self.buttonBox = QtWidgets.QDialogButtonBox(self.formLayoutWidget)
        # self.buttonBox.setGeometry(QtCore.QRect(0, 330, 600, 50))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel | QtWidgets.QDialogButtonBox.StandardButton.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.accept)  # type: ignore
        self.buttonBox.rejected.connect(self.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(self)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.buttonBox)

    def _end_validation_event(self, end_date_time: QtCore.QDateTime):
        apply_button = self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        apply_button.setDisabled(end_date_time < self.begin_field.dateTime())

    def exec_new(self) -> tuple[CalendarEvent, bool]:
        status = self.exec()
        calendar_event = CalendarEvent(
            self.description_field.text(),
            self.begin_field.dateTime(),
            self.end_field.dateTime(),
        )
        return calendar_event, bool(status)

    def exec_change(self, event_unit: CalendarEvent) -> bool:
        self.description_field.setText(event_unit.description)
        self.begin_field.setDateTime(event_unit.begin)
        self.end_field.setDateTime(event_unit.end)
        status = self.exec()
        if is_ok := bool(status):
            event_unit.description = self.description_field.text()
            event_unit.begin = self.begin_field.dateTime()
            event_unit.end = self.end_field.dateTime()
        return is_ok
