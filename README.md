🎙️ Real-Time Speech Pipeline (Faster-Whisper + Groq)

Projeto experimental focado em performance, autonomia e controle total da pipeline de voz.

📌 Problema

Soluções tradicionais de transcrição em tempo real costumam exigir:

infraestrutura pesada

dependência integral de APIs externas

latência elevada

custo recorrente

Para quem quer estudar, testar ou construir algo próprio, isso rapidamente vira barreira.

💡 Proposta

Este projeto adota uma abordagem híbrida e eficiente:

🔹 Transcrição local com Faster-Whisper (baixo custo e alta performance)

🔹 Processamento opcional via Groq API para respostas ultra rápidas com LLM

🔹 Arquitetura leve, modular e controlável

O foco é simples: performance + autonomia + flexibilidade.

🧠 Arquitetura
Microfone 
   ↓
Faster-Whisper (local)
   ↓
Processamento opcional via Groq
   ↓
Resposta (texto / TTS)

Pode operar em três modos:

100% local

Local + Groq

CPU ou GPU

Sem lock-in. Sem dependência obrigatória.

🖥️ Requisitos de Hardware
🟢 Modo mínimo (CPU)

Python 3.10+

4GB RAM

Funciona em máquinas modestas

🔵 Modo recomendado (GPU)

CUDA compatível

6GB+ VRAM para modelos maiores

Melhor desempenho em transcrições longas

O Faster-Whisper é altamente otimizado e surpreendentemente eficiente.

🔑 Configuração da API Groq (Opcional)

Se desejar ativar processamento via Groq:

Crie uma conta em: https://console.groq.com

Gere sua API Key

Configure como variável de ambiente

Windows (PowerShell)
setx GROQ_API_KEY "sua_chave_aqui"

Depois:

python main.py
🚀 Objetivo do Projeto

Este não é um SaaS.

É um laboratório pessoal de engenharia aplicada a:

processamento de voz

pipelines híbridas

controle de latência

integração com LLMs

experimentação com modos de aprendizado

A arquitetura foi mantida propositalmente simples para facilitar evolução incremental.

🙏 Agradecimento

A ideia de estruturar o modo de aprendizado inspirado em apps como Duolingo surgiu em conversa com meu amigo Alessandro, cuja sugestão ajudou a expandir o projeto além da simples transcrição, transformando-o também em uma ferramenta prática de treino.

Boas ideias merecem crédito.
