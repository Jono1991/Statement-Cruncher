from PyQt6.QtWidgets import QApplication, QMainWindow, QInputDialog, QLabel, QTableWidget,\
    QTableWidgetItem, QFileDialog, QMessageBox
from PyQt6.uic import loadUi
import sys
import pathlib
import database_functions

class StatementCruncher(QMainWindow):
    def __init__(self):
        super(StatementCruncher, self).__init__()
        loadUi('main_ui.ui', self)

        self.rowCount = 0
        self.dates = []
        self.accountnumbers = []
        self.references = []
        self.debitamounts = []
        self.creditamounts = []
        self.maxRow = 0

        self.table = self.findChild(QTableWidget, 'tableWidget')
        self.table.setRowCount(1000)
        self.incomingsLabelPrice = self.findChild(QLabel, 'incomingsLabelPrice')
        self.outgoingsLabelPrice = self.findChild(QLabel, 'outgoingsLabelPrice')
        self.actionNew.triggered.connect(self.new)
        self.actionAdd_Row.triggered.connect(self.create_row)
        self.actionDelete_row.triggered.connect(self.erase_row)
        self.actionImport_Wizard.triggered.connect(self.import_wizard)
        self.actionMege_Rows.triggered.connect(self.merge_rows)
        self.actionPrint.triggered.connect(self.print_file)
        self.actionExit.triggered.connect(self.exit)

    def exit(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Statement Cruncher')
        dlg.setText('Are you sure you would like to leave?')
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            QApplication.exit()
        else:
            pass

    def print_file(self):
        print("Converting Table to Text Area....")


    def new(self):
        self.table.setRowCount(0)
    def import_wizard(self):
        filepath = QFileDialog.getOpenFileName(self, 'Open bank export')
        fileExt = pathlib.Path(filepath[0]).suffix

        if fileExt == '.csv':

            # Reset the database after each press
            database_functions.clear_table('statement')
            database_functions.extract_data(filepath[0])

            # Displaying total values as labels
            self.incomingsLabelPrice.setText(database_functions.save_total('statement')[0])
            self.outgoingsLabelPrice.setText(database_functions.save_total('statement')[1])

            # Rendering the data on the screen
            database_functions.insert_data('statement', self.table)

        else:
            msg = QMessageBox(self)
            msg.setWindowTitle("Warning")
            msg.setText("File must be a spreadsheet (xlsx or CSV)")
            x = msg.exec()

    def add_row(self, column, list):
        for item in range(self.maxRow):
            self.table.setItem(item, column, QTableWidgetItem(list[item]))

    def create_row(self):
        if self.table.currentRow() == -1:
            self.table.insertRow(0)
        else:
            rowSelected = self.table.currentRow()
            self.table.insertRow(rowSelected+1)

    def erase_row(self):
        if self.table.currentRow() == -1:
            msg = QMessageBox(self)
            msg.setWindowTitle("Warning")
            msg.setText("Nothing to erase!")
            x = msg.exec()
        else:
            rowSelected = self.table.currentRow()
            self.table.removeRow(rowSelected)

    def merge_rows(self):
        title = "Filter"
        label = "Type in a transaction description to merge prices on...."
        data, okay = QInputDialog.getText(self, title, label)

        if okay:
            database_functions.merge_values('statement', data, self.table)
            database_functions.clear_table('statement')
            database_functions.send_to_database('statement', self.table)


app = QApplication([])
window = StatementCruncher()
window.show()
sys.exit(app.exec())