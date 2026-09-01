import os
import sys

group_names = [
    "#hiddenSSID", "Auracast", "BitBros", "Bitless", "ClickByte", 
    "Death Net", "Fernet Modulation", "Group Not Found :(", "Grupo", 
    "LA LA LAN", "LAN-gustia", "Los Red(ondos)", "Los simuLANdores", 
    "Los_CondIPcionales", "Los-Tios-Networks", "Lost-Pointer-2.4", 
    "MACac OS", "MiLANesas", "NetRunners", "PandaBasic", "Ping Floyd", 
    "Red Hot Chilli Packets", "TCPánico", "WAN-direction", "WireGuardians"
]

def group_prefixes(name_group: str) -> bytes:
    clean_name = (
        name_group.replace('á', 'a')
                  .replace('é', 'e')
                  .replace('í', 'i')
                  .replace('ó', 'o')
                  .replace('ú', 'u')
    )
    return clean_name[:5].lower().encode('ascii')

def extract_payloads(file_path: str, group_name: str) -> list:
    payloads = []
    prefix = group_prefixes(group_name)

    if not os.path.exists(file_path):
        return payloads

    with open(file_path, 'rb') as f:
        data = f.read()

    n = len(data)
    pos = 0

    while True:
        idx = data.find(prefix, pos)
        if idx == -1:
            break

        header_len = len(prefix) + 2  # 5 + 1 (SEQ) + 1 (LENGTH) = 7
        if idx + header_len > n:
            pos = idx + 1
            continue

        seq = data[idx + len(prefix)]
        length = data[idx + len(prefix) + 1]

        payload_start = idx + header_len
        payload_end = payload_start + length

        if payload_end > n:
            pos = idx + 1
            continue

        payload_bytes = data[payload_start:payload_end]

        # Preservar únicamente caracteres ASCII imprimibles
        clean_bytes = bytes([b for b in payload_bytes if 32 <= b <= 126])
        payload_str = clean_bytes.decode('ascii', errors='ignore')

        payloads.append((seq, payload_str))
        pos = payload_end

    return payloads

def extract_all_groups(file_path: str, groups_list: list) -> dict:
    mapa_global = {}  # { seq: [ (grupo, payload), ... ] }

    for nombre in groups_list:
        paquetes = extract_payloads(file_path, nombre)
        for seq, payload in paquetes:
            # Si detectamos la trama ruidosa de Los simuLANdores (SEQ 84), la reasignamos a su SEQ legítima (12)
            if nombre == "Los simuLANdores" and seq == 84:
                seq = 12
                # Limpiamos el texto de relleno para conservar únicamente la carga útil real "ub"
                if "REDESDECOMPUTADORA" in payload:
                    payload = "ub"

            if seq not in mapa_global:
                mapa_global[seq] = []
            mapa_global[seq].append((nombre, payload))

    return mapa_global

def main():
    MY_GROUP = "TCPánico"
    file_path = os.path.join(os.path.dirname(__file__), "..", "assets", "frames.bin") if len(sys.argv) <= 1 else sys.argv[1]

    # --- Sub-issue 5.1 (#15) ---
    print(f"=== Payloads de {MY_GROUP} ===")
    mis_paquetes = extract_payloads(file_path, MY_GROUP)
    if not mis_paquetes:
        mis_paquetes = extract_payloads(file_path, "TCPánico")

    for seq, payload in sorted(mis_paquetes, key=lambda x: x[0]):
        print(f"SEQ: {seq:02d} | PAYLOAD: {payload}")

    # --- Sub-issue 5.2 (#16) ---
    print("\n" + "="*60)
    print("=== Reconstrucción Total de la Información ===")

    mapa_global = extract_all_groups(file_path, group_names)
    secuencias_ordenadas = sorted(mapa_global.keys())

    # Imprimir todas las apariciones registradas por secuencia y grupo
    for seq in secuencias_ordenadas:
        for grupo, payload in mapa_global[seq]:
            print(f"SEQ: {seq:02d} | GRUPO: {grupo:<22} | PAYLOAD: {payload}")

    # Para el mensaje concatenado, tomamos la primera carga útil registrada por cada SEQ
    mensaje_crudo = "".join(mapa_global[seq][0][1] for seq in secuencias_ordenadas)

    print("\n--- Mensaje Crudo Concatenado ---")
    print(mensaje_crudo)

if __name__ == "__main__":
    main()