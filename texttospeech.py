from google.cloud import texttospeech

# Set up Google Cloud TTS Client
def text_to_speech(text, output_file, language_code="en-US", voice_name="en-US-Wavenet-D"):
    # Initialize the TTS client
    client = texttospeech.TextToSpeechClient()

    # Set the input text
    input_text = texttospeech.SynthesisInput(text=text)

    # Configure the voice settings
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )

    # Configure audio output settings
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # Perform the TTS request
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # Save the output audio to a file
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to {output_file}")


# Example usage
if __name__ == "__main__":
    text = "Hello, this is your AI therapist speaking. How can I help you today?"
    output_file = "output.mp3"
    text_to_speech(text, output_file)
