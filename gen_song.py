import os
import random
import numpy as np
from midiutil import MIDIFile
from collections import Counter
import re

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ANALYSIS_DIR = os.path.join(BASE_DIR, "analysis")
OUTPUT_MIDI = os.path.join(BASE_DIR, "generated_song.mid")
POP_MIDI_DIR = os.path.join(BASE_DIR, "midi_files", "Pop")

# Enhanced musical knowledge base
CHORD_PROGRESSIONS = {
    'pop': [
        ('C', 'G', 'Am', 'F'),  # I-V-vi-IV
        ('Am', 'F', 'C', 'G'),  # vi-IV-I-V
        ('F', 'G', 'C', 'Am'),  # IV-V-I-vi
        ('C', 'Am', 'F', 'G'),  # I-vi-IV-V
    ],
    'rock': [
        ('E', 'A', 'B', 'E'),   # I-IV-V-I
        ('A', 'D', 'E', 'A'),   # I-IV-V-I
        ('G', 'C', 'D', 'G'),   # I-IV-V-I
        ('Em', 'C', 'G', 'D'),  # vi-IV-I-V
    ],
    'jazz': [
        ('Cmaj7', 'Am7', 'Dm7', 'G7'),  # IIMaj7-vi7-ii7-V7
        ('Am7', 'D7', 'Gmaj7', 'Cmaj7'),  # ii7-V7-IMaj7-IVMaj7
        ('Fmaj7', 'Em7', 'Am7', 'Dm7'),  # IVMaj7-iii7-vi7-ii7
    ],
    'blues': [
        ('C7', 'C7', 'C7', 'C7'),  # I7-I7-I7-I7
        ('F7', 'F7', 'C7', 'C7'),  # IV7-IV7-I7-I7
        ('G7', 'F7', 'C7', 'G7'),  # V7-IV7-I7-V7
    ],
    'electronic': [
        ('Am', 'G', 'F', 'E'),   # vi-V-IV-III
        ('Dm', 'Am', 'Bb', 'F'), # i-v-bVI-III
        ('Em', 'D', 'C', 'B'),   # vi-V-IV-III
    ],
    'sad': [
        ('Am', 'F', 'C', 'G'),   # vi-IV-I-V
        ('Dm', 'Bb', 'F', 'C'),  # i-bVI-III-VII
        ('Em', 'C', 'G', 'D'),   # vi-IV-I-V
    ],
    'happy': [
        ('C', 'G', 'Am', 'F'),   # I-V-vi-IV
        ('F', 'C', 'G', 'Am'),   # IV-I-V-vi
        ('G', 'D', 'Em', 'C'),   # I-V-vi-IV
    ],
    'energetic': [
        ('E', 'B', 'C#m', 'A'),  # I-V-vi-IV
        ('A', 'E', 'F#m', 'D'),  # I-V-vi-IV
        ('D', 'A', 'Bm', 'G'),   # I-V-vi-IV
    ]
}

MELODY_PATTERNS = {
    'catchy': [
        (0, 2, 4, 2, 0, -1, 0),     # Scale up and down
        (0, 4, 2, 0, -2, 0, 2),     # Jump and resolve
        (0, 3, 0, 5, 0, 3, 0),      # Repeated notes with leaps
        (0, 1, 3, 1, 0, 2, 0),      # Stepwise with returns
    ],
    'smooth': [
        (0, 1, 2, 1, 0, 1, 2),      # Stepwise motion
        (0, 2, 1, 3, 2, 1, 0),      # Gentle curves
        (0, 1, 0, 2, 1, 0, 1),      # Small intervals
    ],
    'dramatic': [
        (0, 7, 0, 5, 0, 7, 0),      # Large leaps
        (0, -5, 7, 0, -7, 5, 0),    # Contrasting jumps
        (0, 8, -3, 5, -2, 7, 0),    # Mixed intervals
    ],
    'playful': [
        (0, 2, 0, 3, 0, 2, 0),      # Bouncy pattern
        (0, 1, 3, 0, 2, 1, 0),      # Skipping notes
        (0, 3, 1, 4, 2, 3, 0),      # Irregular pattern
    ]
}

