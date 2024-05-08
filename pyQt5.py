
import sys
from PyQt5.QtWidgets import QApplication, QRadioButton, QWidget, QComboBox,QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QMainWindow, QTextEdit, QFileDialog

# SQLite veritabanı için kütüphane
import sqlite3

class GirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Ekranı")
        self.setGeometry(100, 100, 300, 200)

        self.kullanici_adi_label = QLabel("Kullanıcı Adı:")
        self.kullanici_adi_textbox = QLineEdit()
        self.sifre_label = QLabel("Şifre:")
        self.sifre_textbox = QLineEdit()
        self.sifre_textbox.setEchoMode(QLineEdit.Password)

        self.giris_button = QPushButton("Giriş Yap")
        self.kayit_button = QPushButton("Kayıt Ol")

        self.giris_button.clicked.connect(self.giris)
        self.kayit_button.clicked.connect(self.kayit)

        layout = QVBoxLayout()
        layout.addWidget(self.kullanici_adi_label)
        layout.addWidget(self.kullanici_adi_textbox)
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre_textbox)
        layout.addWidget(self.giris_button)
        layout.addWidget(self.kayit_button)

        self.setLayout(layout)

    def giris(self):
        kullanici_adi = self.kullanici_adi_textbox.text()
        sifre = self.sifre_textbox.text()

        # SQLite veritabanına bağlan
        conn = sqlite3.connect('kullanicilar.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi=? AND sifre=?", (kullanici_adi, sifre))
        user = cursor.fetchone()

        if user:
            self.menu_ekrani = MenuEkrani(kullanici_adi)
            self.menu_ekrani.show()
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre yanlış!")

        conn.close()

    def kayit(self):
        kullanici_adi = self.kullanici_adi_textbox.text()
        sifre = self.sifre_textbox.text()

        # SQLite veritabanına bağlan
        conn = sqlite3.connect('kullanicilar.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi=?", (kullanici_adi,))
        user = cursor.fetchone()

        if user:
            QMessageBox.warning(self, "Hata", "Kullanıcı zaten var!")
        else:
            cursor.execute("INSERT INTO kullanicilar (kullanici_adi, sifre) VALUES (?, ?)", (kullanici_adi, sifre))
            conn.commit()
            QMessageBox.information(self, "Başarılı", "Kullanıcı kaydedildi!")

        conn.close()

class MenuEkrani(QWidget):
    def __init__(self, kullanici_adi):
        super().__init__()
        self.setWindowTitle("Menü Ekranı")
        self.setGeometry(100, 100, 300, 200)
        
        self.kullanici_adi = kullanici_adi  # Kullanıcı adını kaydediyoruz

        self.karsilastir_button = QPushButton("Karşılaştır")
        self.islemler_button = QPushButton("İşlemler")
        self.cikis_button = QPushButton("Çıkış")

        self.karsilastir_button.clicked.connect(self.karsilastir_ac)
        self.islemler_button.clicked.connect(self.islemler_ac)
        self.cikis_button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.karsilastir_button)
        layout.addWidget(self.islemler_button)
        layout.addWidget(self.cikis_button)

        self.setLayout(layout)

    def karsilastir_ac(self):
        self.karsilastir_ekrani = KarsilastirEkrani(self.kullanici_adi)  # Kullanıcı adını KarsilastirEkrani sınıfına iletiyoruz
        self.karsilastir_ekrani.show()

    def islemler_ac(self):
        self.islemler_ekrani = IslemlerEkrani(self.kullanici_adi)
        self.islemler_ekrani.show()

class KarsilastirEkrani(QWidget):
    def __init__(self, kullanici_adi):
        super().__init__()
        self.setWindowTitle("Karşılaştır Ekranı")
        self.setGeometry(100, 100, 400, 300)
        self.kullanici_adi = kullanici_adi

        self.metin1_label = QLabel("Metin 1 Dosyası:")
        self.metin1_textbox = QLineEdit()
        self.metin1_browse_button = QPushButton("Dosya Seç")
        self.metin1_browse_button.clicked.connect(self.browse_metin1)

        self.metin2_label = QLabel("Metin 2 Dosyası:")
        self.metin2_textbox = QLineEdit()
        self.metin2_browse_button = QPushButton("Dosya Seç")
        self.metin2_browse_button.clicked.connect(self.browse_metin2)

        self.algoritma_combo = QComboBox()
        self.algoritma_combo.addItem("Jaccard Benzerliği")
        self.algoritma_combo.addItem("Levenshtein Benzerliği")

        self.karsilastir_button = QPushButton("Karşılaştır")
        self.karsilastir_button.clicked.connect(self.karsilastir)

        self.sonuc_label = QLabel("Karşılaştırma Sonucu:")
        self.sonuc_textbox = QTextEdit()
        self.sonuc_textbox.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.metin1_label)
        layout.addWidget(self.metin1_textbox)
        layout.addWidget(self.metin1_browse_button)
        layout.addWidget(self.metin2_label)
        layout.addWidget(self.metin2_textbox)
        layout.addWidget(self.metin2_browse_button)
        layout.addWidget(QLabel("Benzerlik Algoritması:"))
        layout.addWidget(self.algoritma_combo)
        layout.addWidget(self.karsilastir_button)
        layout.addWidget(self.sonuc_label)
        layout.addWidget(self.sonuc_textbox)

        self.setLayout(layout)

    def browse_metin1(self):
        dosya_adı, _ = QFileDialog.getOpenFileName(self, "Metin 1 Dosyasını Seç", "", "Metin Dosyaları (*.txt)")
        if dosya_adı:
            self.metin1_textbox.setText(dosya_adı)

    def browse_metin2(self):
        dosya_adı, _ = QFileDialog.getOpenFileName(self, "Metin 2 Dosyasını Seç", "", "Metin Dosyaları (*.txt)")
        if dosya_adı:
            self.metin2_textbox.setText(dosya_adı)

    def karsilastir(self):
        dosya1 = self.metin1_textbox.text()
        dosya2 = self.metin2_textbox.text()

        if not dosya1 or not dosya2:
            QMessageBox.warning(self, "Hata", "Lütfen iki metin dosyası seçin.")
            return

        # Dosyaları oku
        with open(dosya1, 'r', encoding='utf-8') as f:
            metin1 = f.read()
        with open(dosya2, 'r', encoding='utf-8') as f:
            metin2 = f.read()
        
        # Seçilen algoritmayı al
        secilen_algoritma = self.algoritma_combo.currentText()

        if secilen_algoritma == "Jaccard Benzerliği":
            benzerlik_skoru = self.calculate_jaccard_similarity(metin1, metin2)
        elif secilen_algoritma == "Levenshtein Benzerliği":
            benzerlik_skoru = self.calculate_levenshtein_similarity(metin1, metin2)

        # Sonucu ekrana yaz
        sonuc = "{} Benzerlik Sonucu: {:.2f}".format(secilen_algoritma, benzerlik_skoru)
        self.sonuc_textbox.setText(sonuc)

    def calculate_jaccard_similarity(self, text1, text2):
        words1 = set(text1.split())
        words2 = set(text2.split())

        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        jaccard_sim = intersection / union if union != 0 else 0

        return jaccard_sim

    def calculate_levenshtein_similarity(self, text1, text2):
        if len(text1) > len(text2):
            text1, text2 = text2, text1

        distances = range(len(text1) + 1)
        for index2, char2 in enumerate(text2):
            new_distances = [index2 + 1]
            for index1, char1 in enumerate(text1):
                if char1 == char2:
                    new_distances.append(distances[index1])
                else:
                    new_distances.append(1 + min((distances[index1], distances[index1 + 1], new_distances[-1])))
            distances = new_distances
        levenshtein_sim = 1 - (distances[-1] / max(len(text1), len(text2)))

        return levenshtein_sim






