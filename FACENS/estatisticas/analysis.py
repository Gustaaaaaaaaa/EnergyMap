import json 
import argparse 

def carregar_regioes(caminho_json):
    """Carrega e retorna a lista de regiões do arquivo JSON."""
    with open(caminho_json, 'r', encoding='utf-8') as f:
        # json.load lê JSON de um objeto de arquivo e retorna dict/list :contentReference[oaicite:4]{index=4}
        return json.load(f)

def exibir_valores(regioes):
    """Imprime nome, eficiência solar e eólica de cada região."""
    for reg in regioes:
        nome = reg.get('name', 'N/D')
        solar = reg.get('solar_efficiency', 'N/D')
        vento = reg.get('wind_efficiency', 'N/D')
        print(f"Região: {nome}")
        print(f"  ☀️ Energia Solar: {solar}")
        print(f"  🌬️ Energia Eólica: {vento}")
        print('-' * 40)

def main():
    parser = argparse.ArgumentParser(
        description="Exibe valores de energia solar e eólica de regions.json"
    )  # Cria parser de argumentos :contentReference[oaicite:5]{index=5}
    parser.add_argument(
        '--file', '-f',
        metavar='ARQUIVO',
        required=True,
        help='Caminho para regions.json'
    )  # Define argumento obrigatório :contentReference[oaicite:6]{index=6}

    args = parser.parse_args()  # Faz o parsing de sys.argv :contentReference[oaicite:7]{index=7}

    regioes = carregar_regioes(args.file)
    exibir_valores(regioes)

if __name__ == '__main__':
    main()