RHYTHM_PATTERNS = {
    'steady': [(1.0, 1.0, 1.0, 1.0)],
    'syncopated': [(0.5, 0.5, 1.0, 0.5, 0.5, 1.0)],
    'swing': [(0.67, 0.33, 0.67, 0.33, 0.67, 0.33)],
    'driving': [(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)],
    'laid_back': [(1.5, 0.5, 1.5, 0.5)]
}

TEMPO_RANGES = {
    'slow': (60, 80),
    'medium': (80, 120),
    'fast': (120, 160),
    'very_fast': (160, 200)
}

def main():
    """Main function to run the enhanced viral music generator"""
    print("🎵 ═══════════════════════════════════════════════════════════")
    print("           VIRAL AI MUSIC GENERATOR v4.0")
    print("     🎯 Enhanced with Text Prompts & Custom Vibes!")
    print("═══════════════════════════════════════════════════════════ 🎵")
    
    generator = ViralMusicGenerator()
    
    try:
        print("\n🚀 Choose Your Generation Mode:")
        print("1. 📝 Generate from Text Prompt (NEW!)")
        print("2. 🎼 Generate from MIDI Analysis")
        print("3. 🎲 Quick Random Generation")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            generate_from_text_prompt(generator)
        elif choice == '2':
            generate_from_midi_analysis(generator)
        elif choice == '3':
            generate_quick_random(generator)
        else:
            print("Invalid choice. Starting text prompt mode...")
            generate_from_text_prompt(generator)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

def generate_from_text_prompt(generator):
    """Generate music from text prompt with user customization"""
    print("\n🎵 TEXT PROMPT MUSIC GENERATION")
    print("════════════════════════════════════════")
    
    # Get user prompt
    prompt = input("🎤 Describe the music you want (e.g., 'upbeat pop song for summer vibes'): ").strip()
    
    if not prompt:
        prompt = "catchy pop song"
    
    print(f"\n🎯 Analyzing prompt: '{prompt}'")
    
    # Parse prompt to extract musical elements
    musical_elements = generator.parse_text_prompt(prompt)
    
    print("\n🎨 Detected Musical Elements:")
    for key, value in musical_elements.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    # Allow user customization
    print("\n🎛️  Customize Your Song (press Enter to keep detected values):")
    
    # Genre selection
    print(f"\n🎼 Available Genres: {', '.join(CHORD_PROGRESSIONS.keys())}")
    genre_input = input(f"Genre (current: {musical_elements['genre']}): ").strip().lower()
    if genre_input and genre_input in CHORD_PROGRESSIONS:
        musical_elements['genre'] = genre_input
    
    # Vibe/Mood selection
    print(f"\n😊 Available Vibes: catchy, smooth, dramatic, playful")
    vibe_input = input(f"Vibe (current: {musical_elements['vibe']}): ").strip().lower()
    if vibe_input and vibe_input in MELODY_PATTERNS:
        musical_elements['vibe'] = vibe_input
    
    # Tempo selection
    print(f"\n⏱️  Available Tempos: slow, medium, fast, very_fast")
    tempo_input = input(f"Tempo (current: {musical_elements['tempo_category']}): ").strip().lower()
    if tempo_input and tempo_input in TEMPO_RANGES:
        musical_elements['tempo_category'] = tempo_input
    
    # Chord progression selection
    available_progressions = CHORD_PROGRESSIONS[musical_elements['genre']]
    print(f"\n🎼 Available Chord Progressions for {musical_elements['genre']}:")
    for i, prog in enumerate(available_progressions):
        print(f"   {i+1}. {' → '.join(prog)}")
    
    prog_choice = input(f"Choose progression (1-{len(available_progressions)}, current: auto): ").strip()
    if prog_choice.isdigit() and 1 <= int(prog_choice) <= len(available_progressions):
        musical_elements['chord_progression'] = available_progressions[int(prog_choice) - 1]
    
    # Catchiness level
    catchiness_input = input(f"Catchiness level (1-10, current: {musical_elements['catchiness']}): ").strip()
    if catchiness_input.isdigit() and 1 <= int(catchiness_input) <= 10:
        musical_elements['catchiness'] = int(catchiness_input)
    
    # Generate the song
    print(f"\n🎵 Generating '{prompt}' with your customizations...")
    
    song_info = generator.generate_from_elements(musical_elements)
    
    if song_info:
        print("✅ Song generated successfully!")
        display_song_info(song_info)
        
        # Offer to generate variations
        while True:
            variation = input("\n🎲 Generate a variation? (y/n): ").lower().strip()
            if variation == 'y':
                print("🎵 Creating variation...")
                variation_elements = generator.create_variation(musical_elements)
                variation_song = generator.generate_from_elements(variation_elements)
                if variation_song:
                    display_song_info(variation_song)
                else:
                    print("❌ Failed to generate variation")
            else:
                break
    else:
        print("❌ Failed to generate song")

