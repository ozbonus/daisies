import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

load_dotenv()

elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY_DAISIES"),
)

audio = elevenlabs.text_to_dialogue.convert(
    inputs=[
        {
            "text": "[maniacal laughter] Where shall I put this car magazine, Mother?! [whispering] The cars are watching me!",
            "voice_id": "IKne3meq5aSn9XLyUdCD",
        },
        {
            "text": "Leave it on the stairs, please. Meow! I'll take it to my bedroom later. [purring] Purrrrr.",
            "voice_id": "9BWtsMINqrJLrRacOk9x",
        },
        {
            "text": "[screaming] OKAY! [giggling] And does this bowl... [deep voice] go in the kitchen of doom?",
            "voice_id": "IKne3meq5aSn9XLyUdCD",
        },
        {
            "text": "Actually, [barking] Woof! can you put it on the shelf above the bath, please? [howling] Awooooo!",
            "voice_id": "9BWtsMINqrJLrRacOk9x",
        },
        {
            "text": "[bouncing] Sure! Sure! Sure! Can I have this new lamp in my bedroom? [crying] It speaks to me!",
            "voice_id": "IKne3meq5aSn9XLyUdCD",
        },
        {
            "text": "Sorry. [clucking] Cluck cluck! It's for us to use outdoors. So put it next to the apple tree. Moo!",
            "voice_id": "9BWtsMINqrJLrRacOk9x",
        },
        {
            "text": "[grunting like a gorilla] What's in this heavy box? [high pitched] Is it secrets?",
            "voice_id": "IKne3meq5aSn9XLyUdCD",
        },
        {
            "text": "Books. [hissing] Hssss! Some of them will go in the living room and some in my bedroom. Put the box on the table next to the cooker. [roaring] Roar! I'll move it before we need the table for dinner.",
            "voice_id": "9BWtsMINqrJLrRacOk9x",
        },
        {
            "text": "[robotic] OK. This clock was in the hall in our old house... [glitch noise] wasn't it?",
            "voice_id": "IKne3meq5aSn9XLyUdCD",
        },
        {
            "text": "Yes, but I want it next to my wardrobe. [chirping] Tweet tweet! I like to know what time it is when I wake up. Quack!",
            "voice_id": "9BWtsMINqrJLrRacOk9x",
        },
        {
            "text": "[singing opera] What about this chaaaaaair? [speaking fast] Shall I put it in the living room or eat it?",
            "voice_id": "IKne3meq5aSn9XLyUdCD",
        },
        {
            "text": "Leave it in the entrance by the front door. [bleating] Baaaa! It's very heavy, so let's keep it downstairs. [snorting] Oink oink!",
            "voice_id": "9BWtsMINqrJLrRacOk9x",
        },
    ]
)

play(audio)