import torch
from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration
import librosa

def transcribe_audio(audio_path, model_name="facebook/s2t-medium-librispeech-asr"):
    # Load the model and processor
    model = Speech2TextForConditionalGeneration.from_pretrained(model_name)
    processor = Speech2TextProcessor.from_pretrained(model_name)

    # Load and preprocess audio
    audio, original_sampling_rate = librosa.load(audio_path, sr=None)
    audio_resampled = librosa.resample(audio, orig_sr=original_sampling_rate, target_sr=16000)

    # Extract input features
    input_features = processor(
        audio_resampled,
        sampling_rate=16000,
        return_tensors="pt"
    ).input_features

    # Generate transcription
    generated_ids = model.generate(input_features=input_features)
    transcription = processor.batch_decode(generated_ids)

    # Clean the transcription
    cleaned_transcription = [t.replace("</s>", "").strip() for t in transcription]
    return cleaned_transcription[0]

# Example usage
# audio_path = "./harvard.wav"
# transcription = transcribe_audio(audio_path)
# print(transcription)
