import py_dss_interface
import pandas as pd
import plotly.express as px
from tqdm import tqdm
import time


def inspecionar_cargas_partindo_secundario_trafos(dss):
    # Log inicial
    start_time = time.time()
    print(f"\n🚀 Iniciando inspeção em {time.strftime('%H:%M:%S')}")

    # 1. Filtrar transformadores com 2 barramentos
    print("\n🔍 Listando transformadores...")
    dss.transformers.first()
    transformers = []
    with tqdm(desc="Coletando transformadores", unit=" trafo") as pbar:
        while True:
            transformers.append(dss.transformers.name)
            pbar.update(1)
            if not dss.transformers.next():
                break

    # 2. Filtrar transformadores válidos
    print("\n⚙️ Filtrando transformadores de 2 barramentos...")
    trafos_2_barramentos = []
    for trafo in tqdm(transformers, desc="Filtrando trafos", unit=" trafo"):
        dss.transformers.name = trafo
        buses = dss.cktelement.bus_names
        if len(buses) == 2:
            trafos_2_barramentos.append(trafo)

    resultados = {}

    # 3. Processar cada transformador
    print(f"\n🔧 Iniciando análise para {len(trafos_2_barramentos)} transformadores:")
    for trafo in tqdm(trafos_2_barramentos, desc="Transformadores", unit=" trafo"):
        trafo_start = time.time()
        dss.transformers.name = trafo

        # Obter barramento secundário
        buses = dss.cktelement.bus_names
        barramento_secundario = buses[1]

        # Configurar BFS
        fila = [barramento_secundario]
        visitados = set()
        cargas_por_barramento = {}

        # Log de progresso para BFS
        print(f"\n   🔄 Transformador {trafo}: Iniciando BFS em {barramento_secundario}")
        with tqdm(desc="Barramentos processados", unit=" bus", leave=False) as bfs_pbar:
            while fila:
                barramento_atual = fila.pop(0)
                if barramento_atual in visitados:
                    continue
                visitados.add(barramento_atual)

                # Verificar cargas
                dss.circuit.set_active_bus(barramento_atual)
                cargas = dss.bus.load_list

                # Agrupamento inteligente de cargas
                cargas_agrupadas = {}
                sufixos = ("_M2UB", "_M3UB", "_MedUB")

                for carga in cargas:
                    # Remove sufixos específicos e nós
                    nome_limpo = carga.split('.')[0]  # Remove números de nós

                    # Remove sufixos de tipo de carga
                    for sufixo in sufixos:
                        if nome_limpo.endswith(sufixo):
                            nome_base = nome_limpo[:-len(sufixo)]
                            break
                        else:
                            nome_base = nome_limpo

                    # Adiciona ao dicionário
                    if nome_base not in cargas_agrupadas:
                        cargas_agrupadas[nome_base] = []
                    cargas_agrupadas[nome_base].append(carga)

                # Armazenar dados detalhados
                cargas_por_barramento[barramento_atual] = {
                    'cargas_brutas': cargas,
                    'cargas_agrupadas': cargas_agrupadas
                }

                # Encontrar linhas conectadas
                linhas_conectadas = []
                for linha in tqdm(dss.lines.names, desc="Verificando linhas", unit=" linha", leave=False):
                    dss.lines.name = linha
                    barramentos_linha = dss.cktelement.bus_names
                    barramento1_linha = barramentos_linha[0]
                    barramento2_linha = barramentos_linha[1]

                    if barramento_atual in (barramento1_linha, barramento2_linha):
                        linhas_conectadas.append(linha)

                # Adicionar barramentos conectados
                for linha in linhas_conectadas:
                    dss.lines.name = linha
                    barramentos_linha = dss.cktelement.bus_names
                    barramento1_linha = barramentos_linha[0]
                    barramento2_linha = barramentos_linha[1]
                    outro_barramento = barramento2_linha if barramento_atual == barramento1_linha else barramento1_linha

                    if outro_barramento not in visitados and outro_barramento not in fila:
                        fila.append(outro_barramento)

                # Atualizar progresso
                bfs_pbar.update(1)
                bfs_pbar.set_postfix({
                    "Fila": len(fila),
                    "Visitados": len(visitados),
                    "Último Barramento": barramento_atual[:20] + "..."
                })

        resultados[trafo] = cargas_por_barramento
        print(f"   ✅ Transformador {trafo} concluído em {time.time() - trafo_start:.1f}s")

    # Log final
    total_time = time.time() - start_time
    print(f"\n🎉 Análise concluída em {total_time:.2f} segundos")
    print(f"📊 Total de transformadores analisados: {len(resultados)}")
    print(f"🏙️  Total de barramentos inspecionados: {sum(len(v) for v in resultados.values())}")
    return resultados


# Configuração e execução
dss_file = r"C:\py-dss-interface_pg\pythonProject\IC\Master.dss"
dss = py_dss_interface.DSS()
dss.text(f"compile [{dss_file}]")
dss.text("Set Mode=Snap")
dss.text("Solve")

resultados = inspecionar_cargas_partindo_secundario_trafos(dss)

# Exibição detalhada dos resultados
# ... (código anterior mantido)

# Exibição detalhada dos resultados
for trafo, barramentos in resultados.items():
    print(f"\n{'=' * 50}\nTransformador: {trafo}\n{'=' * 50}")

    total_brutas = 0
    total_liquidas = 0

    for barramento, data in barramentos.items():
        # Contagem para este barramento
        brutas_barramento = len(data['cargas_brutas'])
        liquidas_barramento = len(data['cargas_agrupadas'])

        # Acumula totais
        total_brutas += brutas_barramento
        total_liquidas += liquidas_barramento

        # Exibe detalhes
        print(f"\n  ┌─ Barramento: {barramento}")
        print(f"  ├─ Cargas brutas (individuais): {brutas_barramento}")
        print(f"  ├─ Cargas líquidas (agrupadas): {liquidas_barramento}")
        print(f"  └─ Detalhes dos grupos:")
        for grupo, cargas in data['cargas_agrupadas'].items():
            print(f"     ├─ {grupo}: {len(cargas)} cargas")
            print(f"     │   → Exemplos: {cargas[:2]}...")  # Mostra até 2 cargas por grupo

    # Exibe totais do transformador
    print(f"\n  ► RESUMO DO TRANSFORMADOR:")
    print(f"  ├─ Total de cargas brutas (todas): {total_brutas}")
    print(f"  └─ Total de cargas líquidas (grupos únicos): {total_liquidas}")