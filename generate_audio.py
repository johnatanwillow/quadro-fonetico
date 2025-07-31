import os
import sys
from google.cloud import texttospeech
from google.api_core.exceptions import GoogleAPIError

# --- CONFIGURAÇÃO GLOBAL ---
PATH_TO_YOUR_GOOGLE_CLOUD_KEY = 'google-cloud-key.json'
AUDIO_OUTPUT_DIR = 'audio'

# --- CONFIGURAÇÕES DE IDIOMA E VOZES ---
VOICE_ENGLISH_LANGUAGE_CODE = "en-GB"
VOICE_ENGLISH_NAME = "en-GB-Wavenet-A"
VOICE_ENGLISH_GENDER = texttospeech.SsmlVoiceGender.NEUTRAL

VOICE_FRENCH_LANGUAGE_CODE = "fr-FR"
VOICE_FRENCH_NAME = "fr-FR-Wavenet-B"
VOICE_FRENCH_GENDER = texttospeech.SsmlVoiceGender.FEMALE

# --- LISTA DE ITENS A SEREM GERADOS PARA INGLÊS ---
# Fonemas e Palavras do quadro fonético (sem prefixo)
ITEMS_TO_GENERATE_ENGLISH_PHONETIC = {
    "i": '<speak><phoneme alphabet="ipa" ph="iː">ee</phoneme></speak>',
    "ɪ": '<speak><phoneme alphabet="ipa" ph="ɪ">ih</phoneme></speak>',
    "ʊ": '<speak><phoneme alphabet="ipa" ph="ʊ">oo</phoneme></speak>',
    "u": '<speak><phoneme alphabet="ipa" ph="uː">oo</phoneme></speak>',
    "e": '<speak><phoneme alphabet="ipa" ph="e">eh</phoneme></speak>',
    "ə": '<speak><phoneme alphabet="ipa" ph="ə">uh</phoneme></speak>',
    "ɜ": '<speak><phoneme alphabet="ipa" ph="ɜː">ur</phoneme></speak>',
    "ɔ": '<speak><phoneme alphabet="ipa" ph="ɔː">aw</phoneme></speak>',
    "æ": '<speak><phoneme alphabet="ipa" ph="æ">aa</phoneme></speak>',
    "ʌ": '<speak><phoneme alphabet="ipa" ph="ʌ">uh</phoneme></speak>',
    "ɑ": '<speak><phoneme alphabet="ipa" ph="ɑː">ah</phoneme></speak>',
    "ɒ": '<speak><phoneme alphabet="ipa" ph="ɒ">oh</phoneme></speak>',
    "eɪ": '<speak><phoneme alphabet="ipa" ph="eɪ">ay</phoneme></speak>',
    "aɪ": '<speak><phoneme alphabet="ipa" ph="aɪ">eye</phoneme></speak>',
    "ɔɪ": '<speak><phoneme alphabet="ipa" ph="ɔɪ">oy</phoneme></speak>',
    "oʊ": '<speak><phoneme alphabet="ipa" ph="oʊ">oh</phoneme></speak>',
    "aʊ": '<speak><phoneme alphabet="ipa" ph="aʊ">ow</phoneme></speak>',
    "ɪə": '<speak><phoneme alphabet="ipa" ph="ɪə">ear</phoneme></speak>',
    "eə": '<speak><phoneme alphabet="ipa" ph="eə">air</phoneme></speak>',
    "ʊə": '<speak><phoneme alphabet="ipa" ph="ʊə">ure</phoneme></speak>',
    "p": '<speak><phoneme alphabet="ipa" ph="p">p</phoneme></speak>',
    "b": '<speak><phoneme alphabet="ipa" ph="b">b</phoneme></speak>',
    "t": '<speak><phoneme alphabet="ipa" ph="t">t</phoneme></speak>',
    "d": '<speak><phoneme alphabet="ipa" ph="d">d</phoneme></speak>',
    "k": '<speak><phoneme alphabet="ipa" ph="k">k</phoneme></speak>',
    "g": '<speak><phoneme alphabet="ipa" ph="g">g</phoneme></speak>',
    "m": '<speak><phoneme alphabet="ipa" ph="m">m</phoneme></speak>',
    "n": '<speak><phoneme alphabet="ipa" ph="n">n</phoneme></speak>',
    "ŋ": '<speak><phoneme alphabet="ipa" ph="ŋ">ng</phoneme></speak>',
    "f": '<speak><phoneme alphabet="ipa" ph="f">f</phoneme></speak>',
    "v": '<speak><phoneme alphabet="ipa" ph="v">v</phoneme></speak>',
    "θ": '<speak><phoneme alphabet="ipa" ph="θ">th</phoneme></speak>',
    "ð": '<speak><phoneme alphabet="ipa" ph="ð">th</phoneme></speak>',
    "s": '<speak><phoneme alphabet="ipa" ph="s">s</phoneme></speak>',
    "z": '<speak><phoneme alphabet="ipa" ph="z">z</phoneme></speak>',
    "ʃ": '<speak><phoneme alphabet="ipa" ph="ʃ">sh</phoneme></speak>',
    "ʒ": '<speak><phoneme alphabet="ipa" ph="ʒ">zh</phoneme></speak>',
    "h": '<speak><phoneme alphabet="ipa" ph="h">h</phoneme></speak>',
    "tʃ": '<speak><phoneme alphabet="ipa" ph="tʃ">ch</phoneme></speak>',
    "dʒ": '<speak><phoneme alphabet="ipa" ph="dʒ">j</phoneme></speak>',
    "l": '<speak><phoneme alphabet="ipa" ph="l">l</phoneme></speak>',
    "r": '<speak><phoneme alphabet="ipa" ph="r">r</phoneme></speak>',
    "j": '<speak><phoneme alphabet="ipa" ph="j">y</phoneme></speak>',
    "w": '<speak><phoneme alphabet="ipa" ph="w">w</phoneme></speak>',
    "cat": "cat",
    "hello": "hello",
    "apple": "apple",
    "banana": "banana",
    "table": "table",
    "water": "water",
    "computer": "computer",
    "english": "English",
    "phonetic": "phonetic"
}

