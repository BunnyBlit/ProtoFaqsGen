# GameFAQs Generation Prototype

So, what do we have here? This is a quick and dirty text generation prototype for generating a guide in the style of GameFAQs for a game that doesn't exist. The game is represented by a directed graph, and we generate text by traversing the graph, generating paragraphs of text as we go. Woo.

## Graphs

A sample graph in the dot language is provided in `./data/sample.dot`. The node labels are structured as `[type]_[name]_[attribute]`, so `Weap_Flambridge_Fire` is a weapon node, named flambridge with the fire attribute and `Town_Littledom` is a town node with the name of Littledom.

## To Use
I used conda for dependency management because the original notebook used ASP (and by extension, clingo), but venv should also work just fine. Create a virtual environment however you like to do that, for example:
```
$ python -m venv .venv
$ source .venv/bin/activate
```
Install requirements:
```
(.venv) $ pip install -r requirements.txt
```
And then the CLI is pretty simple:
```
(.venv) $ python3 generate.py -f ./data/sample.dot
```

There's also a -h flag for help.

## Other stuff
Notes.md has some scribbles mostly written to myself, you may or may not find them legible or useful.