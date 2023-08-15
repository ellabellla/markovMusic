# Markov Music

This cli tool generates music using a markov chain and outputs it to a midi port. 

The program uses a midi file to build a markov chain. The markov chain stores the probabilities at each note of what the next note will be. The program then selects a random starting note and randomly chooses the next notes based on the markov chains probabilities. This results in a random walk of notes based on the input song.

## Usage
```
usage: Markov Music [-h] [-l] [-t TRACKS] [-b BPM] filename

Generate Music from midi's

positional arguments:
  filename

options:
  -h, --help            show this help message and exit
  -l, --list
  -t TRACKS, --tracks TRACKS
  -b BPM, --bpm BPM

By Ella Pash
```

## License
This project is under the MIT License. You can view the license [here](./LICENSE).