import plotly.graph_objects as go
import webbrowser

# Dane w formacie "waga x powtórzenia", podane jako jeden string dla obu linii
daneBench = "105x5@8, 100x5@8, 110x5@8, 115x4@9, 120x4@9, 115x4@9, 120x3@9, 120x3@9, 120x4@9, 120x4@10, 105x3@7, 107.5x3@7, 112.5x3@7, 115x3@9, 120x3@9"
daneSquat = "160x5@8, 160x5@8, 170x5@8, 180x3@9, 200x3@9, 205x3@9, 175x3@7, 205x3@8, 215x3@9, 210x3@9, 220x3@9, 225x3@9, 230x3@9, 235x3@9, 240x3@9"
daneDeadlift = "190x5@8, 200x4@10, 207.5x5@8, 240x3@9, 250x3@10, 255x1@10, 210x1@9, 220x3@9, 240x3@9, 235x3@9, 240x3@8, 245x3@9, 250x3@9, 255x3@9, 260x3@9"


#danme do tesu

#daneBench = "100x3@8, 100x5@9"
#daneSquat = "200x3@8, 200x5@9"
#daneDeadlift = "250x3@7, 250x3@6"

# Funkcja parsująca dane
def parsuj_dane(dane):
    dane_lista = dane.split(',')  # Rozdzielenie po przecinku
    weight = []
    reps = []
    rpe = []
    for item in dane_lista:
        waga_powt_rpe = item.strip().split('x')  # Rozdzielenie na waga i powtórzenia, usunięcie spacji
        powt_rpe = waga_powt_rpe[1].split('@')
        weight.append(float(waga_powt_rpe[0]))  # Zamiana na liczb
        reps.append(int(powt_rpe[0]))  # Powtórzenia jako liczba całkowita
        rpe.append(float(powt_rpe[1]))
    return weight, reps, rpe

# Parsowanie danych dla obu linii
weight1, reps1, rpe1 = parsuj_dane(daneBench)
weight2, reps2, rpe2 = parsuj_dane(daneSquat)
weight3, reps3, rpe3 = parsuj_dane(daneDeadlift)

# Lista wyników dla pierwszej i drugiej linii
wyniki1 = [(w * (r+10-rpe) * 0.0333 + w) for w, r, rpe in zip(weight1, reps1, rpe1)]
wyniki2 = [(w * (r+10-rpe) * 0.0333 + w) for w, r, rpe in zip(weight2, reps2, rpe2)]
wyniki3 = [(w * (r+10-rpe) * 0.0333 + w) for w, r, rpe in zip(weight3, reps3, rpe3)]


#total
total = [b + s + d for b, s, d in zip(wyniki1, wyniki2, wyniki3)]

# Lista liczb naturalnych na osi X (od 1 do liczby wyników)
liczby_naturalne = list(range(1, len(wyniki1) + 1))

# Tworzenie wykresu
fig = go.Figure()

# Dodanie danych dla pierwszej linii
fig.add_trace(go.Scatter(x=liczby_naturalne, y=wyniki1, mode='lines+markers', name='Bench', line=dict(color='blue')))

# Dodanie danych dla drugiej linii
fig.add_trace(go.Scatter(x=liczby_naturalne, y=wyniki2, mode='lines+markers', name='Squat', line=dict(color='red')))

# Dodanie danych dla 3 lini

fig.add_trace(go.Scatter(x=liczby_naturalne, y=wyniki3, mode='lines+markers', name='Deadlift', line=dict(color='green')))

# Dodanie danych dla sumy Bench + Squat + Deadlift
fig.add_trace(go.Scatter(x=liczby_naturalne, y=total, mode='lines+markers', name='Total', line=dict(color='yellow')))

# Dodanie poziomej linii na poziomie 700 kg jako celu
fig.add_shape(
    type="line",
    x0=1, x1=max(liczby_naturalne),  # Od początku do końca osi X
    y0=700, y1=700,  # Poziom Y = 700 kg
    line=dict(color="gold", width=3, dash="dot"),  # Czerwona linia przerywana
    name="Cel 700 kg"
)

# Dodanie tytułów osi i tytułu wykresu
fig.update_layout(
    title="Porównanie dwóch serii danych",
    xaxis_title="Czas",
    xaxis=dict(
        tickmode='linear',
        dtick=1
    ),
    yaxis_title="OneRepMax (kg)",
    yaxis_range=[0, 750],  # Zakres osi Y
    yaxis=dict(
        tickmode='linear',
        dtick=20  # Oznaczenia co 5 kg na osi Y
    ),
    width=1920,  # Szerokość wykresu
    height=1080,  # Wysokość wykresu
    template="plotly_dark"  # Ciemny motyw, opcjonalnie
)

# Zapis wykresu w pliku HTML
filename = "wykres.html"
fig.write_html(filename)

# Automatyczne otwarcie pliku w domyślnej przeglądarce
webbrowser.open(filename)
