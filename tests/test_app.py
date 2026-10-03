import pytest
import hashlib

# Função de Hash para validação direta
def gerar_hash_lgpd(chave):
    return hashlib.sha256(chave.strip().encode('utf-8')).hexdigest()

# Função simulada de cálculo de risco para teste unitário
def calcular_risco(valor, hora, q1, q2, q3, tem_denuncia):
    score = 0
    if hora >= 22 or hora < 6:
        score += 25
    if valor > 1000:
        score += 20
    if q1: score += 30
    if q2: score += 35
    if q3: score += 20
    if tem_denuncia: score += 50
    return min(score, 100)

# --- TESTES ---

def test_gerar_hash_lgpd():
    chave = "11999998888"
    hash_esperado = hashlib.sha256(chave.encode('utf-8')).hexdigest()
    assert gerar_hash_lgpd(chave) == hash_esperado

def test_calculo_risco_baixo():
    # Transação normal de dia (14h), valor baixo (R$ 50), sem questionário nem denúncias
    score = calcular_risco(valor=50, hora=14, q1=False, q2=False, q3=False, tem_denuncia=False)
    assert score == 0

def test_calculo_risco_alto_engenharia_social():
    # Suspeita de falso parente (q1 = True) durante a noite (23h)
    score = calcular_risco(valor=500, hora=23, q1=True, q2=False, q3=False, tem_denuncia=False)
    assert score == 55  # 25 (horário) + 30 (urgência)