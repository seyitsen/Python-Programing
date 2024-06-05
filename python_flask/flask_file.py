from flask import Flask, render_template, send_file
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

flask_file = Flask(__name__)

# Rastgele koordinatları üretme
def rastgeleKordinat(k):
    kordinatlar = []
    for _ in range(k):
        x = np.random.randint(0, 1000)
        y = np.random.randint(0, 1000)
        kordinatlar.append((x, y))
    return kordinatlar

# Koordinatları grafikte görselleştirme
def kordinatlariGorsellestir(kordinatlar):
    plt.figure(figsize=(5, 5))  # Görsel boyutunu küçültme
    plt.grid(True)

    # Her ızgara grubuna farklı bir renk atama
    num_grids = 10
    color_palette = plt.cm.viridis(np.linspace(0, 1, num_grids))

    for x, y in kordinatlar:
        # Hangi ızgara grubunda olduğunu bulma
        grid_x = x // 100
        grid_y = y // 100
        grid_index = grid_x * 10 + grid_y
        
        # İlgili ızgara grubuna ait renkle noktayı görselleştirme
        plt.scatter(x, y, color=color_palette[grid_index % num_grids])

    plt.xlabel('X Koordinatı')
    plt.ylabel('Y Koordinatı')
    plt.title('Koordinatlar')

    # Görseli bellek tamponuna kaydetme
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img

@flask_file.route('/')
def index():
    return render_template('index.html')

@flask_file.route('/generate')
def generate():
    # Yeni rastgele noktalar üretme
    kordinatlar = rastgeleKordinat(1000)
    img = kordinatlariGorsellestir(kordinatlar)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    flask_file.run(debug=True)