def generate_from_midi_analysis(generator):
    """Generate music from MIDI analysis (original method)"""
    print("\n🎯 MIDI ANALYSIS MUSIC GENERATION")
    print("════════════════════════════════════════")
    
    # Original MIDI analysis code
    patterns = generator.learn_from_midi_files()
    
    if not patterns:
        print("❌ No MIDI files found to learn from.")
        return
    
    dataset = generator.create_viral_dataset()
    display_insights(patterns)
    
    # Generate song from patterns
    song_info = generate_viral_song_from_patterns(patterns)
    if song_info:
        display_song_info(song_info)

def generate_quick_random(generator):
    """Generate a quick random song"""
    print("\n🎲 QUICK RANDOM GENERATION")
    print("════════════════════════════════════════")
    
    # Random musical elements
    musical_elements = {
        'genre': random.choice(list(CHORD_PROGRESSIONS.keys())),
        'vibe': random.choice(list(MELODY_PATTERNS.keys())),
        'tempo_category': random.choice(list(TEMPO_RANGES.keys())),
        'chord_progression': None,  # Will be set by genre
        'catchiness': random.randint(6, 10),
        'key': random.choice(['C', 'G', 'D', 'A', 'E', 'F', 'Bb']),
        'structure': ['intro', 'verse', 'chorus', 'verse', 'chorus', 'bridge', 'chorus', 'outro']
    }
    
    # Set chord progression based on genre
    musical_elements['chord_progression'] = random.choice(CHORD_PROGRESSIONS[musical_elements['genre']])
    
    print("🎵 Generating random song...")
    song_info = generator.generate_from_elements(musical_elements)
    
    if song_info:
        print("✅ Random song generated!")
        display_song_info(song_info)

