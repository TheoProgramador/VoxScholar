# 🎙️ Real-Time Speech Pipeline (Faster-Whisper + Groq)

## 📌 Problema

Soluções de transcrição em tempo real geralmente exigem:
- infraestrutura pesada
- dependência total de APIs externas
- latência alta
- custo recorrente

Este projeto resolve isso com uma abordagem híbrida:

- 🔹 Transcrição local usando Faster-Whisper (baixo custo, alta eficiência)
- 🔹 Processamento opcional via Groq API para respostas rápidas com LLM
- 🔹 Arquitetura leve e minimalista

O foco é performance e controle.

---

## 🧠 Arquitetura

Microfone → Faster-Whisper (local) → Processamento opcional via Groq → Resposta

Pode rodar:
- 100% local
- Local + Groq
- CPU ou GPU

---

## 🖥️ Requisitos de Hardware

### Modo mínimo (CPU)
- Python 3.10+
- 4GB RAM
- Funciona até em máquinas modestas

### Modo recomendado (GPU)
- CUDA compatível
- 6GB+ VRAM para modelos maiores

Faster-Whisper é altamente otimizado e pode rodar até em dispositivos modestos.

---

## 🔑 Configuração da API Groq (Opcional)

Se quiser usar processamento via Groq:

1. Crie uma conta em: https://console.groq.com
2. Gere sua API Key
3. Configure como variável de ambiente

### Windows (PowerShell)

```powershell
setx GROQ_API_KEY "sua_chave_aqui"

python main.py