import json

from PyQt5 import QtWidgets, QtCore, QtGui

from components.job_queue import JobState


class QueueTable(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.editEnabled = False

        self.setSelectionBehavior(self.SelectRows)
        self.setEnabled(False)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.setColumnCount(9)
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(['Source', 'Function', 'Parameters', 'API Keys', 'Path', 'Status', 'Write mode', 'Encoding', 'Key column'])
        # self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)

    @QtCore.pyqtSlot(list)
    def display_jobs(self, jobs):
        self.clearSelection()
        if len(jobs) > 0:
            self.setEnabled(True)
        else:
            self.setEnabled(False)
        self.setRowCount(len(jobs))

        editing = True
        for row, job in enumerate(jobs):

            if editing and job.state == JobState.RUNNING:
                self.editing = False
                self.editEnabled = False

            sourceName = QtWidgets.QTableWidgetItem(job.sourceName)
            sourceFunction = QtWidgets.QTableWidgetItem(job.sourceFunction)
            functionArgs = QtWidgets.QTableWidgetItem(job.functionArgs)
            sourceKeys = QtWidgets.QTableWidgetItem(json.dumps(job.sourceKeys))
            outputPath = QtWidgets.QTableWidgetItem(job.outputPath)
            status = QtWidgets.QTableWidgetItem(job.state.value)
            write_mode = QtWidgets.QTableWidgetItem('Append' if job.append else 'Overwrite')
            encoding = QtWidgets.QTableWidgetItem(job.encoding)
            key_column = QtWidgets.QTableWidgetItem('Enabled' if job.keyColumn else 'Disabled')

            self.setItem(row, 0, sourceName)
            self.setItem(row, 1, sourceFunction)
            self.setItem(row, 2, functionArgs)
            self.setItem(row, 3, sourceKeys)
            self.setItem(row, 4, outputPath)
            self.setItem(row, 5, status)
            self.setItem(row, 6, write_mode)
            self.setItem(row, 7, encoding)
            self.setItem(row, 8, key_column)

    def selected_jobs(self):
        rows = set()
        for cell in self.selectedIndexes():
            rows.add(cell.row())
        return list(rows)

    @QtCore.pyqtSlot(list)
    def select_jobs(self, rows):
        for row in rows:
            for col in range(self.columnCount()):
                item = self.itemAt(row, col)
                item.setSelected(True)
        pass
