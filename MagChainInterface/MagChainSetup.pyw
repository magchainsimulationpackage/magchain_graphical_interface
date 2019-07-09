#!/usr/bin/env python3

import numpy as np

import sys, re
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QDate, Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont, QImage, QTextDocument

import os
import shutil

dir_principal = os.getcwd()

data_folder = dir_principal + '/Data'
output_folder = dir_principal + '/Outputs'

if not os.path.exists(output_folder): os.mkdir(output_folder)

class Window(QMainWindow): 
    def __init__(self):
        QMainWindow.__init__(self)

        os.chdir(data_folder)
        uic.loadUi('MagChainInterface.ui', self)

        #self.showMaximized()

        self.manage_files = ManageFiles()

        #Load files
        self.load_attradius.clicked.connect(self.obrir_load_attradius)

        self.load_input.clicked.connect(self.obrir_load_input)

        self.load_magchain.clicked.connect(self.obrir_load_magchain)

        self.load_restart_tosim.clicked.connect(self.obrir_load_restart_tosim)

        self.load_attradius_input.clicked.connect(self.obrir_load_attradius_input)

        self.load_restart.clicked.connect(self.obrir_load_restart)


        #Validate fields
        self.particles.textChanged.connect(self.validate_particles)
        self.x_box.textChanged.connect(self.validate_x_box)
        self.y_box.textChanged.connect(self.validate_y_box)
        self.z_box.textChanged.connect(self.validate_z_box)
        self.dt.textChanged.connect(self.validate_time_step)
        self.steps.textChanged.connect(self.validate_steps)
        self.stats_every.textChanged.connect(self.validate_stats)
        self.traj_every.textChanged.connect(self.validate_traj)
        self.restart_every.textChanged.connect(self.validate_restart)
        self.hist_every.textChanged.connect(self.validate_hist_every)
        self.hist_size.textChanged.connect(self.validate_hist_size)


        #Import from input or restart
        self.import_input.clicked.connect(self.import_input_file)

        #Generate attradius file
        self.attradius_dialog = Attradius_dial()
        self.generate_attradius.clicked.connect(self.open_attradius_dialog)

        #Clear all
        self.clear.clicked.connect(self.clear_parameters)

        #Export
        self.export_button.clicked.connect(self.export)


        #Run
        self.run.clicked.connect(self.run_simulation)


    #Load files
    def obrir_load_attradius(self):
        self.manage_files.openFileNameDialog(self.attradius)

    def obrir_load_input(self):
        self.manage_files.openFileNameDialog(self.input)

    def obrir_load_magchain(self):
        self.manage_files.openFileNameDialog(self.magchain)

    def obrir_load_restart_tosim(self):
        self.manage_files.openFileNameDialog(self.loaded_restart_tosim)

    def obrir_load_attradius_input(self):
        self.manage_files.copy_attradius(self.loaded_attradius_input, self.attradius_size)

    def obrir_load_restart(self):
        self.clear_parameters()
        self.manage_files.copy_restart(self.particles, self.x_box, self.y_box, self.z_box, self.dt, self.restart_imported)
        self.sim_from_restart.setChecked(True)



    #Open attradius dialog
    def open_attradius_dialog(self):
        self.attradius_dialog.exec_()


    #Create input file
    def clear_parameters(self):
        self.particles.setText('')
        self.x_box.setText('')
        self.y_box.setText('')
        self.z_box.setText('')
        self.dt.setText('')
        self.steps.setText('')

        self.stats_every.setText('')
        self.traj_every.setText('')
        self.restart_every.setText('')
        self.hist_every.setText('')
        self.hist_size.setText('')

        self.loaded_attradius_input.setText('Empty')
        self.loaded_attradius_input.setStyleSheet('color: red')

        self.attradius_size.setText('')

        self.x_box.setStyleSheet('')
        self.y_box.setStyleSheet('')
        self.z_box.setStyleSheet('')

        self.dt.setStyleSheet('')
        self.particles.setStyleSheet('')
        self.steps.setStyleSheet('')

        self.x_box.setReadOnly(False)
        self.y_box.setReadOnly(False)
        self.z_box.setReadOnly(False)

        self.dt.setReadOnly(False)
        self.particles.setReadOnly(False)

    def import_input_file(self):
        self.clear_parameters()
        self.manage_files.copy_input(self.particles, self.x_box, self.y_box, self.z_box, self.dt, self.loaded_attradius_input, self.attradius_size, self.stats_every,
                                        self.traj_every, self.restart_every, self.hist_every, self.hist_size, self.steps)


    def validate_particles(self):
        field = self.particles.text()

        validate = re.match("^[e0123456789'.-]+$", field)
        
        if field == '': #Si esta buit bordes grocs                                       
            self.particles.setStyleSheet('border: 1px solid yellow;')

            return False

        elif not validate:#Si no es valid bordes vermells
            self.particles.setStyleSheet('border: 1px solid red;')

            return False

        else:
            self.particles.setStyleSheet('border: 1px solid green;')

            return True

    def validate_x_box(self):
        field = self.x_box.text()

        validate = re.match("^[e0123456789'.-]+$", field)
        
        if field == '': #Si esta buit bordes grocs                                       
            self.x_box.setStyleSheet('border: 1px solid yellow;')

            return False

        elif not validate:#Si no es valid bordes vermells
            self.x_box.setStyleSheet('border: 1px solid red;')

            return False

        else:
            self.x_box.setStyleSheet('border: 1px solid green;')

            return True

    def validate_y_box(self):
        field = self.y_box.text()

        validate = re.match("^[e0123456789'.-]+$", field)
        
        if field == '': #Si esta buit bordes grocs                                       
            self.y_box.setStyleSheet('border: 1px solid yellow;')

            return False

        elif not validate:#Si no es valid bordes vermells
            self.y_box.setStyleSheet('border: 1px solid red;')

            return False

        else:
            self.y_box.setStyleSheet('border: 1px solid green;')

            return True

    def validate_z_box(self):
        field = self.z_box.text()

        validate = re.match("^[e0123456789'.-]+$", field)
        
        if field == '': #Si esta buit bordes grocs                                       
            self.z_box.setStyleSheet('border: 1px solid yellow;')

            return False

        elif not validate:#Si no es valid bordes vermells
            self.z_box.setStyleSheet('border: 1px solid red;')

            return False

        else:
            self.z_box.setStyleSheet('border: 1px solid green;')

            return True

    def validate_time_step(self):
        field = self.dt.text()

        validate = re.match("^[e0123456789'.-]+$", field)
        
        if field == '': #Si esta buit bordes grocs                                       
            self.dt.setStyleSheet('border: 1px solid yellow;')

            return False

        elif not validate:#Si no es valid bordes vermells
            self.dt.setStyleSheet('border: 1px solid red;')

            return False

        else:
            self.dt.setStyleSheet('border: 1px solid green;')

            return True

    def validate_steps(self):
        field = self.steps.text()

        validate = re.match("^[e0123456789'.-]+$", field)
        
        if field == '': #Si esta buit bordes grocs                                       
            self.steps.setStyleSheet('border: 1px solid yellow;')

            return False

        elif not validate:#Si no es valid bordes vermells
            self.steps.setStyleSheet('border: 1px solid red;')

            return False

        else:
            self.steps.setStyleSheet('border: 1px solid green;')

            return True

    def validate_stats(self):
        field = self.stats_every.text()

        validate = re.match("^[e0123456789'.-]+$", field)
        
        if field == '': #Si esta buit bordes grocs                                       
            self.stats_every.setStyleSheet('')

            return True

        elif not validate:#Si no es valid bordes vermells
            self.stats_every.setStyleSheet('border: 1px solid red;')

            return False

        else:
            self.stats_every.setStyleSheet('border: 1px solid green;')

            return True

    def validate_traj(self):
        field = self.traj_every.text()

        validate = re.match("^[e0123456789'.-]+$", field)
        
        if field == '': #Si esta buit bordes grocs                                       
            self.traj_every.setStyleSheet('')

            return True

        elif not validate:#Si no es valid bordes vermells
            self.traj_every.setStyleSheet('border: 1px solid red;')

            return False

        else:
            self.traj_every.setStyleSheet('border: 1px solid green;')

            return True

    def validate_restart(self):
        field = self.restart_every.text()

        validate = re.match("^[e0123456789'.-]+$", field)
        
        if field == '': #Si esta buit bordes grocs                                       
            self.restart_every.setStyleSheet('')

            return True

        elif not validate:#Si no es valid bordes vermells
            self.restart_every.setStyleSheet('border: 1px solid red;')

            return False

        else:
            self.restart_every.setStyleSheet('border: 1px solid green;')

            return True

    def validate_hist_every(self):
        field = self.hist_every.text()

        validate = re.match("^[e0123456789'.-]+$", field)
        
        if field == '': #Si esta buit bordes grocs                                       
            self.hist_every.setStyleSheet('')

            return True

        elif not validate:#Si no es valid bordes vermells
            self.hist_every.setStyleSheet('border: 1px solid red;')

            return False

        else:
            self.hist_every.setStyleSheet('border: 1px solid green;')

            return True

    def validate_hist_size(self):
        field = self.hist_size.text()

        validate = re.match("^[e0123456789'.-]+$", field)
        
        if field == '': #Si esta buit bordes grocs                                       
            self.hist_size.setStyleSheet('')

            return True

        elif not validate:#Si no es valid bordes vermells
            self.hist_size.setStyleSheet('border: 1px solid red;')

            return False

        else:
            self.hist_size.setStyleSheet('border: 1px solid green;')

            return True

    def validate_fields(self):

        doc = QTextDocument()
        doc.setHtml(self.loaded_attradius_input.text())
        text = doc.toPlainText()

        val = []

        if text == 'Empty':
            QMessageBox.warning(self, 'Warning', 'Attraction radius file must be loaded!')

            return False

        val.append(self.validate_particles())
        val.append(self.validate_x_box())
        val.append(self.validate_y_box())
        val.append(self.validate_z_box())
        val.append(self.validate_time_step())
        val.append(self.validate_steps())
        val.append(self.validate_stats())
        val.append(self.validate_traj())
        val.append(self.validate_restart())
        val.append(self.validate_hist_every())
        val.append(self.validate_hist_size())

        val = np.array(val)

        if np.any(val == False):
            QMessageBox.warning(self, 'Warning!', 'Invalid parameters!')

            return False

        else:
            return True


    #Export input or project
    def export(self):

        validation = self.validate_fields()

        if validation == False:
            pass
        
        else:

            filename = self.manage_files.saveFileDialog()

            f = open(filename, 'w')

            f.write('#Template generated by MagChainInterface v1.0\n\n')

            if self.sim_from_restart.isChecked():
                f.write('restart_data' + ' ' + self.restart_imported.text() + '\n')

            f.write('nparticles\t' + self.particles.text() + '\n')
            f.write('sbox\t' + self.x_box.text() + ' ' + self.y_box.text() + ' ' + self.z_box.text() + '\n')
            f.write('timestep\t' + self.dt.text() + '\n\n')

            f.write('attradius\t' + self.loaded_attradius_input.text() + ' ' + self.attradius_size.text() + '\n')


            if self.stats_every.text() != '': f.write('stats_every\t' + self.stats_every.text() + '\n')
            if self.traj_every.text() != '': f.write('traj_every\t' + self.traj_every.text() + '\n')
            if self.restart_every.text() != '': f.write('restart_every\t' + self.restart_every.text() + '\n')

            if self.hist_every.text() != '' and self.hist_size.text() != '': 
                f.write('hist_every\t' + self.hist_every.text() + '' + self.hist_size.text() + '\n')
            
            elif self.hist_every.text() != '' and self.hist_size.text() == '':
                f.write('hist_every\t' + self.hist_every.text() + '\n')

            if self.equil.isChecked():
                f.write('\nequil\t' + self.steps.text())

            else:
                f.write('\nrun\t' + self.steps.text())

            f.close()



    #Run simulation

    def get_name(self, filename):
        dirs = []
        this = ''

        for item in filename:

            if item != '/':
                this = this + str(item)
                
            elif item == '/':
                dirs.append(this)
                this = ''

        dirs.append(this)

        return dirs[-1]
    
    def copy_files(self):
        #Copy the files into the data folder

        attradius_file = self.attradius.text()
        input_file = self.input.text()
        magchain_file = self.magchain.text()
        restart_file = self.loaded_restart_tosim.text()

        all_correct = False
        total_filename = ''

        if attradius_file == '':
            QMessageBox.warning(self, 'Warning!', 'attradius file not loaded!')

        elif input_file == '':
            QMessageBox.warning(self, 'Warning!', 'Input file not loaded!')

        elif magchain_file == '':
            QMessageBox.warning(self, 'Warning!', 'MagChain executable not loaded!')

        else:

            attradius_name = self.get_name(attradius_file)
            input_name = self.get_name(input_file)
            magchain_name = self.get_name(magchain_file)

            if restart_file != '':
                restart_name = self.get_name(restart_file)

                shutil.copy(restart_file, output_folder + '/' + restart_name)

            shutil.copy(attradius_file, output_folder + '/' + attradius_name)
            shutil.copy(input_file, output_folder + '/' + input_name)
            shutil.copy(magchain_file, output_folder + '/' + magchain_name)

            magchain_filename = output_folder + '/' + magchain_name
            input_filename = output_folder + '/' + input_name

            total_filename = magchain_filename + ' ' + input_filename

            all_correct = True

        return total_filename, all_correct

    def run_simulation(self):

        total_filename, all_correct = self.copy_files()

        if all_correct:

            os.chdir(output_folder)

            os.system(total_filename)

    #close event
    def closeEvent(self, event):
        result = QMessageBox.question(self, 'Leaving...','Do you want to exit?', QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.Yes:

            event.accept()  
        else:
            event.ignore()


class ManageFiles(QFileDialog):
    def __init__(self):
        QFileDialog.__init__(self)

        self.title = 'Save files'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400 

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fileName, _ = QFileDialog.getSaveFileName(self, 'Save files') 

        if fileName:
            return fileName

    def openFileNameDialog(self, name):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)

        if fileName:
            name.setText(fileName)

    def copy_attradius(self, loaded_attradius_input, attradius_size):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)

        if fileName:

            dirs = []
            this = ''

            for item in fileName:

                if item != '/':
                    this = this + str(item)
                    
                elif item == '/':
                    dirs.append(this)
                    this = ''

            dirs.append(this)

            loaded_attradius_input.setText(dirs[-1])
            loaded_attradius_input.setStyleSheet('color: black')   

            f = open(fileName, 'r')

            lines = f.readlines()

            size = lines[-1].split()[0]

            attradius_size.setText(size)

            f.close()

    def copy_input(self, particles, x_box, y_box, z_box, dt, loaded_attradius_input, attradius_size, stats_every, traj_every, restart_every, hist_every, hist_size, steps):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)

        if fileName:
            
            f = open(fileName, 'r')

            for line in f:
                cols = line.split()

                if len(cols) > 0:

                    if cols[0] == 'nparticles':
                        particles.setText(cols[1])

                    elif cols[0] == 'sbox':
                        x_box.setText(cols[1])
                        y_box.setText(cols[2])
                        z_box.setText(cols[3])

                    elif cols[0] == 'timestep':
                        dt.setText(cols[1])

                    elif cols[0] == 'attradius':
                        loaded_attradius_input.setText(cols[1])
                        loaded_attradius_input.setStyleSheet('color: black')

                        attradius_size.setText(cols[2])

                    elif cols[0] == 'stats_every':
                        stats_every.setText(cols[1])

                    elif cols[0] == 'traj_every':
                        traj_every.setText(cols[1])

                    elif cols[0] == 'restart_every':
                        restart_every.setText(cols[1])

                    elif cols[0] == 'hist_every':
                        hist_every.setText(cols[1])

                        try:
                            hist_size.setText(cols[2])
                        except:
                            pass

                    elif cols[0] == 'run':
                        steps.setText(cols[1])

    def copy_restart(self, particles, x_box, y_box, z_box, dt, restart_name):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)

        if fileName:
            
            f = open(fileName, 'r')

            counter = 0

            for line in f:

                cols = line.split()

                if counter == 4:

                    particles.setText(cols[0])

                    particles.setStyleSheet('background: gray;')

                    particles.setReadOnly(True)

                elif counter == 7:

                    x_box.setText(cols[0])
                    y_box.setText(cols[1])
                    z_box.setText(cols[2])

                    x_box.setStyleSheet('background: gray;')
                    y_box.setStyleSheet('background: gray;')
                    z_box.setStyleSheet('background: gray;')

                    x_box.setReadOnly(True)
                    y_box.setReadOnly(True)
                    z_box.setReadOnly(True)

                elif counter == 10:

                    dt.setText(cols[0])

                    dt.setStyleSheet('background: gray;')
                    dt.setReadOnly(True)

                counter += 1

            dirs = []
            this = ''

            for item in fileName:

                if item != '/':
                    this = this + str(item)
                    
                elif item == '/':
                    dirs.append(this)
                    this = ''

            dirs.append(this)

            restart_name.setText(dirs[-1])
            restart_name.setStyleSheet('color: black')
               
    def openFolderDialog(self, name):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fileName = str(QFileDialog.getExistingDirectory(self, 'Select folder', options=options))

        if fileName:
            name.setText(fileName)


