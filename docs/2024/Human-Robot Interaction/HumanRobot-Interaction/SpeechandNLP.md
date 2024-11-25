# Speech and NLP pipeline upgrades
- **Speech Pipeline**:
  - Optimized for robustness and computational efficiency.
  - **Modules**:
    - **Keyword Spotting**: Implemented using Porcupine.
    - **Voice Activity Detection**: Captures audio using Silero VAD.
    - **Speech-to-Text**: Audio inferred with Faster-whisper.
  - Outputs text interpreted as commands by an LLM.
  - Handles malformed LLM outputs via cosine similarity to match the closest valid robot actions.
  - A benchmark was made to compare whisper with faster-whisper alternatives which improved transcription time by half in most cases.
  - This model allows the use of hot words which are high probability words to be interpreted depending on the context of the task that the robot is performing, resulting in higher transcription accuracy.

- **NLP Pipeline**:
  - Processes interpreted text into robot-executable commands.
  - Embeds actions for semantic matching when exact matches are unavailable.