class IslemlerEkrani(QWidget):
    def __init__(self,kullanici_adi):
        super().__init__()
        self.setWindowTitle("İşlemler Ekranı")
        self.setGeometry(100, 100, 300, 200)
        self.kullanici_adi = kullanici_adi

        self.sifre_menu_button = QPushButton("Şifre Menüsü")
        self.sifre_menu_button.clicked.connect(self.sifre_menu_ac)

        layout = QVBoxLayout()
        layout.addWidget(self.sifre_menu_button)

        self.setLayout(layout)

    def sifre_menu_ac(self):
        self.sifre_menu_ekrani = SifreMenuEkrani(self.kullanici_adi)
        self.sifre_menu_ekrani.show()

class SifreMenuEkrani(QWidget):
    def __init__(self, kullanici_adi):
        super().__init__()
        self.setWindowTitle("Şifre Menüsü")
        self.setGeometry(100, 100, 300, 200)
        self.kullanici_adi = kullanici_adi

        self.sifre_degistir_button = QPushButton("Şifre Değiştir")
        self.sifre_degistir_button.clicked.connect(self.sifre_degistir_ac)

        layout = QVBoxLayout()
        layout.addWidget(self.sifre_degistir_button)

        self.setLayout(layout)

    def sifre_degistir_ac(self):
        self.sifre_degistir_ekrani = SifreDegistirEkrani(self.kullanici_adi)
        self.sifre_degistir_ekrani.show()


