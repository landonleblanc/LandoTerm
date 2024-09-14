import sys
import logging
import serial
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QLabel, QComboBox, QHBoxLayout

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
        self.terminal_output = QTextEdit(self)
        self.terminal_output.setReadOnly(True)
        self.input_line = QLineEdit(self)
        self.input_line.setDisabled(True)

        # Set layout
        main_layout = QVBoxLayout()
        port_layout = QHBoxLayout()
        port_layout.addWidget(self.port_label)
        port_layout.addWidget(self.port_dropdown)
        port_layout.addWidget(self.refresh_button)
        self.port_label.setFixedWidth(36)  # Set fixed width for port_label
        port_layout.setStretch(1, 3)  # Stretch for port_dropdown
        baud_layout = QHBoxLayout()
        baud_layout.addWidget(self.baudrate_label)
        baud_layout.addWidget(self.baudrate_dropdown)
        self.baudrate_dropdown.setCurrentIndex(2)
        self.baudrate_label.setFixedWidth(65)
        baud_layout.setStretch(1, 3)
        bar_layout = QHBoxLayout()
        bar_layout.addLayout(port_layout)
        bar_layout.addLayout(baud_layout)
        bar_layout.addWidget(self.connect_button)
        bar_layout.setStretch(0, 4)
        bar_layout.setStretch(1, 3)
        bar_layout.setStretch(2, 3)

        # Add the combined horizontal layout and output box to the main layout
        main_layout.addLayout(bar_layout)
        main_layout.addWidget(self.terminal_output)
        main_layout.addWidget(self.input_line)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.connect_button.clicked.connect(self.connect)
        self.refresh_button.clicked.connect(self.update_ports)
        self.input_line.returnPressed.connect(self.send_input)

    def send_input(self):
        user_input = self.input_line.text()
        if user_input:
            self.terminal_output.append(f"> {user_input}")
            self.s.send(user_input.encode())  # Send the input via self.s.send
            self.input_line.clear()  # Clear the input line after sending

    def disconnect(self):
        logging.info("Disconnecting")
        self.s.close()
        self.terminal_output.append(f'Disconnected from {self.s.port}')
        self.connect_button.setText("Connect")
        self.connect_button.clicked.disconnect()
        self.connect_button.clicked.connect(self.connect)
        self.input_line.setDisabled(True)
        self.port_dropdown.setDisabled(False)
        self.baudrate_dropdown.setDisabled(False)

    def connect(self):
        selected_port = self.port_dropdown.currentText()
        selected_baudrate = self.baudrate_dropdown.currentText()
        logging.info(f"Connecting to {selected_port} with baudrate {selected_baudrate}")
        self.s = serialCom(selected_port, int(selected_baudrate))
        self.connect_button.setText("Disconnect")
        self.connect_button.clicked.disconnect()
        self.connect_button.clicked.connect(self.disconnect)
        self.input_line.setDisabled(False)
        self.port_dropdown.setDisabled(True)
        self.baudrate_dropdown.setDisabled(True)
        try:
            self.s = serialCom(selected_port, int(selected_baudrate))
            error = self.s.open()
            if error:
                self.terminal_output.append(error)
                return
        except Exception as e:
            logging.error(e)
            return
        self.terminal_output.append(f'Connected to {selected_port} with baudrate {selected_baudrate}')

    def update_ports(self):
        try:
            ports = ['COM1', 'COM2', 'COM3', 'COM4', 'dev/ttyUSB0', 'dev/ttyUSB1']
            logging.info("Updating port list")
            logging.info(f'Found ports: {ports}')
            # self.ports = serial.tools.list_ports.comports()
            self.port_dropdown.clear()
            self.port_dropdown.addItems(ports)
        except Exception as e:
            logging.error(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())