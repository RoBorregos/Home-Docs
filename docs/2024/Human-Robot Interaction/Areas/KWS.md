# Keyword Spotting (KWS)

Keyword Spotting (KWS) allows speech recognition systems to be more efficient, responsive, and energy friendly.

KWS is a critical component for speech pipelines, especially in voice assistants, as it enables a system to continuously wait for a wake word using a small number of resources.

In the context of RoboCup@Home, it is of extreme importance for speech recognition as all systems must be runned locally, a restriction that greatly limits the availability of computational resources. Further, it is very important as there can be a lot of noise during competitions and a KWS system allows us to efficiently filter audio that corresponds to random noise.

## Implementation

Currently, there is an [implementation](https://github.com/RoBorregos/home-hri/blob/main/ws/src/speech/scripts/KWS.py) of KWS that uses Picovoice’s [Porcupine](https://picovoice.ai/), a Wake Word Detection engine that is lightweight, highly-accurate, and that runs locally.

The node is constantly listening from the `rawAudioChunk` topic, and when a keyword is detected, it publishes a message to the `keyword_detected` topic. The `UsefulAudio` node may be listening to this topic (if the parameter is set), which is used to start recording audio for the STT module.

## Porcupine

Using porcupine is straightforward:

1. Login into webpage, get api key.
2. Enter keyword.
3. If keyword is available, download ‘model’.
4. Use porcupine’s python client to make inferences, by loading the model and passing chunks of audio.

## Problems

The main problems with using Porcupine are:

- Limited keywords: not all keywords are accepted when ‘training’ the model. Keywords must also have a specific length to work (‘yes’ and ‘no’ are too short). In addition, one free account can only make up to 3 different keywords.
- API keys: an api key can be used on, at most, 3 different devices. I'm not sure how, since it runs locally, but porcupine throws exceptions when keys have been used on more than 3 devices.
- Noise detectors: The platform doesn’t have support to detect specific noise, which could be used to get extra points in some of the tasks.
