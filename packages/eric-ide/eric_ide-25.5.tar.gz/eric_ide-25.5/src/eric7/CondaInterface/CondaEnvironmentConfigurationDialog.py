# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2025 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the parameters for the conda virtual environment.
"""

import os

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QDialog, QDialogButtonBox

from eric7.EricWidgets.EricApplication import ericApp
from eric7.EricWidgets.EricPathPicker import EricPathPickerModes

from . import condaVersion, condaVersionStr, isCondaAvailable
from .Ui_CondaEnvironmentConfigurationDialog import (
    Ui_CondaEnvironmentConfigurationDialog,
)


class CondaEnvironmentConfigurationDialog(
    QDialog, Ui_CondaEnvironmentConfigurationDialog
):
    """
    Class implementing a dialog to enter the parameters for the virtual environment.
    """

    def __init__(self, baseDir="", parent=None):
        """
        Constructor

        @param baseDir base directory for the virtual environments
        @type str
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        self.setupUi(self)

        if not baseDir:
            baseDir = os.path.expanduser("~")
        self.__envBaseDir = baseDir

        self.condaTargetDirectoryPicker.setMode(EricPathPickerModes.DIRECTORY_MODE)
        self.condaTargetDirectoryPicker.setWindowTitle(
            self.tr("Conda Environment Location")
        )
        self.condaTargetDirectoryPicker.setDefaultDirectory(os.path.expanduser("~"))

        self.condaCloneDirectoryPicker.setMode(EricPathPickerModes.DIRECTORY_MODE)
        self.condaCloneDirectoryPicker.setWindowTitle(
            self.tr("Conda Environment Location")
        )
        self.condaCloneDirectoryPicker.setDefaultDirectory(os.path.expanduser("~"))

        self.condaRequirementsFilePicker.setMode(EricPathPickerModes.OPEN_FILE_MODE)
        self.condaRequirementsFilePicker.setWindowTitle(
            self.tr("Conda Requirements File")
        )
        self.condaRequirementsFilePicker.setDefaultDirectory(os.path.expanduser("~"))
        self.condaRequirementsFilePicker.setFilters(
            self.tr("Text Files (*.txt);;All Files (*)")
        )

        self.condaLabel.setText(self.tr("conda Version: {0}".format(condaVersionStr())))

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)

        self.__mandatoryStyleSheet = (
            "QLineEdit {border: 2px solid; border-color: #dd8888}"
            if ericApp().usesDarkPalette()
            else "QLineEdit {border: 2px solid; border-color: #800000}"
        )
        self.condaTargetDirectoryPicker.setStyleSheet(self.__mandatoryStyleSheet)
        self.condaNameEdit.setStyleSheet(self.__mandatoryStyleSheet)

        self.condaInsecureCheckBox.setEnabled(condaVersion() >= (4, 3, 18))

        self.condaNameEdit.textChanged.connect(self.__updateOK)
        self.condaTargetDirectoryPicker.textChanged.connect(self.__updateOK)
        self.condaSpecialsGroup.clicked.connect(self.__updateOK)
        self.condaCloneNameEdit.textChanged.connect(self.__updateOK)
        self.condaCloneDirectoryPicker.textChanged.connect(self.__updateOK)
        self.condaCloneButton.clicked.connect(self.__updateOK)
        self.condaRequirementsButton.clicked.connect(self.__updateOK)
        self.condaRequirementsFilePicker.textChanged.connect(self.__updateOK)

        self.condaSpecialsGroup.clicked.connect(self.__updateUi)

        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())

    @pyqtSlot()
    def __updateOK(self):
        """
        Private method to update the enabled status of the OK button.
        """
        if isCondaAvailable():
            enable = bool(self.condaNameEdit.text()) or bool(
                self.condaTargetDirectoryPicker.text()
            )
            if self.condaSpecialsGroup.isChecked():
                if self.condaCloneButton.isChecked():
                    enable &= bool(self.condaCloneNameEdit.text()) or bool(
                        self.condaCloneDirectoryPicker.text()
                    )
                elif self.condaRequirementsButton.isChecked():
                    enable &= bool(self.condaRequirementsFilePicker.text())
            self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(enable)
        else:
            self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)

    @pyqtSlot()
    def __updateUi(self):
        """
        Private method to update the UI depending on the selected
        virtual environment creator (virtualenv or pyvenv).
        """
        enable = not self.condaSpecialsGroup.isChecked()
        self.condaPackagesEdit.setEnabled(enable)
        self.condaPythonEdit.setEnabled(enable)
        self.condaInsecureCheckBox.setEnabled(enable and condaVersion() >= (4, 3, 18))
        self.condaDryrunCheckBox.setEnabled(enable)

    def __generateArguments(self):
        """
        Private method to generate the process arguments.

        @return process arguments
        @rtype list of str
        """
        args = []
        if bool(self.condaNameEdit.text()):
            args.extend(["--name", self.condaNameEdit.text()])
        if bool(self.condaTargetDirectoryPicker.text()):
            args.extend(["--prefix", self.condaTargetDirectoryPicker.text()])
        if self.condaSpecialsGroup.isChecked():
            if self.condaCloneButton.isChecked():
                if bool(self.condaCloneNameEdit.text()):
                    args.extend(["--clone", self.condaCloneNameEdit.text()])
                elif bool(self.condaCloneDirectoryPicker.text()):
                    args.extend(["--clone", self.condaCloneDirectoryPicker.text()])
            elif self.condaRequirementsButton.isChecked():
                args.extend(["--file", self.condaRequirementsFilePicker.text()])
        if self.condaInsecureCheckBox.isChecked():
            args.append("--insecure")
        if self.condaDryrunCheckBox.isChecked():
            args.append("--dry-run")
        if not self.condaSpecialsGroup.isChecked():
            if bool(self.condaPythonEdit.text()):
                args.append("python={0}".format(self.condaPythonEdit.text()))
            if bool(self.condaPackagesEdit.text()):
                args.extend([p.strip() for p in self.condaPackagesEdit.text().split()])

        return args

    def getData(self):
        """
        Public method to retrieve the dialog data.

        @return dictionary containing the data for the environment creation. The
            key 'logicalName' contains the environment name to be used with the
            virtual environment manager and 'arguments' contains the generated
            command line arguments for the 'conda create' command.
        @rtype dict
        """
        return {
            "arguments": self.__generateArguments(),
            "logicalName": self.nameEdit.text(),
        }
