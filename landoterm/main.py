import sys
import logging
import serial
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, QComboBox, QHBoxLayout

logging.basicConfig(filename='landoterm.log', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class serialCom:
    def __init__(self, port: str, baudrate: int):
        self.port = port
        self.baudrate = baudrate
    
    def open(self):
        try:
            self.s = serial.Serial(self.port, self.baudrate)
        except Exception as e:
            logging.error(e)
            return 'Error: Unable to open serial port'

    def send(self, data: str):
        try:
            self.s.write(data.encode())
            return self.s.readline().decode()
        except Exception as e:
            logging.error(e)

    def listen(self):
        try:
            return self.s.readline().decode()
        except Exception as e:
            logging.error(e)

    def close(self):
        try:
            self.s.close()
        except Exception as e:
            logging.error(e)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LandoTerm")
        self.resize(800, 600)
        self.ports = ['COM1', 'COM2', 'COM3', 'COM4']
        # self.update_ports()

        self.port_label = QLabel("Port:", self)
        self.port_dropdown = QComboBox(self)
        self.refresh_button = QPushButton("↻", self)
        self.refresh_button.setFixedSize(26, 26)
        self.baudrate_label = QLabel("Baudrate:", self)
        self.baudrate_dropdown = QComboBox(self)
        self.port_dropdown.addItems(self.ports)
        self.baudrate_dropdown.addItems(map(str, [1200, 2400, 9600, 19200, 38400, 57600, 115200]))
        self.connect_button = QPushButton("Connect", self)
        self.output_box = QLabel(self)


        # Set layout
        main_layout = QVBoxLayout()

        # Create a horizontal layout to combine port, baudrate, and connect button
      
        port_layout = QHBoxLayout()
        port_layout.addWidget(self.port_label)
        port_layout.addWidget(self.port_dropdown)
        port_layout.addWidget(self.refresh_button)
        self.port_label.setFixedWidth(36)  # Set fixed width for port_label
        port_layout.setStretch(1, 3)  # Stretch for port_dropdown
        baud_layout = QHBoxLayout()
        baud_layout.addWidget(self.baudrate_label)
        baud_layout.addWidget(self.baudrate_dropdown)
        self.baudrate_label.setFixedWidth(65)  # No stretch for baudrate_label
        baud_layout.setStretch(1, 3)  # Stretch for baudrate_dropdown
        bar_layout = QHBoxLayout()
        bar_layout.addLayout(port_layout)
        bar_layout.addLayout(baud_layout)
        bar_layout.addWidget(self.connect_button)

        bar_layout.setStretch(0, 4)  # No stretch for port_label
        bar_layout.setStretch(1, 3)  # Stretch for port_dropdown
        bar_layout.setStretch(2, 3)  # No stretch for baudrate_label

        # Add the combined horizontal layout and output box to the main layout
        main_layout.addLayout(bar_layout)
        main_layout.addWidget(self.output_box)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.connect_button.clicked.connect(self.connect)


    def update_port_list(self):
        try:
            ports = self.settings.get_ports()
            return ports
        except Exception as e:
            logging.error(e)
            return []

    def connect(self):
        selected_port = self.port_dropdown.currentText()
        selected_baudrate = self.baudrate_dropdown.currentText()
        logging.info(f"Connecting to {selected_port} with baudrate {selected_baudrate}")
        #TODO Implement connection logic here

    def update_ports(self):
        try:
            self.ports = ['COM1', 'COM2', 'COM3', 'COM4']
            # self.ports = serial.tools.list_ports.comports()
        except Exception as e:
            logging.error(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())