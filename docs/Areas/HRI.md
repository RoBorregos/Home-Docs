# Human Robot Interaction

Human-Robot Interaction (HRI) refers to the study and design of interactions between humans and robots. It encompasses the development of technologies, interfaces, and systems that enable effective communication, collaboration, and cooperation between humans and robots. HRI aims to create intuitive and natural ways for humans to interact with robots, allowing for seamless integration of robots into various domains such as healthcare, manufacturing, entertainment, and personal assistance.

## HRI Overview

<p align="center">
<img src= "/assets/home/HRI/Pipeline.jpeg" alt="Pipeline overview" width="80%" height="80%">
</p>

Currently, in RoBorregos, the development of HRI consists of 2 pipelines: speech and NLP processing. The speech pipeline has several modules to achieve robustness while being computationally efficient (i.e. ensure resource-intensive models only infer voiced audio). The first module of speech is the Keyword Spotting node, which was implemented using porcupine. After the keyword is detected, audio is recorded until voice is no longer detected using Silero VAD. The audio captured is then inferred using Whisper.

Finally, the NLP pipeline processes the interpreted text by parsing the string into commands using an LLM. As a strategy to deal with malformed LLM outputs, the resulting commands are matched to the closest valid action according to the robot context and capabilities, found via cosine similarity by embedding the actions if there is no exact match.