class SifreDegistirEkrani(QWidget):
    def __init__(self, kullanici_adi):
        super().__init__()
        self.setWindowTitle("Şifre Değiştir Ekranı")
        self.setGeometry(100, 100, 300, 200)

        self.kullanici_adi = kullanici_adi  # Kullanıcı adını kaydediyoruz

        self.eski_sifre_label = QLabel("Eski Şifre:")
        self.eski_sifre_textbox = QLineEdit()
        self.yeni_sifre_label = QLabel("Yeni Şifre:")
        self.yeni_sifre_textbox = QLineEdit()
        self.yeni_sifre_textbox.setEchoMode(QLineEdit.Password)
        self.yeni_sifre_tekrar_label = QLabel("Yeni Şifre (Tekrar):")
        self.yeni_sifre_tekrar_textbox = QLineEdit()
        self.yeni_sifre_tekrar_textbox.setEchoMode(QLineEdit.Password)

        self.kaydet_button = QPushButton("Kaydet")
        self.kaydet_button.clicked.connect(self.sifre_degistir)

        layout = QVBoxLayout()
        layout.addWidget(self.eski_sifre_label)
        layout.addWidget(self.eski_sifre_textbox)
        layout.addWidget(self.yeni_sifre_label)
        layout.addWidget(self.yeni_sifre_textbox)
        layout.addWidget(self.yeni_sifre_tekrar_label)
        layout.addWidget(self.yeni_sifre_tekrar_textbox)
        layout.addWidget(self.kaydet_button)

        self.setLayout(layout)

    def sifre_degistir(self):
        eski_sifre = self.eski_sifre_textbox.text()
        yeni_sifre = self.yeni_sifre_textbox.text()
        yeni_sifre_tekrar = self.yeni_sifre_tekrar_textbox.text()

        # Eski şifrenin doğruluğunu kontrol et
        conn = sqlite3.connect('kullanicilar.db')
        cursor = conn.cursor()
        cursor.execute("SELECT sifre FROM kullanicilar WHERE kullanici_adi=?", (self.kullanici_adi,))
        kayit = cursor.fetchone()

        if kayit is None:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı bulunamadı!")
            return

        kayitli_sifre = kayit[0]

        if eski_sifre != kayitli_sifre:
            QMessageBox.warning(self, "Hata", "Eski şifre yanlış!")
            return

        # Yeni şifrelerin eşleştiğini kontrol et
        if yeni_sifre != yeni_sifre_tekrar:
            QMessageBox.warning(self, "Hata", "Yeni şifreler eşleşmiyor!")
            return

        # Veritabanında şifreyi güncelle
        cursor.execute("UPDATE kullanicilar SET sifre=? WHERE kullanici_adi=?", (yeni_sifre, self.kullanici_adi))
        conn.commit()
        QMessageBox.information(self, "Bilgi", "Şifre başarıyla değiştirildi.")
        conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    giris_ekrani = GirisEkrani()
    giris_ekrani.show()
    sys.exit(app.exec_())