# --- LISTA DE PALAVRAS PARA O QUESTIONÁRIO DE INGLÊS (EXEMPLO) ---
# O nome do arquivo gerado terá o prefixo "quiz_en_".
QUIZ_WORDS_ENGLISH = {
    "quiz_en_apple": "apple",
    "quiz_en_banana": "banana",
    "quiz_en_grape": "grape",
    "quiz_en_lemon": "lemon",
    "quiz_en_strawberry": "strawberry",
    "quiz_en_cookie": "cookie",
    "quiz_en_cake": "cake",
    "quiz_en_bread": "bread",
    "quiz_en_milk": "milk",
    "quiz_en_cheese": "cheese",
    "quiz_en_sugar": "sugar",
    "quiz_en_salt": "salt",
    "quiz_en_meat": "meat",
    "quiz_en_fish": "fish",
    "quiz_en_vegetable": "vegetable",
    "quiz_en_fruit": "fruit",
    "quiz_en_pencil": "pencil",
    "quiz_en_eraser": "eraser",
    "quiz_en_notebook": "notebook",
    "quiz_en_pen": "pen",
    "quiz_en_paper": "paper",
    "quiz_en_school": "school",
    "quiz_en_teacher": "teacher",
    "quiz_en_student": "student",
    "quiz_en_class": "class",
    "quiz_en_history": "history",
    "quiz_en_geography": "geography",
    "quiz_en_mathematics": "mathematics",
    "quiz_en_science": "science",
    "quiz_en_music": "music",
    "quiz_en_sport": "sport",
    "quiz_en_english": "English",
    "quiz_en_french": "French",
    "quiz_en_spanish": "Spanish",
    "quiz_en_german": "German",
    "quiz_en_friendship": "friendship",
    "quiz_en_family": "family",
    "quiz_en_father": "father",
    "quiz_en_mother": "mother",
    "quiz_en_brother": "brother",
    "quiz_en_sister": "sister",
    "quiz_en_grandfather": "grandfather",
    "quiz_en_grandmother": "grandmother",
    "quiz_en_uncle": "uncle",
    "quiz_en_aunt": "aunt",
    "quiz_en_cousin": "cousin",
    "quiz_en_dog": "dog",
    "quiz_en_cat": "cat",
    "quiz_en_bird": "bird",
    "quiz_en_fish_animal": "fish",
    "quiz_en_flower": "flower",
    "quiz_en_tree": "tree",
    "quiz_en_sun": "sun",
    "quiz_en_moon": "moon",
    "quiz_en_star": "star",
    "quiz_en_sky": "sky",
    "quiz_en_sea": "sea",
    "quiz_en_river": "river",
    "quiz_en_mountain": "mountain",
    "quiz_en_forest": "forest",
    "quiz_en_city": "city",
    "quiz_en_village": "village",
    "quiz_en_street": "street",
    "quiz_en_square": "square",
    "quiz_en_restaurant": "restaurant",
    "quiz_en_cafe": "cafe",
    "quiz_en_hotel": "hotel",
    "quiz_en_station": "station",
    "quiz_en_airport": "airport",
    "quiz_en_train": "train",
    "quiz_en_plane": "plane",
    "quiz_en_bus": "bus",
    "quiz_en_bicycle": "bicycle",
    "quiz_en_foot": "foot",
    "quiz_en_hand": "hand",
    "quiz_en_head": "head",
    "quiz_en_arm": "arm",
    "quiz_en_leg": "leg",
    "quiz_en_body": "body",
    "quiz_en_heart": "heart",
    "quiz_en_stomach": "stomach",
    "quiz_en_phone_call": "phone call",
    "quiz_en_computer_science": "computer science",
    "quiz_en_history_book": "history book",
    "quiz_en_music_class": "music class"
}

