# Respeaker

## Summary

The [ReSpeaker Mic Array v2.0](https://wiki.seeedstudio.com/ReSpeaker_Mic_Array_v2.0/) is an upgraded version of the original ReSpeaker Mic Array, designed to enhance voice interaction capabilities. It features four high-performance digital microphones arranged in an array, enabling effective far-field voice capture.

This year, we integrated this device to improve the quality of audio and obtain better inferences when perfroming STT. In addition, other features such as Noise Suppression and Direction of Arrival (DoA) detection extend greately the robot's capabilities.

In addition, the ReSpeaker Mic Array has LED ring support, which can be used to provide visual feedback to users. We use this feature to indicate the robot's status (speaking, listening).

## Nodes

### AudioCapturer.py

- **Purpose**: This node captures audio from the ReSpeaker hardware.
- **Usage**:
  - Publishes to: `rawAudioChunk`
  - Description: This node captures audio from the ReSpeaker hardware and publishes it to the `audio` topic.
- **relevance**: the node accepts a boolean parameter `respeaker` to enable or disable the ReSpeaker hardware. If set to true, the node will expect 6 audio channels when openning the stream and extract the 6th channel, which contains the merged playback.

### ReSpeaker.py

- **Purpose**: This node interfaces with the ReSpeaker hardware.
- **Usage**:
  - Publishes to: `DOA`
  - Subscribes to: `ReSpeaker/light`
  - Description: This node interfaces with the ReSpeaker hardware to get the direction of arrival (DOA) of sound and control the LED ring.

## Setup

The `ReSpeaker.py` file needs some permitions to interact with the ReSpeaker hardware (lights). To do so, you need to add the following udev rule:

```bash
echo "SUBSYSTEM=="usb", ATTR{idVendor}=="2886", ATTR{idProduct}=="0018", MODE="0666"" | sudo tee -a /etc/udev/rules.d/99-usb.rules
```

After adding the rule, you need to reload the udev rules:

```bash
sudo udevadm control --reload-rules
```
