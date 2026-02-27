from vad_record import VADRecorder
from stt_fw import FasterWhisperSTT
from llm_groq import GroqChat
from tts import TTS
import re
from Prompts import CHAT_PROMPT, STRICT_PROMPT
from text_clean import clean_for_tts
from voice_commands import detect_command
import argparse
import time

def set_mode(messages: list[dict], mode: str) -> str:
    mode = mode.lower().strip()
    if mode not in ("chat", "strict"):
        return "Modes: /chat or /strict"

    prompt = CHAT_PROMPT if mode == "chat" else STRICT_PROMPT

    # mantém histórico, só troca o system prompt (primeira mensagem)
    if messages and messages[0].get("role") == "system":
        messages[0]["content"] = prompt
    else:
        messages.insert(0, {"role": "system", "content": prompt})

    return f"Mode set to {mode}."

def clean_for_tts(text: str) -> str:
    # Remove **negrito**
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)

    # Remove *itálico*
    text = re.sub(r"\*(.*?)\*", r"\1", text)

    # Remove traços de lista no começo da linha
    text = re.sub(r"^\s*-\s*", "", text, flags=re.MULTILINE)

    return text

def apply_mode(messages: list[dict], mode: str) -> None:
    prompt = CHAT_PROMPT if mode == "chat" else STRICT_PROMPT
    if messages and messages[0].get("role") == "system":
        messages[0]["content"] = prompt
    else:
        messages.insert(0, {"role": "system", "content": prompt})



def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="ChatMode")
    args = ap.parse_args()
    passed = False

    recorder = VADRecorder(silence_ms=1200, vad_mode=2, max_record_s=25)

    stt = FasterWhisperSTT(model_name="base", device="cuda", compute_type="float16")
    llm = GroqChat(model="openai/gpt-oss-120b")
    tts = TTS(rate=130, voice_contains="zira")

    mode = "chat"
    messages = [{"role": "system", "content": CHAT_PROMPT}]

    print("VoiceTrainer pronto.")
    print('Diga: "switch to strict mode" / "switch to chat mode" / "reset context" / "quit"\n')

    try:
        while tts.is_speaking:
            time.sleep(0.05)

        while True:
            print("🎤 Speak now...")
            wav_path, _ = recorder.record_utterance("utterance.wav")
            if not wav_path:
                print("...no speech detected.\n")
                continue

            user_text = stt.transcribe(wav_path, language="en").strip()
            if not user_text:
                print("...couldn't transcribe.\n")
                continue

            print(f"You: {user_text}\n")

            cmd = detect_command(user_text)
            if cmd == "quit":
                tts.speak_async("Bye.")
                break
            
            if args.mode == "ChatMode" and passed == False:
                apply_mode(messages, "chat")
                passed = True
                messages = [{"role": "system", "content": CHAT_PROMPT }]
                #spoken = "Chat mode enabled." if mode == "chat" else "Strict mode enabled."
                #tts.speak(spoken)
                print("Chat Mode Enbled\n")
                continue

            if cmd == "reset":
                messages = [{"role": "system", "content": CHAT_PROMPT if mode == "chat" else STRICT_PROMPT}]
                tts.speak_async("Context reset.")
                print("Context reset.\n")
                continue

            if cmd in ("chat", "strict"):
                mode = cmd
                apply_mode(messages, mode)
                spoken = "Chat mode enabled." if mode == "chat" else "Strict mode enabled."
                tts.speak_async(spoken)
                print(spoken + "\n")
                continue

            # conversa normal
            messages.append({"role": "user", "content": user_text})

            reply = llm.chat(messages).strip()
            print(f"AI: {reply}\n")
            messages.append({"role": "assistant", "content": reply})

            tts.speak_blocking(clean_for_tts(reply))

    except KeyboardInterrupt:
        print("\nSaindo.")

if __name__ == "__main__":
    main()