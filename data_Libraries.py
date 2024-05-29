import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Rastgele koordinatları üretme
def rastgeleKordinat(k):
    kordinatlar = []
    for _ in range(k):
        x = np.random.randint(0, 1000)
        y = np.random.randint(0, 1000)
        kordinatlar.append((x, y))
    return kordinatlar

# Koordinatları Excel dosyasına kaydetme
def kaydet_excel(kordinatlar, filename):
    df = pd.DataFrame(kordinatlar, columns=['X', 'Y'])
    df.to_excel(filename, index=False)

# Excel dosyasından koordinatları okuma
def oku_excel(filename):
    df = pd.read_excel(filename)
    return df.values.tolist()

# Koordinatları grafikte görselleştirme
def kordinatlariGorsellestir(kordinatlar):
    plt.figure(figsize=(10, 10))
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
    plt.show()

def main():
    # Koordinatları üretme ve Excel'e kaydetme
    kordinatlar = rastgeleKordinat(1000)
    kaydet_excel(kordinatlar, 'koordinatlar.xlsx')

    # Excel'den koordinatları okuma
    excel_koordinatlari = oku_excel('koordinatlar.xlsx')

    # Koordinatları görselleştirme
    kordinatlariGorsellestir(excel_koordinatlari)

main()