class calc_attradius(object):
    def __init__(self, gamma, maxsize):
        
        self.gamma = gamma
        self.maxsize = maxsize

        self.tolerance = 1e-3
        self.minsize = 1
        self.dx = 0.01
        self.utarget = -1.0
        self.xmin = 1.0
        self.xmax = 50.0
        self.u = 0.0

    def EvalEnergy(self, m, x):
        energy = 0.0
        d = 0.0
        
        for i in range(1, m+1):
            
            d = x + (i-1)
            d = d**3
            energy += 1/d

        
        energy *= -self.gamma

        return energy

    def makefile(self, filename, progressBar):

        radiusfile = open(filename + '.dat', 'w')

        radiusfile.write('#size attradius(gamma=%.2f)\n' % self.gamma)

        for i in range(self.minsize, self.maxsize + 1):

            radiusfile.write(str(i))
            progressBar.setValue(i/(self.maxsize + 1) * 100)

            x = self.xmin + (self.xmax - self.xmin)*np.random.uniform(0, 1)
                
            self.u = self.EvalEnergy(i, x)
              
            while abs(self.u - self.utarget) > self.tolerance:

                if self.u - self.utarget < 0:
                    x = x + (self.xmax - x) * np.random.uniform(0, 1)

                else:
                    x = x - (x - self.xmin) * np.random.uniform(0, 1)               

                self.u = self.EvalEnergy(i, x)
            
            radiusfile.write("\t" + str((x-0.5)/2.0) + '\n')

        radiusfile.close()
    
class Attradius_dial(QDialog):
    
    def __init__(self):
        QDialog.__init__(self)

        os.chdir(data_folder)
        uic.loadUi('attradius_dialog.ui', self)

        self.generate_file.clicked.connect(self.obrir_generate_file)

    def obrir_generate_file(self):

        manage_files = ManageFiles()

        filename = manage_files.saveFileDialog()

        gamma = self.gamma.value()
        max_size = self.max_size.value()

        CA = calc_attradius(gamma, max_size)

        if (CA.EvalEnergy(max_size, CA.xmax) < CA.utarget):

            QMessageBox.warning(self, 'Warning!', 'increase xmax! = %.2f' % CA.xmax)
            
        if (CA.EvalEnergy(CA.minsize, CA.xmin) > CA.utarget):

            QMessageBox.warning(self, 'Warning!', 'decrease xmin! = %.2f' % CA.xmin)


        CA.makefile(filename, self.progressBar)

        QMessageBox.information(self, 'Information', 'Attraction rdius file generated properly!')
        self.progressBar.setValue(0)
        
            
app = QApplication(sys.argv)
_window=Window()
_window.show()
app.exec_()