# --- LISTA DE ITENS A SEREM GERADOS PARA FRANCÊS ---
# Fonemas e Palavras do quadro fonético (com prefixo fr_)
ITEMS_TO_GENERATE_FRENCH_PHONETIC = {
    "fr_i": '<speak><phoneme alphabet="ipa" ph="i">i</phoneme></speak>',
    "fr_y": '<speak><phoneme alphabet="ipa" ph="y">u</phoneme></speak>',
    "fr_u": '<speak><phoneme alphabet="ipa" ph="u">ou</phoneme></speak>',
    "fr_e": '<speak><phoneme alphabet="ipa" ph="e">é</phoneme></speak>',
    "fr_ə": '<speak><phoneme alphabet="ipa" ph="ə">e muet</phoneme></speak>',
    "fr_ø": '<speak><phoneme alphabet="ipa" ph="ø">eu</phoneme></speak>',
    "fr_o": '<speak><phoneme alphabet="ipa" ph="o">o</phoneme></speak>',
    "fr_ɛ": '<speak><phoneme alphabet="ipa" ph="ɛ">è</phoneme></speak>',
    "fr_œ": '<speak><phoneme alphabet="ipa" ph="œ">eu</phoneme></speak>',
    "fr_ɔ": '<speak><phoneme alphabet="ipa" ph="ɔ">o</phoneme></speak>',
    "fr_a": '<speak><phoneme alphabet="ipa" ph="a">a</phoneme></speak>',
    "fr_ɑ": '<speak><phoneme alphabet="ipa" ph="ɑ">â</phoneme></speak>',
    "fr_ɛ̃": '<speak><phoneme alphabet="ipa" ph="ɛ̃">in</phoneme></speak>',
    "fr_ɔ̃": '<speak><phoneme alphabet="ipa" ph="ɔ̃">on</phoneme></speak>',
    "fr_œ̃": '<speak><phoneme alphabet="ipa" ph="œ̃">un</phoneme></speak>',
    "fr_ɑ̃": '<speak><phoneme alphabet="ipa" ph="ɑ̃">an</phoneme></speak>',
    "fr_ɥ": '<speak><phoneme alphabet="ipa" ph="ɥ">ui</phoneme></speak>',
    "fr_w": '<speak><phoneme alphabet="ipa" ph="w">oi</phoneme></speak>',
    "fr_j": '<speak><phoneme alphabet="ipa" ph="j">ill</phoneme></speak>',
    "fr_p": '<speak><phoneme alphabet="ipa" ph="p">p</phoneme></speak>',
    "fr_b": '<speak><phoneme alphabet="ipa" ph="b">b</phoneme></speak>',
    "fr_t": '<speak><phoneme alphabet="ipa" ph="t">t</phoneme></speak>',
    "fr_d": '<speak><phoneme alphabet="ipa" ph="d">d</phoneme></speak>',
    "fr_k": '<speak><phoneme alphabet="ipa" ph="k">c</phoneme></speak>',
    "fr_g": '<speak><phoneme alphabet="ipa" ph="g">g</phoneme></speak>',
    "fr_m": '<speak><phoneme alphabet="ipa" ph="m">m</phoneme></speak>',
    "fr_n": '<speak><phoneme alphabet="ipa" ph="n">n</phoneme></speak>',
    "fr_ɲ": '<speak><phoneme alphabet="ipa" ph="ɲ">gn</phoneme></speak>',
    "fr_f": '<speak><phoneme alphabet="ipa" ph="f">f</phoneme></speak>',
    "fr_v": '<speak><phoneme alphabet="ipa" ph="v">v</phoneme></speak>',
    "fr_s": '<speak><phoneme alphabet="ipa" ph="s">s</phoneme></speak>',
    "fr_z": '<speak><phoneme alphabet="ipa" ph="z">z</phoneme></speak>',
    "fr_ʃ": '<speak><phoneme alphabet="ipa" ph="ʃ">ch</phoneme></speak>',
    "fr_ʒ": '<speak><phoneme alphabet="ipa" ph="ʒ">j</phoneme></speak>',
    "fr_ʁ": '<speak><phoneme alphabet="ipa" ph="ʁ">r</phoneme></speak>',
    "fr_l": '<speak><phoneme alphabet="ipa" ph="l">l</phoneme></speak>',
    "fr_bonjour": "Bonjour",
    "fr_oui": "Oui",
    "fr_merci": "Merci",
    "fr_chat": "Chat",
    "fr_eau": "Eau",
    "fr_parler": "Parler",
    "fr_famille": "Famille",
    "fr_croissant": "Croissant"
}
##
# --- LISTA DE PALAVRAS PARA O QUESTIONÁRIO DE FRANCÊS (EXEMPLO) ---
# O nome do arquivo gerado terá o prefixo "quiz_fr_".
QUIZ_WORDS_FRENCH = {
    "quiz_fr_table": "table",
    "quiz_fr_chaise": "chaise",
    "quiz_fr_lit": "lit",
    "quiz_fr_lampe": "lampe",
    "quiz_fr_téléphone": "téléphone",
    "quiz_fr_stylo": "stylo",
    "quiz_fr_papier": "papier",
    "quiz_fr_crayon": "crayon",
    "quiz_fr_gomme": "gomme",
    "quiz_fr_cahier": "cahier",
    "quiz_fr_école": "école",
    "quiz_fr_professeur": "professeur",
    "quiz_fr_étudiant": "étudiant",
    "quiz_fr_classe": "classe",
    "quiz_fr_histoire": "histoire",
    "quiz_fr_géographie": "géographie",
    "quiz_fr_mathématiques": "mathématiques",
    "quiz_fr_science": "science",
    "quiz_fr_sport": "sport",
    "quiz_fr_musique": "musique",
    "quiz_fr_français": "français",
    "quiz_fr_anglais": "anglais",
    "quiz_fr_espagnol": "espagnol",
    "quiz_fr_allemand": "allemand",
    "quiz_fr_ami": "ami",
    "quiz_fr_famille": "famille",
    "quiz_fr_père": "père",
    "quiz_fr_mère": "mère",
    "quiz_fr_frère": "frère",
    "quiz_fr_sœur": "sœur",
    "quiz_fr_grand-père": "grand-père",
    "quiz_fr_grand-mère": "grand-mère",
    "quiz_fr_oncle": "oncle",
    "quiz_fr_tante": "tante",
    "quiz_fr_cousin": "cousin",
    "quiz_fr_cousine": "cousine",
    "quiz_fr_chien": "chien",
    "quiz_fr_chat": "chat",
    "quiz_fr_oiseau": "oiseau",
    "quiz_fr_poisson": "poisson",
    "quiz_fr_fleur": "fleur",
    "quiz_fr_arbre": "arbre",
    "quiz_fr_soleil": "soleil",
    "quiz_fr_lune": "lune",
    "quiz_fr_étoile": "étoile",
    "quiz_fr_ciel": "ciel",
    "quiz_fr_mer": "mer",
    "quiz_fr_rivière": "rivière",
    "quiz_fr_montagne": "montagne",
    "quiz_fr_forêt": "forêt",
    "quiz_fr_ville": "ville",
    "quiz_fr_village": "village",
    "quiz_fr_rue": "rue",
    "quiz_fr_place": "place",
    "quiz_fr_restaurant": "restaurant",
    "quiz_fr_café": "café",
    "quiz_fr_hôtel": "hôtel",
    "quiz_fr_gare": "gare",
    "quiz_fr_aéroport": "aéroport",
    "quiz_fr_train": "train",
    "quiz_fr_avion": "avion",
    "quiz_fr_bus": "bus",
    "quiz_fr_vélo": "vélo",
    "quiz_fr_pied": "pied",
    "quiz_fr_main": "main",
    "quiz_fr_tête": "tête",
    "quiz_fr_bras": "bras",
    "quiz_fr_jambe": "jambe",
    "quiz_fr_corps": "corps",
    "quiz_fr_cœur": "cœur",
    "quiz_fr_estomac": "estomac",
    "quiz_fr_eau": "eau",
    "quiz_fr_lait": "lait",
    "quiz_fr_fromage": "fromage",
    "quiz_fr_pain": "pain",
    "quiz_fr_beurre": "beurre",
    "quiz_fr_sucre": "sucre",
    "quiz_fr_sel": "sel",
    "quiz_fr_viande": "viande",
    "quiz_fr_poisson": "poisson",
    "quiz_fr_fruit": "fruit",
    "quiz_fr_légume": "légume",
    "quiz_fr_pomme": "pomme",
    "quiz_fr_orange": "orange",
    "quiz_fr_banane": "banane",
    "quiz_fr_fraise": "fraise",
    "quiz_fr_chocolat": "chocolat",
    "quiz_fr_gâteau": "gâteau"
}