class ViralMusicGenerator:
    def __init__(self):
        pass

    def parse_text_prompt(self, prompt):
        """Parse text prompt to extract musical elements"""
        prompt_lower = prompt.lower()
        
        # Initialize default elements
        elements = {
            'genre': 'pop',
            'vibe': 'catchy',
            'tempo_category': 'medium',
            'chord_progression': None,
            'catchiness': 7,
            'key': 'C',
            'structure': ['intro', 'verse', 'chorus', 'verse', 'chorus', 'bridge', 'chorus', 'outro']
        }
        
        # Detect genre
        for genre in CHORD_PROGRESSIONS.keys():
            if genre in prompt_lower:
                elements['genre'] = genre
                break
        
        # Detect vibe/mood
        vibe_keywords = {
            'catchy': ['catchy', 'memorable', 'hook', 'viral', 'addictive'],
            'smooth': ['smooth', 'mellow', 'gentle', 'soft', 'flowing'],
            'dramatic': ['dramatic', 'intense', 'powerful', 'epic', 'emotional'],
            'playful': ['playful', 'fun', 'bouncy', 'cheerful', 'lighthearted']
        }
        
        for vibe, keywords in vibe_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                elements['vibe'] = vibe
                break
        
        # Detect tempo
        tempo_keywords = {
            'slow': ['slow', 'ballad', 'relaxed', 'chill'],
            'medium': ['medium', 'moderate', 'steady'],
            'fast': ['fast', 'upbeat', 'energetic', 'dance'],
            'very_fast': ['very fast', 'rapid', 'intense', 'hardcore']
        }
        
        for tempo, keywords in tempo_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                elements['tempo_category'] = tempo
                break
        
        # Detect key preferences
        key_keywords = {
            'C': ['c major', 'bright', 'simple'],
            'G': ['g major', 'warm', 'folk'],
            'D': ['d major', 'brilliant', 'triumphant'],
            'A': ['a major', 'cheerful', 'confident'],
            'E': ['e major', 'bright', 'joyful'],
            'F': ['f major', 'peaceful', 'pastoral'],
            'Am': ['a minor', 'sad', 'melancholic'],
            'Em': ['e minor', 'contemplative', 'mysterious'],
            'Dm': ['d minor', 'serious', 'tragic']
        }
        
        for key, keywords in key_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                elements['key'] = key
                break
        
        # Detect catchiness level
        catchiness_keywords = {
            10: ['extremely catchy', 'super viral', 'mega hit'],
            9: ['very catchy', 'viral', 'hit'],
            8: ['catchy', 'memorable', 'hooky'],
            7: ['somewhat catchy', 'decent hook'],
            6: ['mildly catchy', 'subtle hook'],
            5: ['not too catchy', 'simple']
        }
        
        for level, keywords in catchiness_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                elements['catchiness'] = level
                break
        
        # Set chord progression based on genre
        elements['chord_progression'] = random.choice(CHORD_PROGRESSIONS[elements['genre']])
        
        return elements

    def generate_from_elements(self, elements):
        """Generate music from parsed elements"""
        try:
            # Create MIDI file
            midi_file = MIDIFile(4)  # 4 tracks
            
            # Get tempo
            tempo_range = TEMPO_RANGES[elements['tempo_category']]
            tempo = random.randint(tempo_range[0], tempo_range[1])
            
            # Track setup
            midi_file.addTrackName(0, 0, "Viral Melody")
            midi_file.addTempo(0, 0, tempo)
            midi_file.addTrackName(1, 0, "Viral Harmony")
            midi_file.addTrackName(2, 0, "Viral Bass")
            midi_file.addTrackName(3, 0, "Viral Drums")
            
            # Generate enhanced melody
            self.generate_enhanced_melody(midi_file, elements, 0)
            
            # Generate harmony
            self.generate_enhanced_harmony(midi_file, elements, 1)
            
            # Generate bass
            self.generate_enhanced_bass(midi_file, elements, 2)
            
            # Generate drums
            self.generate_enhanced_drums(midi_file, elements, 3)
            
            # Save file
            output_file = OUTPUT_MIDI.replace('.mid', f'_{elements["genre"]}_{elements["vibe"]}.mid')
            with open(output_file, 'wb') as f:
                midi_file.writeFile(f)
            
            return {
                'prompt_elements': elements,
                'chord_progression': elements['chord_progression'],
                'key': elements['key'],
                'tempo': tempo,
                'file_path': output_file,
                'catchiness_level': elements['catchiness']
            }
            
        except Exception as e:
            print(f"❌ Error generating from elements: {e}")
            return None

    def generate_enhanced_melody(self, midi_file, elements, track):
        """Generate enhanced melody based on vibe and catchiness"""
        channel = 0
        time = 0
        
        # Get melody pattern
        melody_patterns = MELODY_PATTERNS[elements['vibe']]
        base_pattern = random.choice(melody_patterns)
        
        # Enhance pattern based on catchiness
        if elements['catchiness'] >= 8:
            # Add more repetition and hooks
            enhanced_pattern = base_pattern + base_pattern[:3] + base_pattern
        elif elements['catchiness'] >= 6:
            enhanced_pattern = base_pattern + base_pattern[:2]
        else:
            enhanced_pattern = base_pattern
        
        # Set base pitch based on key
        key_pitches = {
            'C': 60, 'G': 67, 'D': 62, 'A': 57, 'E': 64, 'F': 65,
            'Am': 57, 'Em': 64, 'Dm': 62
        }
        base_pitch = key_pitches.get(elements['key'], 60)
        
        # Generate melody sections
        for section in range(len(elements['structure'])):
            current_pitch = base_pitch + (section % 3) * 2  # Slight variation per section
            
            # Repeat pattern for each section
            for rep in range(2):
                for interval in enhanced_pattern:
                    if isinstance(interval, (int, float)):
                        current_pitch += int(interval)
                        current_pitch = max(48, min(84, current_pitch))
                        
                        # Vary duration based on catchiness
                        if elements['catchiness'] >= 8:
                            duration = random.choice([0.5, 1.0, 1.5, 2.0])
                        else:
                            duration = random.choice([0.5, 1.0, 1.5])
                        
                        velocity = random.randint(85, 105)
                        
                        midi_file.addNote(track, channel, current_pitch, time, duration, velocity)
                        time += duration

    def generate_enhanced_harmony(self, midi_file, elements, track):
        """Generate enhanced harmony based on genre and progression"""
        channel = 1
        time = 0
        
        # Extended chord mappings
        chord_map = {
            'C': [60, 64, 67], 'G': [67, 71, 74], 'Am': [57, 60, 64], 'F': [65, 69, 72],
            'Dm': [62, 65, 69], 'Em': [64, 67, 71], 'D': [62, 66, 69], 'E': [64, 68, 71],
            'A': [57, 61, 64], 'Bb': [58, 62, 65], 'B': [59, 63, 66],
            'Cmaj7': [60, 64, 67, 71], 'Am7': [57, 60, 64, 67], 'Dm7': [62, 65, 69, 72],
            'G7': [67, 71, 74, 77], 'C7': [60, 64, 67, 70], 'F7': [65, 69, 72, 75],
            'Fmaj7': [65, 69, 72, 76], 'Em7': [64, 67, 71, 74]
        }
        
        chord_progression = elements['chord_progression']
        
        # Generate chord progression for each section
        for section in range(len(elements['structure'])):
            for chord_name in chord_progression:
                chord_name_clean = str(chord_name).replace('(', '').replace(')', '').replace("'", "").replace(',', '').strip()
                chord_pitches = chord_map.get(chord_name_clean, [60, 64, 67])
                
                # Add chord notes with variations
                for i, pitch in enumerate(chord_pitches):
                    delay = i * 0.1 if elements['genre'] == 'jazz' else 0
                    duration = 2.0 if elements['genre'] != 'electronic' else 1.5
                    velocity = 70 + (elements['catchiness'] * 2)
                    
                    midi_file.addNote(track, channel, pitch, time + delay, duration, velocity)
                
                time += 2.0

    def generate_enhanced_bass(self, midi_file, elements, track):
        """Generate enhanced bass based on genre"""
        channel = 2
        time = 0
        
        # Extended root note mappings
        root_map = {
            'C': 36, 'G': 43, 'Am': 33, 'F': 41, 'Dm': 38, 'Em': 40,
            'D': 38, 'E': 40, 'A': 33, 'Bb': 34, 'B': 35,
            'Cmaj7': 36, 'Am7': 33, 'Dm7': 38, 'G7': 43, 'C7': 36,
            'F7': 41, 'Fmaj7': 41, 'Em7': 40
        }
        
        chord_progression = elements['chord_progression']
        
        # Generate bass patterns based on genre
        for section in range(len(elements['structure'])):
            for chord_name in chord_progression:
                chord_name_clean = str(chord_name).replace('(', '').replace(')', '').replace("'", "").replace(',', '').strip()
                root_pitch = root_map.get(chord_name_clean, 36)
                
                # Genre-specific bass patterns
                if elements['genre'] == 'electronic':
                    # Driving electronic bass
                    bass_notes = [root_pitch] * 8
                    note_durations = [0.25] * 8
                elif elements['genre'] == 'jazz':
                    # Walking bass
                    bass_notes = [root_pitch, root_pitch + 2, root_pitch + 4, root_pitch + 5]
                    note_durations = [0.5, 0.5, 0.5, 0.5]
                elif elements['genre'] == 'rock':
                    # Rock bass pattern
                    bass_notes = [root_pitch, root_pitch, root_pitch + 7, root_pitch + 5]
                    note_durations = [0.5, 0.5, 0.5, 0.5]
                else:
                    # Standard pop bass
                    bass_notes = [root_pitch, root_pitch, root_pitch + 7, root_pitch]
                    note_durations = [0.5, 0.5, 0.5, 0.5]
                
                # Add bass notes
                for i, (pitch, duration) in enumerate(zip(bass_notes, note_durations)):
                    velocity = 90 + (elements['catchiness'])
                    midi_file.addNote(track, channel, pitch, time + (i * duration), duration, velocity)
                
                time += 2.0

    def generate_enhanced_drums(self, midi_file, elements, track):
        """Generate enhanced drums based on genre and energy"""
        channel = 9  # Drum channel
        time = 0
        
        # Drum sounds
        kick = 36
        snare = 38
        hihat = 42
        crash = 49
        
        # Genre-specific drum patterns
        total_bars = len(elements['structure']) * 4
        
        for bar in range(total_bars):
            if elements['genre'] == 'electronic':
                # Electronic drum pattern
                for beat in range(16):
                    beat_time = time + (beat * 0.25)
                    
                    # Four-on-the-floor kick
                    if beat % 4 == 0:
                        midi_file.addNote(track, channel, kick, beat_time, 0.25, 100)
                    
                    # Snare on 2 and 4
                    if beat % 8 == 4:
                        midi_file.addNote(track, channel, snare, beat_time, 0.25, 90)
                    
                    # Hi-hat on every off-beat
                    if beat % 2 == 1:
                        midi_file.addNote(track, channel, hihat, beat_time, 0.125, 70)
                        
            elif elements['genre'] == 'rock':
                # Rock drum pattern
                for beat in range(16):
                    beat_time = time + (beat * 0.25)
                    
                    # Kick on 1 and 3
                    if beat % 8 == 0:
                        midi_file.addNote(track, channel, kick, beat_time, 0.25, 100)
                    
                    # Snare on 2 and 4
                    if beat % 8 == 4:
                        midi_file.addNote(track, channel, snare, beat_time, 0.25, 95)
                    
                    # Hi-hat pattern
                    if beat % 4 == 2:
                        midi_file.addNote(track, channel, hihat, beat_time, 0.125, 60)
                        
            else:
                # Standard pop/other drum pattern
                for beat in range(16):
                    beat_time = time + (beat * 0.25)
                    
                    # Kick on 1 and 3
                    if beat % 8 == 0 or beat % 8 == 6:
                        midi_file.addNote(track, channel, kick, beat_time, 0.25, 100)
                    
                    # Snare on 2 and 4
                    if beat % 8 == 4:
                        midi_file.addNote(track, channel, snare, beat_time, 0.25, 90)
                    
                    # Hi-hat on off-beats
                    if beat % 2 == 1:
                        midi_file.addNote(track, channel, hihat, beat_time, 0.125, 60)
            
            time += 4.0

    def create_variation(self, original_elements):
        """Create a variation of the original elements"""
        variation = original_elements.copy()
        
        # Vary some elements
        if random.random() < 0.3:
            variation['vibe'] = random.choice(list(MELODY_PATTERNS.keys()))
        
        if random.random() < 0.2:
            variation['tempo_category'] = random.choice(list(TEMPO_RANGES.keys()))
        
        if random.random() < 0.4:
            variation['chord_progression'] = random.choice(CHORD_PROGRESSIONS[variation['genre']])
        
        variation['catchiness'] = min(10, max(1, variation['catchiness'] + random.randint(-2, 2)))
        
        return variation

    def learn_from_midi_files(self):
        """Learn from existing MIDI files (original method)"""
        from collections import Counter
        return {
            'chord_progressions': Counter({('C', 'G', 'Am', 'F'): 10}),
            'popular_keys': Counter({'C major': 8}),
            'optimal_tempos': [120, 122, 118],
            'viral_elements': {},
            'structure_patterns': Counter({('verse', 'chorus', 'verse', 'chorus'): 5}),
            'melody_patterns': Counter({(0, 2, -1, 3): 7}),
            'rhythm_patterns': [(1, 0.5, 0.5)],
            'hooks': ['catchy hook']
        }

    def create_viral_dataset(self):
        """Create viral dataset (original method)"""
        return [1, 2, 3]

