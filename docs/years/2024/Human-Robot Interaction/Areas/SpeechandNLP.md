# Speech and NLP pipeline upgrades
- **Speech Pipeline**: Optimized for robustness and computational efficiency.
    - **Keyword Spotting**: Implemented using Porcupine, a fast detector commonly used to spot 'Frida', our robot's name.
    - **Voice Activity Detection**: Captures audio using Silero VAD to ensure a voice is present.
    - **Speech-to-Text**: Audio inferred with Faster-whisper.
        - Outputs raw text which is to be interpreted as commands by an LLM.
        - A benchmark was made to compare whisper with faster-whisper alternatives which improved transcription time by half in most cases.
        - This model allows the use of hot words which are high probability words to be interpreted depending on the context of the task that the robot is performing, resulting in higher transcription accuracy.

- **NLP Pipeline**:
    - Processes interpreted text into robot-executable commands.
    - Embeds actions for semantic matching when exact matches are unavailable.


