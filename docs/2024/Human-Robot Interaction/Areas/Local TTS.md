# Local TTS

Based on our experience during the last Mexican Tournament of Robotics, internet connection tends to be a problem in the competition area. Not only the internet was unavailable, but the connection was often slow, making a poor experience for the users. This is why we decided to implement a local TTS system.

## Piper

[Piper](https://github.com/rhasspy/piper) is a fast, local neural TTS system. It contains a variety of pre-trained models in many supported languages.

Currently, there are 2 implementations to [run Piper](https://github.com/RoBorregos/home-hri/blob/main/ws/src/speech/scripts/Say.py#L171):

1. Install `piper` library using `pip`
2. Install `piper` by compiling from source

For laptop users, the dockerfile supports the first implementation, which is more straigthforward. For Nvidia Jetson, the second implementation is recommended because using the pre-built wheel sometimes yielded errors, which were fixed by compiling from source.