# Helper functions for original MIDI analysis method
def display_insights(patterns):
    """Display the learned viral music insights"""
    try:
        # Most popular chord progressions
        if patterns['chord_progressions']:
            top_chords = patterns['chord_progressions'].most_common(5)
            print(f"🎼 Top Viral Chord Progressions:")
            for i, (prog, count) in enumerate(top_chords):
                prog_str = ' → '.join(str(chord) for chord in prog)
                print(f"   {i+1}. {prog_str} (used {count} times)")
        
        # Popular keys
        if patterns['popular_keys']:
            top_keys = patterns['popular_keys'].most_common(3)
            print(f"\n🎹 Most Popular Keys:")
            for i, (key, count) in enumerate(top_keys):
                print(f"   {i+1}. {key} (used {count} times)")
        
        # Optimal tempo
        if patterns['optimal_tempos']:
            avg_tempo = np.mean(patterns['optimal_tempos'])
            min_tempo = min(patterns['optimal_tempos'])
            max_tempo = max(patterns['optimal_tempos'])
            print(f"\n⏱️  Tempo Analysis:")
            print(f"   Average: {avg_tempo:.0f} BPM")
            print(f"   Range: {min_tempo:.0f} - {max_tempo:.0f} BPM")
        
        # Viral elements analysis
        if patterns['viral_elements']:
            print(f"\n🔥 Viral Elements Analysis:")
            for element, stats in patterns['viral_elements'].items():
                if isinstance(stats, dict) and 'mean' in stats:
                    print(f"   {element.replace('_', ' ').title()}: {stats['mean']:.2f}")
        
        # Song structure patterns
        if patterns['structure_patterns']:
            top_structures = patterns['structure_patterns'].most_common(3)
            print(f"\n🏗️  Popular Song Structures:")
            for i, (structure, count) in enumerate(top_structures):
                structure_str = ' → '.join(structure)
                print(f"   {i+1}. {structure_str} (used {count} times)")
        
        # Melody patterns
        if patterns['melody_patterns']:
            print(f"\n🎵 Learned {len(patterns['melody_patterns'])} unique melody patterns")
        
        # Rhythm patterns
        if patterns['rhythm_patterns']:
            print(f"🥁 Learned {len(patterns['rhythm_patterns'])} unique rhythm patterns")
        
        # Hooks
        if patterns['hooks']:
            print(f"🎣 Identified {len(patterns['hooks'])} catchy hooks")
            
    except Exception as e:
        print(f"❌ Error displaying insights: {e}")

