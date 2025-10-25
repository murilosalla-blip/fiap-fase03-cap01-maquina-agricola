import re, csv, os, datetime as dt

LOG_IN = "Log Wokwi.txt"          # nome do log esperado
BASE_OUT = "fase2_sensores"       # prefixo do CSV de saída
OUT_DIR = "."                     # saída = mesma pasta do script/log

# regex alinhada ao formato do log
pat = re.compile(
    r"Umidade:\s*([-\d.]+)\s*%\s*"
    r"Temp:\s*([-\d.]+)\s*C\s*"
    r"LDR:\s*(\d+)\s*"
    r"pH\(sim\):\s*([-\d.]+)\s*"
    r"pH_OK:\s*(\w+)\s*"
    r"N\(OK\):\s*(\d+)\s*P\(OK\):\s*(\d+)\s*K\(OK\):\s*(\d+)\s*"
    r"Faltando:\s*(\d+)\s*"
    r"ON:\s*([-\d.]+)\s*OFF:\s*([-\d.]+)\s*"
    r"Rain\(mm\):\s*([-\d.]+)\s*POP\(%\):\s*(\d+).*?"
    r"Irrigacao:\s*(\w+)",
    re.S
)

def unique_csv_name(base_dir, base_name):
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    candidate = f"{base_name}_{ts}.csv"
    path = os.path.join(base_dir, candidate)
    if not os.path.exists(path):
        return path
    i = 2
    while True:
        candidate = f"{base_name}_{ts}_v{i}.csv"
        path = os.path.join(base_dir, candidate)
        if not os.path.exists(path):
            return path
        i += 1

if not os.path.exists(LOG_IN):
    raise FileNotFoundError(f'Arquivo não encontrado: "{LOG_IN}". Coloque este script na mesma pasta do log.')

with open(LOG_IN, "r", encoding="utf-8") as f:
    text = f.read()

rows = []
for m in pat.finditer(text):
    rows.append({
        "row_id": len(rows) + 1,
        "umidade_pct": float(m.group(1)),
        "temp_c": float(m.group(2)),
        "ldr": int(m.group(3)),
        "ph_sim": float(m.group(4)),
        "ph_ok": m.group(5),
        "n_ok": int(m.group(6)),
        "p_ok": int(m.group(7)),
        "k_ok": int(m.group(8)),
        "faltando": int(m.group(9)),
        "limiar_on": float(m.group(10)),
        "limiar_off": float(m.group(11)),
        "rain_mm": float(m.group(12)),
        "pop_pct": int(m.group(13)),
        "irrigacao": m.group(14),
        "source_file": LOG_IN
    })

if not rows:
    raise ValueError("Nenhum dado compatível encontrado no log. Verifique o conteúdo.")

out_path = unique_csv_name(OUT_DIR, BASE_OUT)
fieldnames = list(rows[0].keys())

with open(out_path, "x", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)

print("="*60)
print("CSV gerado com sucesso!")
print("Arquivo salvo em:", os.path.abspath(out_path))
print("Total de linhas exportadas:", len(rows))
print("="*60)
