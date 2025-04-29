#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Standalone Inversion Application for Pyckster

This module provides a PyQt window for loading .sgt files,
running inversions, and visualizing results without using core.py.
"""

import sys
import os
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QFileDialog, QGroupBox, QFormLayout,QComboBox,
    QDoubleSpinBox, QSpinBox, QCheckBox, QMessageBox, QSplitter,QSizePolicy
)
from PyQt5.QtCore import Qt, QLocale
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# Try different import approaches
try:
    # Try relative import first (when part of a package)
    from .visualization_utils import InversionVisualizations
except ImportError:
    try:
        # Try absolute import next (when package is installed)
        from pyckster.visualization_utils import InversionVisualizations
    except ImportError:
        # Finally try direct import (when in same directory)
        from visualization_utils import InversionVisualizations

# Import the tab factory at the top of your file
try:
    from tab_factory import TabFactory
except ImportError:
    try:
        from pyckster.tab_factory import TabFactory
    except ImportError:
        from .tab_factory import TabFactory

class StandaloneInversionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window title
        self.setWindowTitle("PyGIMLI Inversion Tool")
        
        # Initialize class variables
        self.sgt_file = None
        self.refrac_manager = None
        
        # Default inversion parameters
        self.params = {
            'vTop': 300,
            'vBottom': 3000,
            'secNodes': 2,
            'paraDX': 0.33,
            'paraDepth': None,
            'balanceDepth': False,
            'paraMaxCellSize': None,
            'zWeight': 0.5,
            'lam': 30,
            'maxIter': 6,
            'verbose': True,
        }
        
        # Create the UI
        self.initUI()
    
    def initUI(self):
        # Set locale to use period as decimal separator
        locale = QLocale(QLocale.C)  # C locale uses period as decimal separator
        QLocale.setDefault(locale)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # # Create top information bar (just file info, no button)
        # top_layout = QHBoxLayout()
        # self.file_label = QLabel("No SGT file selected")
        # top_layout.addWidget(self.file_label)
        # main_layout.addLayout(top_layout)
        
        # Create splitter for parameter panel and visualization
        splitter = QSplitter(Qt.Horizontal)
        # Make sure the splitter expands to fill available space
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Create left panel for parameters
        param_widget = QWidget()
        param_layout = QVBoxLayout(param_widget)

        # After creating the param_widget
        param_widget = QWidget()
        # Set a minimum width but allow it to be as narrow as possible by default
        param_widget.setMinimumWidth(300)  # Minimum width to ensure controls are usable
        # param_widget.setMaximumWidth(300)  # Optional: prevent it from getting too wide
        param_layout = QVBoxLayout(param_widget)

        # Add Load SGT File button at the top
        load_file_button = QPushButton("Load SGT File")
        load_file_button.clicked.connect(self.loadSgtFile)
        param_layout.addWidget(load_file_button)

        # Add file information label directly below the load button
        self.file_label = QLabel("No SGT file selected")
        self.file_label.setWordWrap(True)  # Allow text to wrap
        param_layout.addWidget(self.file_label)

        # Add Time Correction button below 
        correct_time_button = QPushButton("Correct Time Picks")
        correct_time_button.clicked.connect(self.correctTimePicks)
        param_layout.addWidget(correct_time_button)

        # Create time correction parameter group
        time_correction_group = QGroupBox("Time Correction Parameters")
        time_correction_form = QFormLayout()

        # Velocity source selection
        self.velocity_mode_combo = QComboBox()
        self.velocity_mode_combo.addItem("Constant Velocity", "constant")
        self.velocity_mode_combo.addItem("Surface Velocity (Calculated)", "surface")
        time_correction_form.addRow("Velocity Source:", self.velocity_mode_combo)

        # Constant velocity parameter
        self.corr_velocity_spin = QDoubleSpinBox()
        self.corr_velocity_spin.setRange(100, 5000)
        self.corr_velocity_spin.setValue(300)  # Default value
        self.corr_velocity_spin.setSingleStep(50)
        time_correction_form.addRow("Constant Velocity (m/s):", self.corr_velocity_spin)

        # Surface velocity parameters
        self.surf_velocity_smooth_check = QCheckBox()
        self.surf_velocity_smooth_check.setChecked(True)
        self.surf_velocity_smooth_check.setEnabled(False)  # Initially disabled
        time_correction_form.addRow("Smooth Surface Velocity:", self.surf_velocity_smooth_check)

        self.surf_velocity_window_spin = QSpinBox()
        self.surf_velocity_window_spin.setRange(3, 21)
        self.surf_velocity_window_spin.setValue(9)
        self.surf_velocity_window_spin.setSingleStep(2)
        self.surf_velocity_window_spin.setEnabled(False)  # Initially disabled
        time_correction_form.addRow("Smoothing Window:", self.surf_velocity_window_spin)

        # Connect velocity mode combo to enable/disable related controls
        self.velocity_mode_combo.currentIndexChanged.connect(self.updateVelocityControls)

        # Set locale for numeric inputs
        self.corr_velocity_spin.setLocale(locale)

        # Add form to group
        time_correction_group.setLayout(time_correction_form)

        # Add group to param layout (between buttons and inversion parameters)
        param_layout.addWidget(time_correction_group)

        # Add Run Inversion button below
        run_button = QPushButton("Run Inversion")
        run_button.clicked.connect(self.runInversion)
        param_layout.addWidget(run_button)
        
        # Create parameter group
        param_group = QGroupBox("Inversion Parameters")
        param_form = QFormLayout()
        
        # Create parameter spinboxes
        self.vTop_spin = QDoubleSpinBox()
        self.vTop_spin.setRange(100, 5000)
        self.vTop_spin.setValue(self.params['vTop'])
        self.vTop_spin.setSingleStep(50)
        param_form.addRow("Top Velocity (m/s):", self.vTop_spin)
        
        self.vBottom_spin = QDoubleSpinBox()
        self.vBottom_spin.setRange(500, 10000)
        self.vBottom_spin.setValue(self.params['vBottom'])
        self.vBottom_spin.setSingleStep(100)
        param_form.addRow("Bottom Velocity (m/s):", self.vBottom_spin)
        
        self.secNodes_spin = QSpinBox()
        self.secNodes_spin.setRange(1, 10)
        self.secNodes_spin.setValue(self.params['secNodes'])
        param_form.addRow("Secondary Nodes:", self.secNodes_spin)
        
        self.paraDX_spin = QDoubleSpinBox()
        self.paraDX_spin.setRange(0.1, 2.0)
        self.paraDX_spin.setValue(self.params['paraDX'])
        self.paraDX_spin.setDecimals(2)
        self.paraDX_spin.setSingleStep(0.05)
        param_form.addRow("Para DX (m):", self.paraDX_spin)
        
        self.paraDepth_spin = QDoubleSpinBox()
        self.paraDepth_spin.setRange(0, 100)
        self.paraDepth_spin.setValue(20)  # Default value if None
        self.paraDepth_spin.setSingleStep(1)
        self.paraDepth_spin.setSpecialValueText("Auto")  # 0 means Auto (None)
        param_form.addRow("Para Depth (m):", self.paraDepth_spin)
        
        self.balanceDepth_check = QCheckBox()
        self.balanceDepth_check.setChecked(self.params['balanceDepth'])
        param_form.addRow("Balance Depth:", self.balanceDepth_check)
        
        self.zWeight_spin = QDoubleSpinBox()
        self.zWeight_spin.setRange(0.1, 1.0)
        self.zWeight_spin.setValue(self.params['zWeight'])
        self.zWeight_spin.setDecimals(2)
        self.zWeight_spin.setSingleStep(0.05)
        param_form.addRow("Z Weight:", self.zWeight_spin)
        
        self.lam_spin = QDoubleSpinBox()
        self.lam_spin.setRange(1, 100)
        self.lam_spin.setValue(self.params['lam'])
        self.lam_spin.setSingleStep(1)
        param_form.addRow("Lambda:", self.lam_spin)
        
        self.maxIter_spin = QSpinBox()
        self.maxIter_spin.setRange(1, 20)
        self.maxIter_spin.setValue(self.params['maxIter'])
        param_form.addRow("Max Iterations:", self.maxIter_spin)
        
        self.verbose_check = QCheckBox()
        self.verbose_check.setChecked(self.params['verbose'])
        param_form.addRow("Verbose:", self.verbose_check)

        # For each QDoubleSpinBox, explicitly set the locale
        self.vTop_spin.setLocale(locale)
        self.vBottom_spin.setLocale(locale)
        self.paraDX_spin.setLocale(locale)
        self.paraDepth_spin.setLocale(locale)
        self.zWeight_spin.setLocale(locale)
        self.lam_spin.setLocale(locale)
        
        # Add form to group
        param_group.setLayout(param_form)
        
        # Add group to param layout (now below the buttons)
        param_layout.addWidget(param_group)
        
        # Add stretcher to push everything up
        param_layout.addStretch()
        
        # Add param widget to splitter
        splitter.addWidget(param_widget)

        # Set initial sizes to make the left panel very narrow
        splitter.setSizes([100, 900])  # Give only 10% of space to the menu initially
        
        # First, create the right panel that will hold the tabs
        viz_widget = QWidget()
        viz_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        viz_layout = QVBoxLayout(viz_widget)

        # Create the tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        viz_layout.addWidget(self.tab_widget)

        # Create tabs using the factory
        self.data_tab = TabFactory.create_data_tab(self)
        self.models_tab = TabFactory.create_models_tab(self)
        self.traveltimes_tab = TabFactory.create_traveltimes_tab(self)
        self.source_receiver_tab = TabFactory.create_source_receiver_tab(self)
        
        # Add tabs to tab widget
        self.tab_widget.addTab(self.data_tab, "Data")
        self.tab_widget.addTab(self.models_tab, "Models")
        self.tab_widget.addTab(self.traveltimes_tab, "Traveltimes")
        self.tab_widget.addTab(self.source_receiver_tab, "Source vs Receiver")

        # Add the viz widget to the main splitter
        splitter.addWidget(viz_widget)
 
        # Set initial sizes for splitter (20% for menu, 80% for figures)
        splitter.setSizes([200, 800])
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)

        # Set stretch factors to control how extra space is distributed when maximizing
        splitter.setStretchFactor(0, 0)  # Parameter panel (left) should not stretch
        splitter.setStretchFactor(1, 1)  # Visualization panel (right) gets all extra space 
        
        # Set window size
        self.resize(1000, 700)
    
    def loadSgtFile(self):
        """Load a .sgt file using a file dialog"""
        fname, _ = QFileDialog.getOpenFileName(
            self, 'Load SGT File', '', 'SGT Files (*.sgt)')
        
        if fname:
            self.sgt_file = fname
            self.file_label.setText(f"File: {os.path.basename(fname)}")
            
            # Load the file and initialize the refraction manager
            try:
                import pygimli as pg
                from pygimli.physics import TravelTimeManager as refrac
                self.refrac_manager = refrac(fname)

                # Generate mesh and assign it to the manager


                # Print number of shots and picks imported
                num_shots = len(np.unique(self.refrac_manager.data['s']))
                num_geo = len(np.unique(self.refrac_manager.data['g']))
                num_picks = len(self.refrac_manager.data['t'])
                self.file_label.setText(f"File: {os.path.basename(fname)}\n"
                                        f"Shots: {num_shots}\n"
                                        f"Receivers: {num_geo}\n"
                                        f"Picks: {num_picks}")
                
                # After successful loading, display the visualization
                self.showDataTab()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load SGT file: {str(e)}")
                import traceback
                traceback.print_exc()
                self.sgt_file = None
                self.refrac_manager = None
                return
        else:
            self.file_label.setText("No SGT file selected")
            self.sgt_file = None
            self.refrac_manager = None
            
            # Reset parameters to defaults
            self.params = {
                'vTop': 300,
                'vBottom': 3000,
                'secNodes': 2,
                'paraDX': 0.33,
                'paraDepth': None,
                'balanceDepth': False,
                'paraMaxCellSize': None,
                'zWeight': 0.5,
                'lam': 30,
                'maxIter': 6,
                'verbose': True,
            }
            
            # Update the existing tab with empty content
            new_data_tab = TabFactory.create_data_tab(self)
            self.tab_widget.removeTab(0)
            self.tab_widget.insertTab(0, new_data_tab, "Data")
            self.data_tab = new_data_tab
            self.tab_widget.setCurrentIndex(0)

    def showDataTab(self):
        """Update visualization in the Data tab"""
        if not self.refrac_manager:
            return
            
        # Create new data tab content
        new_data_tab = TabFactory.create_data_tab(
            self, self.refrac_manager, self.params
        )
        
        # Replace the content in the existing tab index
        self.tab_widget.removeTab(0)
        self.tab_widget.insertTab(0, new_data_tab, "Data")
        self.data_tab = new_data_tab  # Update the reference
        
        # Switch to the Data tab
        self.tab_widget.setCurrentIndex(0)

    def showModelTab(self):
        """Update visualization in the Model tab"""
        if not self.refrac_manager:
            QMessageBox.warning(self, "Warning", "No inversion results to display.")
            return
        
        # Create new model tab content
        new_model_tab = TabFactory.create_models_tab(
            self, self.refrac_manager, self.params
        )
        
        # Replace the content in the existing tab index
        self.tab_widget.removeTab(1)
        self.tab_widget.insertTab(1, new_model_tab, "Models")
        self.model_tab = new_model_tab  # Update the reference
        
        # Switch to the Models tab
        self.tab_widget.setCurrentIndex(1)

    def showTraveltimesTab(self):
        """Update visualization in the Traveltimes tab"""
        if not self.refrac_manager:
            QMessageBox.warning(self, "Warning", "No inversion results to display.")
            return
        
        # Create new traveltimes tab content
        new_traveltimes_tab = TabFactory.create_traveltimes_tab(
            self, self.refrac_manager, self.params
        )
        
        # Replace the content in the existing tab index
        self.tab_widget.removeTab(2)
        self.tab_widget.insertTab(2, new_traveltimes_tab, "Traveltimes")
        self.traveltimes_tab = new_traveltimes_tab

    def showSourceReceiverTab(self):
        """Update visualization in the Source vs Receiver tab"""
        if not self.refrac_manager:
            QMessageBox.warning(self, "Warning", "No inversion results to display.")
            return
        
        # Create new source-receiver tab content
        new_source_receiver_tab = TabFactory.create_source_receiver_tab(
            self, self.refrac_manager, self.params
        )
        
        # Replace the content in the existing tab index
        self.tab_widget.removeTab(3)
        self.tab_widget.insertTab(3, new_source_receiver_tab, "Source vs Receiver")
        self.source_receiver_tab = new_source_receiver_tab
        
    def getInversionParams(self):
        """Get inversion parameters from UI controls"""
        self.params['vTop'] = self.vTop_spin.value()
        self.params['vBottom'] = self.vBottom_spin.value()
        self.params['secNodes'] = self.secNodes_spin.value()
        self.params['paraDX'] = self.paraDX_spin.value()
        
        # Handle special value for paraDepth
        paraDepth_value = self.paraDepth_spin.value()
        self.params['paraDepth'] = None if paraDepth_value == 0 else paraDepth_value
        
        self.params['balanceDepth'] = self.balanceDepth_check.isChecked()
        self.params['zWeight'] = self.zWeight_spin.value()
        self.params['lam'] = self.lam_spin.value()
        self.params['maxIter'] = self.maxIter_spin.value()
        self.params['verbose'] = self.verbose_check.isChecked()
        
        return self.params
    
    def runInversion(self):
        """Run the inversion using the current parameters"""
        if not self.sgt_file:
            QMessageBox.warning(self, "Warning", "Please load an SGT file first.")
            return
        
        # Check if PyGIMLI is installed
        try:
            import pygimli as pg
        except ImportError:
            QMessageBox.critical(self, "Error", "PyGIMLI is not installed. Please install it to run the inversion.")
            return
        
        # Get parameters from UI
        params = self.getInversionParams()

        # Check if the parameters are valid
        if np.any(self.refrac_manager.data['t'] < 0):
            # Open a dialog to inform the user about negative times and allow them to proceed with correctTimePicks
            reply = QMessageBox.question(
                self, "Negative Times Detected",
                "Negative times detected in the data. Would you like to correct them before running the inversion?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.correctTimePicks()
                self.showDataTab()
            else:
                return
        
        try:
            # Try to import the inversion manager module
            try:
                from inversion_manager import run_inversion
            except ImportError:
                try:
                    from pyckster.inversion_manager import run_inversion
                except ImportError:
                    QMessageBox.critical(self, "Error", "Could not import inversion_manager module.")
                    return
            
            # Run the inversion
            self.refrac_manager = run_inversion(
                sgt_file=self.sgt_file,
                params=params
            )
            
            # Display the results
            # self.displayInversionResults()

            self.showModelTab()
            self.showTraveltimesTab()
            self.showSourceReceiverTab()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Inversion failed: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def displayInversionResults(self):
        """Open the InversionVisualizer to display results"""
        if not self.refrac_manager:
            QMessageBox.warning(self, "Warning", "No inversion results to display.")
            return
        
        try:
            # Try to import the visualizer module
            try:
                from inversion_visualizer import InversionVisualizer
            except ImportError:
                try:
                    from pyckster.inversion_visualizer import InversionVisualizer
                except ImportError:
                    QMessageBox.critical(self, "Error", "Could not import inversion_visualizer module.")
                    return
            
            # Create and show the visualizer window
            visualizer = InversionVisualizer(self.refrac_manager, self.params)
            visualizer.show()
            
            # Keep a reference to prevent garbage collection
            self.visualizer = visualizer
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to display results: {str(e)}")
            import traceback
            traceback.print_exc()

    def correctTimePicks(self):
        """Perform time correction on the loaded data"""
        if not self.refrac_manager:
            QMessageBox.warning(self, "Warning", "Please load an SGT file first.")
            return
        
        try:
            # Try to import the time correction function from inversion_manager
            try:
                from inversion_manager import correct_time_picks
            except ImportError:
                try:
                    from pyckster.inversion_manager import correct_time_picks
                except ImportError:
                    QMessageBox.critical(self, "Error", "Could not import time correction function.")
                    return
            
            # Get parameters from the time correction menu
            min_velocity = self.corr_velocity_spin.value()
            
            # Create a backup of the original data
            original_times = np.copy(self.refrac_manager.data['t'])

            # Apply the time correction with all parameters
            correct_time_picks(
                self.refrac_manager, 
                min_velocity=min_velocity,
            )
            
            # Refresh the visualization
            self.showDataTab()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Time correction failed: {str(e)}")
            import traceback
            traceback.print_exc()

    # Add this method to the StandaloneInversionApp class
    def updateVelocityControls(self):
        """Enable/disable velocity controls based on selected mode"""
        mode = self.velocity_mode_combo.currentData()
        
        # Enable/disable constant velocity control
        self.corr_velocity_spin.setEnabled(mode == "constant")
        
        # Enable/disable surface velocity controls
        self.surf_velocity_smooth_check.setEnabled(mode == "surface")
        self.surf_velocity_window_spin.setEnabled(mode == "surface" and 
                                            self.surf_velocity_smooth_check.isChecked())
        
        # Connect smooth checkbox to window spin state
        self.surf_velocity_smooth_check.stateChanged.connect(
            lambda state: self.surf_velocity_window_spin.setEnabled(
                mode == "surface" and state == Qt.Checked))

def main():
    """Main function to run the standalone application"""
    app = QApplication(sys.argv)
    window = StandaloneInversionApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()