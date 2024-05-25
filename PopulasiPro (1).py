import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QSizePolicy, QStackedWidget
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ProyeksiPendudukApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Populasi Pro')
        self.setMinimumSize(1200, 600)  # Set minimum window size
        self.setMaximumSize(1200, 600)  # Set maximum window size

        # Disable minimize button
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)

        self.stacked_widget = QStackedWidget()

        self.menu_widget = QWidget()
        menu_layout = QVBoxLayout()
        menu_layout.addStretch()

        start_button = QPushButton("Mulai")
        start_button.clicked.connect(self.show_input_menu)
        start_button.setStyleSheet("QPushButton {"
                                   "background-color: #4CAF50;"
                                   "border: none;"
                                   "color: white;"
                                   "padding: 15px 32px;"
                                   "text-align: center;"
                                   "text-decoration: none;"
                                   "display: inline-block;"
                                   "font-size: 16px;"
                                   "margin: 4px 2px;"
                                   "cursor: pointer;"
                                   "}"
                                   "QPushButton::hover {"
                                   "background-color: #45a049;"
                                   "}"
                                   "QPushButton::pressed {"
                                   "background-color: #3e8e41;"
                                   "}"
                                   "QPushButton::focus {"
                                   "outline: none;"
                                   "}"
                                   )

        start_button_text = QLabel("Populasi Pro")
        start_button_text.setAlignment(Qt.AlignCenter)
        start_button_text.setStyleSheet("font-family: Poppins; font-weight: bold; color: #4CAF50; font-size: 40px;")

        menu_layout.addWidget(start_button_text)
        menu_layout.addWidget(start_button)
        menu_layout.addStretch()

        self.menu_widget.setLayout(menu_layout)
        self.stacked_widget.addWidget(self.menu_widget)

        self.input_widget = QWidget()
        input_layout = QVBoxLayout()

        label1 = QLabel("Jumlah penduduk pada tahun yang akan dijadikan titik awal proyeksi:")
        self.input1 = QLineEdit()
        input_layout.addWidget(label1)
        input_layout.addWidget(self.input1)

        label2 = QLabel("Selang waktu proyeksi (dalam tahun):")
        self.input2 = QLineEdit()
        input_layout.addWidget(label2)
        input_layout.addWidget(self.input2)

        label3 = QLabel("Luas wilayah daerah (dalam hektar):")
        self.input3 = QLineEdit()
        input_layout.addWidget(label3)
        input_layout.addWidget(self.input3)

        input_layout.addStretch()

        self.button = QPushButton("Hitung Proyeksi")
        self.button.clicked.connect(self.hitung_proyeksi)
        self.button.setStyleSheet("QPushButton {"
                                   "background-color: #4CAF50;"
                                   "border: none;"
                                   "color: white;"
                                   "padding: 15px 32px;"
                                   "text-align: center;"
                                   "text-decoration: none;"
                                   "display: inline-block;"
                                   "font-size: 16px;"
                                   "margin: 4px 2px;"
                                   "cursor: pointer;"
                                   "}"
                                   "QPushButton::hover {"
                                   "background-color: #45a049;"
                                   "}"
                                   "QPushButton::pressed {"
                                   "background-color: #3e8e41;"
                                   "}"
                                   "QPushButton::focus {"
                                   "outline: none;"
                                   "}"
                                   )
        input_layout.addWidget(self.button)

        self.input_widget.setLayout(input_layout)
        self.stacked_widget.addWidget(self.input_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)

        # Create a QHBoxLayout to hold FigureCanvas and QTextEdit
        hbox = QHBoxLayout()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumSize(600, 300)  # Set minimum canvas size
        hbox.addWidget(self.canvas)

        self.output = QTextEdit()
        self.output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set size policy to Expanding
        hbox.addWidget(self.output)

        layout.addLayout(hbox)

        # Tambahkan tombol Hitung Ulang di bagian bawah output
        self.recalculate_button = QPushButton("Hitung Ulang")
        self.recalculate_button.clicked.connect(self.show_input_menu)  # Panggil fungsi show_input_menu ketika tombol ditekan
        self.recalculate_button.hide()  # Sembunyikan tombol saat aplikasi dimulai
        self.recalculate_button.setStyleSheet("QPushButton {"
                                   "background-color: #f44336;"
                                   "border: none;"
                                   "color: white;"
                                   "padding: 15px 32px;"
                                   "text-align: center;"
                                   "text-decoration: none;"
                                   "display: inline-block;"
                                   "font-size: 16px;"
                                   "margin: 4px 2px;"
                                   "cursor: pointer;"
                                   "}"
                                   "QPushButton::hover {"
                                   "background-color: #c0392b;"
                                   "}"
                                   "QPushButton::pressed {"
                                   "background-color: #992d22;"
                                   "}"
                                   "QPushButton::focus {"
                                   "outline: none;"
                                   "}"
                                   )
        layout.addWidget(self.recalculate_button)  # Tambahkan tombol ke layout

        self.setLayout(layout)

    def show_input_menu(self):
        # Bersihkan output sebelum menampilkan kembali menu input
        self.reset_output()

        if self.stacked_widget.currentWidget() == self.input_widget:  # Jika saat ini sedang menampilkan input_widget
            self.stacked_widget.setCurrentWidget(self.menu_widget)  # Tampilkan menu_widget
            self.recalculate_button.hide()  # Sembunyikan tombol "Hitung Ulang"
        else:
            self.stacked_widget.setCurrentWidget(self.input_widget)  # Tampilkan kembali input_widget

    def hitung_proyeksi(self):
        # Bersihkan output dan grafik sebelum menghitung proyeksi baru
        self.reset_output()

        try:
            # Lakukan perhitungan proyeksi
            Po = float(self.input1.text())
            n = int(self.input2.text())
            luas_wilayah = float(self.input3.text())

            r = self.hitung_r(Po, n)

            populations = [Po]
            projection_text = "Hasil proyeksi penduduk:\n"
            for year in range(1, n + 1):
                Pn = self.proyeksi_penduduk(Po, r, year)
                populations.append(Pn)
                projection_text += f"Proyeksi penduduk pada tahun ke-{year}: {Pn:.0f}\n"

            kepadatan = self.hitung_kepadatan_penduduk(populations[-1], luas_wilayah)
            projection_text += f"Kepadatan penduduk pada tahun ke-{n}: {kepadatan:.2f} penduduk/hektar\n\n"

            advice_text = self.generate_advice(kepadatan)
            projection_text += advice_text

            self.output.setText(projection_text)
            self.plot_population_projections(range(n + 1), populations, advice_text)

            # Hide input widget after displaying the output
            self.recalculate_button.show()  # Tampilkan tombol "Hitung Ulang"

        except ValueError:
            # Tangani jika terjadi kesalahan dalam konversi tipe data
            self.output.setText("Masukkan yang Anda berikan tidak valid. Pastikan Anda memasukkan angka yang valid.")
            self.recalculate_button.hide()

    def reset_output(self):
        # Membersihkan teks output
        self.output.clear()
        # Membersihkan grafik
        self.figure.clear()
        # Menggambar kembali canvas kosong
        self.canvas.draw()

    def proyeksi_penduduk(self, Po, r, n):
        Pn = Po * (1 + r) ** n
        return Pn

    def hitung_kepadatan_penduduk(self, Pn, luas_wilayah):
        kepadatan = Pn / luas_wilayah
        return kepadatan

    def hitung_r(self, Po, n):
        Pn = Po * 2
        r = (Pn / Po) ** (1 / n) - 1
        return r

    def generate_advice(self, kepadatan):
        advice = "Saran:\n"
        if kepadatan > 400:
            advice += "Analisa: Kepadatan penduduk sangat tinggi dalam wilayah ini.\n"
            advice += "Solusi: Perlunya dilakukan perencanaan pembangunan yang berkelanjutan dan pembaruan infrastruktur yang mampu menampung pertumbuhan penduduk yang cepat."
        elif 201 <= kepadatan <= 400:
            advice += "Analisa: Kepadatan penduduk tinggi dalam wilayah ini.\n"
            advice += "Solusi: Perlu ditingkatkan lagi pelayanan dan infrastruktur publik untuk mendukung kebutuhan penduduk yang tinggi."
        elif 151 <= kepadatan <= 200:
            advice += "Analisa: Kepadatan penduduk sedang dalam wilayah ini.\n"
            advice += "Solusi: Perlu dilakukan pemantauan dan perencanaan perkembangan wilayah secara berkelanjutan untuk menjaga keseimbangan antara pertumbuhan penduduk dan ketersediaan fasilitas umum."
        else:
            advice += "Analisa: Kepadatan penduduk rendah dalam wilayah ini.\n"
            advice += "Solusi: Diperlukan upaya untuk meningkatkan daya tarik dan pelayanan wilayah agar dapat menarik lebih banyak penduduk dan mendorong pertumbuhan ekonomi lokal."
        return advice

    def plot_population_projections(self, years, populations, advice_text):
        ax = self.figure.add_subplot(111)
        ax.plot(years, populations, marker='o')
        ax.set_xlabel('Tahun')
        ax.set_ylabel('Jumlah Penduduk')
        ax.set_title('Grafik Proyeksi Pertumbuhan Penduduk')
        ax.grid(True)
        ax.text(0.5, 0.5, advice_text, ha='center', va='center', wrap=True, bbox=dict(facecolor='white', alpha=0.5))
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProyeksiPendudukApp()
    ex.show()
    sys.exit(app.exec_())
