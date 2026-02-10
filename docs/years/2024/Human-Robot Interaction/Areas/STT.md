# Improved speech-to-text module

- Migration to **Faster-Whisper** after **benchmarking**:
  - Improved speed (halved translation time).
  - Higher accuracy in noisy environments.
- **Dynamic Integration of "Hot Words"**:
  - Context-specific vocabulary dynamically adjusted.
  - Increases robustness and accuracy for uncommon terms.

---

# STT Benchmark#

| File (10s) | Size (MB) | Faster-whisper accuracy | Time (s) | Whisper accuracy | Time (s) |
| ---------- | --------- | ----------------------- | -------- | ---------------- | -------- |
| test1.wav  | 1.22      | 85.7%                   | 0.64     | 71.4%            | 1.25     |
| test2.wav  | 1.22      | 77.8%                   | 0.71     | 33.3%            | 1.44     |
| test3.wav  | 1.22      | 71.4%                   | 0.66     | 57.1%            | 1.13     |
| test4.wav  | 1.22      | 80%                     | 0.70     | 60%              | 1.36     |
| test5.wav  | 1.53      | 71.4%                   | 4.68     | 71.4%            | 4.5      |
| test6.wav  | 1.83      | 42.9%                   | 0.63     | 28.6%            | 1.03     |
| test7.wav  | 1.83      | 90%                     | 0.64     | 90%              | 0.87     |
| test8.wav  | 1.83      | 83.3%                   | 0.61     | 66.7%            | 0.99     |
| test9.wav  | 1.83      | 100%                    | 0.62     | 100%             | 0.94     |
| test10.wav | 1.83      | 100%                    | 0.58     | 100%             | 0.77     |