# --- FUNÇÃO PRINCIPAL DE GERAÇÃO ---
def generate_audio_files(language="english"):
    if PATH_TO_YOUR_GOOGLE_CLOUD_KEY:
        if not os.path.exists(PATH_TO_YOUR_GOOGLE_CLOUD_KEY):
            print(f"ERRO: O arquivo da chave '{PATH_TO_YOUR_GOOGLE_CLOUD_KEY}' não foi encontrado.")
            sys.exit(1)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = PATH_TO_YOUR_GOOGLE_CLOUD_KEY

    try:
        client = texttospeech.TextToSpeechClient()
    except Exception as e:
        print(f"\n--- ERRO NA AUTENTICAÇÃO OU INICIALIZAÇÃO DO CLIENTE para {language.upper()} ---")
        print(f"Detalhes do erro: {e}")
        sys.exit(1)

    if language == "english":
        voice_params = texttospeech.VoiceSelectionParams(language_code=VOICE_ENGLISH_LANGUAGE_CODE, name=VOICE_ENGLISH_NAME, ssml_gender=VOICE_ENGLISH_GENDER)
        items_to_process_phonetic = ITEMS_TO_GENERATE_ENGLISH_PHONETIC
        items_to_process_quiz = QUIZ_WORDS_ENGLISH
        lang_display_name = "Inglês"
    elif language == "french":
        voice_params = texttospeech.VoiceSelectionParams(language_code=VOICE_FRENCH_LANGUAGE_CODE, name=VOICE_FRENCH_NAME, ssml_gender=VOICE_FRENCH_GENDER)
        items_to_process_phonetic = ITEMS_TO_GENERATE_FRENCH_PHONETIC
        items_to_process_quiz = QUIZ_WORDS_FRENCH
        lang_display_name = "Francês"
    else:
        print("Idioma não suportado. Escolha 'english' ou 'french'.")
        sys.exit(1)

    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    if not os.path.exists(AUDIO_OUTPUT_DIR):
        os.makedirs(AUDIO_OUTPUT_DIR)

    print(f"\nIniciando a geração de áudios para {lang_display_name}...")
    
    # Processa os itens do quadro fonético
    process_items(client, voice_params, audio_config, items_to_process_phonetic)
    # Processa os itens do questionário
    process_items(client, voice_params, audio_config, items_to_process_quiz)

    print(f"\n--- Geração para {lang_display_name} Concluída ---")

