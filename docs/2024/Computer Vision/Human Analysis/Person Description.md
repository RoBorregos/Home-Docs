# Person Description
In order to describe a person, originally dlib was used to extract an approximate age, race and gender. However, this was usually not very precise, so a different approach was integrated.

## Moondream
For visual model descriptions the locally hosted VLLM Moondream was used. Model, which is a prompt power visual analysis model. Given a contextualized frame with a specific prompt, the model provides an accurate description of the image enhanced with the prompt analysis and response. 