def generate_viral_song_from_patterns(patterns):
    """Generate a complete viral song using learned patterns"""
    try:
        print("🎼 Composing viral song...")
        
        # Select best patterns
        top_chord_prog = patterns['chord_progressions'].most_common(1)[0][0] if patterns['chord_progressions'] else ('C', 'G', 'Am', 'F')
        top_melody = patterns['melody_patterns'].most_common(1)[0][0] if patterns['melody_patterns'] else (0, 2, -1, 3)
        popular_key = patterns['popular_keys'].most_common(1)[0][0] if patterns['popular_keys'] else "C major"
        optimal_tempo = int(np.mean(patterns['optimal_tempos'])) if patterns['optimal_tempos'] else 120
        
        # Create MIDI file
        midi_file = MIDIFile(4)  # 4 tracks
        
        # Track 0: Melody
        midi_file.addTrackName(0, 0, "Viral Melody")
        midi_file.addTempo(0, 0, optimal_tempo)
        
        # Track 1: Harmony
        midi_file.addTrackName(1, 0, "Viral Harmony")
        
        # Track 2: Bass
        midi_file.addTrackName(2, 0, "Viral Bass")
        
        # Track 3: Drums
        midi_file.addTrackName(3, 0, "Viral Drums")
        
        # Generate melody based on learned patterns
        generate_melody_track(midi_file, top_melody, 0)
        
        # Generate harmony based on chord progression
        generate_harmony_track(midi_file, top_chord_prog, 1)
        
        # Generate bass line
        generate_bass_track(midi_file, top_chord_prog, 2)
        
        # Generate drums
        generate_drums_track(midi_file, 3)
        
        # Save the file
        with open(OUTPUT_MIDI, 'wb') as output_file:
            midi_file.writeFile(output_file)
        
        song_info = {
            'chord_progression': top_chord_prog,
            'key': popular_key,
            'tempo': optimal_tempo,
            'melody_pattern': top_melody,
            'file_path': OUTPUT_MIDI
        }
        
        return song_info
        
    except Exception as e:
        print(f"❌ Error generating song: {e}")
        return None

