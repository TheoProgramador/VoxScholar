import pyttsx3

e = pyttsx3.init()
voices = e.getProperty("voices")
for i, v in enumerate(voices):
    print(i, getattr(v, "name", ""), getattr(v, "id", ""))