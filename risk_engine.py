import math
import hashlib
import re
import datetime

def gerar_hash_chave(chave: str) -> str:
    """
    Gera o Hash SHA-256 da chave Pix para conformidade com a LGPD.
    """
    chave_limpa = re.sub(r'[\s\-\.\/\(\)\+]', '', chave.lower().strip())
    return hashlib.sha256(chave_limpa.encode('utf-8')).hexdigest()

def calcular_risk_score(denuncias: list, peso_v: float = 0.5, peso_r: float = 0.3, peso_g: float = 0.2, alpha: float = 1.0) -> float:
    """
    Algoritmo de cálculo de risco com decaimento temporal exponencial.
    """
    if not denuncias:
        return 0.0

    agora = datetime.datetime.now()
    lambda_decay = math.log(2) / 7.0

    v_k = 0.0
    soma_confiabilidade = 0.0

    for d in denuncias:
        dias_decorridos = (agora - d['data']).total_seconds() / 86400.0
        v_k += math.exp(-lambda_decay * dias_decorridos)
        soma_confiabilidade += d['confiabilidade_usuario']

    v_k_norm = min(100.0, v_k * 20.0)
    r_k = (soma_confiabilidade / len(denuncias)) * 100.0
    g_k = min(100.0, len(denuncias) * 15.0)

    score_bruto = (peso_v * v_k_norm + peso_r * r_k + peso_g * g_k) * alpha
    return round(min(100.0, max(0.0, score_bruto)), 2)