def process_items(client, voice_params, audio_config, items):
    for filename_prefix, text_or_ssml in items.items():
        output_path = os.path.join(AUDIO_OUTPUT_DIR, f"{filename_prefix}.mp3")
        synthesis_input = texttospeech.SynthesisInput(ssml=text_or_ssml) if text_or_ssml.strip().startswith('<speak>') else texttospeech.SynthesisInput(text=text_or_ssml)
        try:
            response = client.synthesize_speech(input=synthesis_input, voice=voice_params, audio_config=audio_config)
            with open(output_path, "wb") as out:
                out.write(response.audio_content)
            print(f"✔ Gerado: {filename_prefix}.mp3")
        except GoogleAPIError as e:
            print(f"✖ ERRO ao gerar {filename_prefix}.mp3: {e}")

if __name__ == "__main__":
    # --- GERAR OS AUDIOS PARA O QUIZ ---
    # Para gerar os áudios do quiz, descomente as linhas abaixo.
    generate_audio_files(language="english")
    generate_audio_files(language="french")

    # Recomenda-se gerar apenas os áudios do quiz, pois os do quadro fonético já existem.
    # generate_audio_files(language="english")
    # generate_audio_files(language="french")
    print("Execute 'generate_audio_files(language=\"english\")' e 'generate_audio_files(language=\"french\")' para gerar os áudios do questionário.")