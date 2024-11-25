
## Human-Robot Interaction
# Development 2024

## **Speech and NLP pipeline upgrades**
- **Speech Pipeline**:
  - Optimized for robustness and computational efficiency.
  - **Modules**:
    - **Keyword Spotting**: Implemented using Porcupine.
    - **Voice Activity Detection**: Captures audio using Silero VAD.
    - **Speech-to-Text**: Audio inferred with Whisper.
  - Outputs text interpreted as commands by an LLM.
  - Handles malformed LLM outputs via cosine similarity to match the closest valid robot actions.

- **NLP Pipeline**:
  - Processes interpreted text into robot-executable commands.
  - Embeds actions for semantic matching when exact matches are unavailable.

---

## **Local command extraction**
- Crucial for dividing user instructions into actionable commands.
- Transition from OpenAI’s 3.5 Turbo (API dependent, latency issues) to a fine-tuned **Llama 3.2 3B** model for local use.
- **Benefits of the new implementation**:
  - Comparable performance.
  - Reduced latency and internet independence.
  - Fine-tuning results published on HuggingFace.

---

## **Local Entities Similarity**
- Matches parsed command components (e.g., action, location, item) to the robot's context.
- Uses **embedding models** for semantic similarity with cosine similarity comparison.
  - **Example**: "kitchen" inferred as "kitchen_table" if only "kitchen_table" and "office" exist.
- **Benchmarking**:
  - Multiple embedding models evaluated for specific tasks.
  - OpenAI text-embedding-3-small/large models used as a reference.
  - Synonyms generated using GPT-4 for evaluation metrics.

---

## **Improved speech-to-text module**
- Migration to **Faster-Whisper** after benchmarking:
  - Improved speed (halved translation time).
  - Higher accuracy in noisy environments.
- **Dynamic Integration of "Hot Words"**:
  - Context-specific vocabulary dynamically adjusted.
  - Increases robustness and accuracy for uncommon terms.

---

This framework improves HRI by enhancing speech processing, NLP command parsing, and context-aware command execution while reducing latency and dependencies.