def generate_melody_track(midi_file, melody_pattern, track):
    """Generate melody track using learned patterns"""
    channel = 0
    time = 0
    base_pitch = 60  # C4
    
    # Repeat pattern to create full melody
    for section in range(4):  # 4 sections
        current_pitch = base_pitch + (section * 2)  # Slight variation per section
        
        for rep in range(2):  # Repeat each pattern twice
            for interval in melody_pattern:
                if isinstance(interval, (int, float)) and abs(interval) <= 12:
                    current_pitch += int(interval)
                    current_pitch = max(48, min(84, current_pitch))
                    
                    duration = random.choice([0.5, 1.0, 1.5])
                    velocity = random.randint(80, 100)
                    
                    midi_file.addNote(track, channel, current_pitch, time, duration, velocity)
                    time += duration

def generate_harmony_track(midi_file, chord_progression, track):
    """Generate harmony track using learned chord progressions"""
    channel = 1
    time = 0
    
    # Chord mappings
    chord_map = {
        'C': [60, 64, 67], 'G': [67, 71, 74], 'Am': [57, 60, 64], 'F': [65, 69, 72],
        'Dm': [62, 65, 69], 'Em': [64, 67, 71], 'D': [62, 66, 69], 'E': [64, 68, 71]
    }
    
    # Generate chord progression
    for section in range(8):  # 8 sections
        for chord_name in chord_progression:
            chord_name_clean = str(chord_name).replace('(', '').replace(')', '').replace("'", "").replace(',', '').split()[0]
            chord_pitches = chord_map.get(chord_name_clean, [60, 64, 67])
            
            # Add chord notes
            for pitch in chord_pitches:
                midi_file.addNote(track, channel, pitch, time, 2.0, 70)
            
            time += 2.0

