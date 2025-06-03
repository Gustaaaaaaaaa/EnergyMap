import requests
import folium
import argparse

def get_current_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&solar_radiation=true"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    clima = data.get("current_weather", {})
    rad_solar = data.get("solar_radiation", {}).get("value", "Não disponível")  # Radiação solar em W/m²
    umidade = clima.get("humidity", "Não disponível")
    pressao = clima.get("pressure", "Não disponível")
    
    return {
        "temperatura": clima.get("temperature", "Não disponível"),
        "vento": clima.get("windspeed", "Não disponível"),
        "hora": clima.get("time", "Não disponível"),
        "rad_solar": rad_solar,
        "direcao_vento": clima.get("winddirection", "Não disponível"),
        "umidade": umidade,
        "pressao": pressao
    }

def get_elevation(lat, lon):
    url = f"https://api.opentopodata.org/v1/srtm90m?locations={lat},{lon}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()['results'][0]['elevation']

def calcular_potencial_eolico(velocidade, raio_rotor, densidade_ar=1.225):
    area = 3.1416 * raio_rotor ** 2
    potencia = 0.5 * densidade_ar * area * velocidade ** 3
    return potencia / 1000  # kW

def gerar_mapa(lat, lon, potencia, vento, rad_solar, temperatura, saida):
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker(
        [lat, lon],
        popup=f"🌬️ Vento: {vento} m/s\n🔋 Potência eólica: {potencia:.2f} kW\n🌡️ Temperatura: {temperatura}°C\n☀️ Radiação solar: {rad_solar} W/m²",
        icon=folium.Icon(color='blue')
    ).add_to(m)
    m.save(saida)
    print(f"✅ Mapa salvo como: {saida}")

def main():
    parser = argparse.ArgumentParser(description="Potencial Eólico Atual (Open-Meteo)")
    parser.add_argument("--lat", type=float, required=True, help="Latitude")
    parser.add_argument("--lon", type=float, required=True, help="Longitude")
    parser.add_argument("--rotor-radius", type=float, default=2.5, help="Raio do rotor (m)")
    parser.add_argument("--output", type=str, default="mapa_potencial_eolico.html", help="Arquivo HTML de saída")
    args = parser.parse_args()

    clima = get_current_weather(args.lat, args.lon)
    elevacao = get_elevation(args.lat, args.lon)
    potencia = calcular_potencial_eolico(float(clima['vento']), args.rotor_radius) if clima['vento'] != "Não disponível" else "Não disponível"

    print(f"""
📍 Local: ({args.lat}, {args.lon})
⛰️ Elevação: {elevacao} m
🕒 Hora da medição: {clima['hora']}
🌬️ Velocidade do vento: {clima['vento']} m/s
🌀 Direção do vento: {clima['direcao_vento']}° (norte = 0°)
🌡️ Temperatura: {clima['temperatura']}°C
☀️ Radiação solar: {clima['rad_solar']} W/m²
💧 Umidade relativa do ar: {clima['umidade']}%
🌬️ Pressão atmosférica: {clima['pressao']} hPa
🔋 Potência eólica estimada: {potencia}
""")

    gerar_mapa(args.lat, args.lon, potencia, clima['vento'], clima['rad_solar'], clima['temperatura'], args.output)

if __name__ == "__main__":
    main()
