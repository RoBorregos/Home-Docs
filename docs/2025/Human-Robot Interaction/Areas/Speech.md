# Speech pipeline upgrades

This year, we implemented a realtime speech processing pipeline based on [Whisper live](https://github.com/collabora/WhisperLive/blob/main/whisper_live/backend/faster_whisper_backend.py).

We adapted the repository to use grpc communication rather than websockets so that it could be integrated into our existing architecture. Internally, the adapted code from Whisper Live transcribes a window of audio and concatenates the results into a full transcription that is sent at each update through the grpc service.

The grpc communication was implemented as a bidirectional stream, where the ros process sends audio chunks to the speech service, which in turn responds with updated transcriptions. From the caller (ros) side in our system, we wrapped this implementation using an action server to allow for easy feedback and cancellation of the speech recognition process.

This implementation reuses the faster whisper backend previously used, including its dockerfile. However, the integration of whisper live into our pipeline enabled us to remove other components such as VAD and noise suppression, which are now handled internally by Whisper live implementation and underlying faster whisper model.

One drawback is that the inference speed should be very fast because of the constant audio streaming and reinference. Currently, there is no cuda implementation for faster whisper in PC (we only have cuda support for Jetson devices in our repository).

## Usage

Start the docker container for the speech service: `stt-l4t.yaml`

Set up the correct ip address on the ros side in the action client: `hri/packages/speech/config/hear_streaming.yaml`

Start the container that handles hri's ros services: `hri-ros.yaml`

Testing can be performed using hri's subtask manager. For testing examples see `task_manager/scripts/test_hri_manager.py`

Note: run test script in integration's container.