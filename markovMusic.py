import argparse
from fractions import Fraction
from music21 import *
import random
import mido
import time

def extract_notes(path):
    midiFile = converter.parse(path)
    parts = midiFile.parts.stream()
    extracted_notes = []
    track_names = []
    for part in parts:
        track_names.append(part.partName)
        notes = []
        prev_offset = 0
        for note in part.recurse().notes.stream():
            dur = float(note.duration.quarterLength)
            offset = float(note.offset)
            pits = [(pit.midi, dur, offset-prev_offset) for pit in note.pitches]
            prev_offset = offset
            
            notes.append(pits)
        extracted_notes.append(notes)
    
    return (track_names, extracted_notes)

def generate_chain(extracted_notes, tracks):
    markov_chain = {}
    for track in tracks:
        if track < len(extracted_notes) and track >= 0:
            part = extracted_notes[track]
            
            for i, notes in enumerate(part[1:-1]):
                for note in notes:
                    key = (note[0], note[1])
                    if key not in markov_chain:
                        markov_chain[key] = []
                    markov_chain[key].extend(part[i+1])
                    
    return markov_chain

def play(bpm, markov_chain):
    bps = bpm/60
    
    note = random.choice(list(markov_chain.keys()))
    note = (note[0], note[1], 0)
    port = mido.open_output()
    
    while True:
        time.sleep(note[2]*(1/bps)) # wait offset
        
        port.send(mido.Message('note_on', note=note[0]))
        time.sleep(note[1]*(1/bps)) # wait duration
        port.send(mido.Message('note_off', note=note[0]))
        
        note = random.choice(markov_chain[(note[0], note[1])])

def main():
    parser = argparse.ArgumentParser(
        prog='Markov Music',
        description='Generate Music from midi\'s',
        epilog='By Ella Pash')
    
    parser.add_argument('-l', '--list', default=False, required=False, action='store_true')
    parser.add_argument('-t', '--tracks', default=None, type=str, required=False)
    parser.add_argument('-b', '--bpm', default=100, type=int, required=False)
    parser.add_argument('filename')
    
    args = parser.parse_args()
    try:
        (track_names, notes) = extract_notes(args.filename)
        if args.list:
            for i, track_names in enumerate(track_names):
                print(f"{i}: {track_names}")
            exit()

        tracks = [i for i in range(len(notes))]
        if args.tracks != None:
            tracks = [int(num) for num in args.tracks.split(" ")]

        markov_chain = generate_chain(notes, tracks)
        play(args.bpm, markov_chain)
    except KeyboardInterrupt:
        print("\nExiting")

if __name__ == "__main__":
    main()