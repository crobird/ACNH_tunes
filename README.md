# ACNH_tunes
Play animal crossing town tunes in your terminal.

# Requirements
Dependencies are listed in requirements.txt and can be installed with `pip install -r requirements.txt`.

# Town tune format
The scale for tunes goes from a low G up over an octave to a high E. As you may know, there are no accidentals (sharps or flats) playable for town tunes. Lower versions of notes are declared with lowercase letters and upper versions of notes will use uppercase letters. So the scale low-to-high is: `gabcdefGABCDE`.

In addition to these letters, an `x` designates a rest, where no note is played for that duration. And a `-` character will extend the previous note's duration.

Here are a couple of examples:

```
TMBG - Ana Ng: GGG-deG-ddd-c-b-
Gravity Falls theme: fffAAGFxAAAGAGf
```

# Usage

## Specify the tune directly
`./play_tune.py -t fffAAGFxAAAGAGf`

## From a file
`./play_tune.py -f sample.tune`

## Or leave blank for interactive mode
In this mode, there are a few preset tunes you can play, or you can type the text for the tune and iterate on it as you tweak things.

## More help provided with -h
Use the -h help flag and see how to change the default note value, the volume, and how to dump out the note information being played. It's not that I'm trying to be cagey, but it's all in the help docs and I don't want to type it all again.

# Misc
- There's no enforcement on tune length, so beware making something that's too long and won't work when you talk to Isabelle.