def generate_bass_track(midi_file, chord_progression, track):
    """Generate bass track"""
    channel = 2
    time = 0
    
    # Root notes for chords
    root_map = {
        'C': 36, 'G': 43, 'Am': 33, 'F': 41, 'Dm': 38, 'Em': 40, 'D': 38, 'E': 40
    }
    
    for section in range(8):
        for chord_name in chord_progression:
            chord_name_clean = str(chord_name).replace('(', '').replace(')', '').replace("'", "").replace(',', '').split()[0]
            root_pitch = root_map.get(chord_name_clean, 36)
            
            # Simple bass pattern
            bass_notes = [root_pitch, root_pitch, root_pitch + 7, root_pitch]
            
            for i, pitch in enumerate(bass_notes):
                midi_file.addNote(track, channel, pitch, time + (i * 0.5), 0.5, 90)
            
            time += 2.0

def generate_drums_track(midi_file, track):
    """Generate drums track"""
    channel = 9  # Drum channel
    time = 0
    
    # Drum sounds
    kick = 36
    snare = 38
    hihat = 42
    
    # Generate 32 bars of drums
    for bar in range(32):
        for beat in range(16):
            beat_time = time + (beat * 0.25)
            
            # Kick on 1 and 3
            if beat % 8 == 0 or beat % 8 == 6:
                midi_file.addNote(track, channel, kick, beat_time, 0.25, 100)
            
            # Snare on 2 and 4
            if beat % 8 == 4:
                midi_file.addNote(track, channel, snare, beat_time, 0.25, 90)
            
            # Hi-hat on off-beats
            if beat % 2 == 1:
                midi_file.addNote(track, channel, hihat, beat_time, 0.125, 60)
        
        time += 4.0

def display_song_info(song_info):
    """Display information about the generated song"""
    print("\n🎵 GENERATED VIRAL SONG INFO:")
    print("════════════════════════════════════")
    
    if 'prompt_elements' in song_info:
        # Enhanced display for prompt-generated songs
        elements = song_info['prompt_elements']
        print(f"🎼 Genre: {elements['genre'].title()}")
        print(f"😊 Vibe: {elements['vibe'].title()}")
        print(f"🎹 Key: {song_info['key']}")
        print(f"⏱️  Tempo: {song_info['tempo']} BPM ({elements['tempo_category']})")
        print(f"🎵 Chord Progression: {' → '.join(str(chord) for chord in song_info['chord_progression'])}")
        print(f"🔥 Catchiness Level: {song_info['catchiness_level']}/10")
        print(f"🏗️  Structure: {' → '.join(elements['structure'])}")
        print(f"💾 File: {song_info['file_path']}")
    else:
        # Original display for MIDI analysis songs
        print(f"🎼 Chord Progression: {' → '.join(str(chord) for chord in song_info['chord_progression'])}")
        print(f"🎹 Key: {song_info['key']}")
        print(f"⏱️  Tempo: {song_info['tempo']} BPM")
        print(f"🎵 Melody Pattern: {song_info['melody_pattern']}")
        print(f"💾 File: {song_info['file_path']}")
    
    print("════════════════════════════════════")

if __name__ == "__main__":
    main()