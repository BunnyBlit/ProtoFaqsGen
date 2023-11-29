# Stella's into generating gamefaqs guides and I need portfolio projects so lets fuckin go

Notes:
For the graph side:
	list of locations
		towns
		dungeons	
	boss fights
	key items
	ordering

	start node!
	Prologue
		get characters (fixed party)
	The Game (loop)
		town -> (get upgrades) -> dungeon (kill a boss) -> get key item (unlocks next town)
		there is a boss where you win the game
			end node!

	Tag em!
		— rule based query to tag things
		— weapon elements
		— armor elements
		— boss elemental affinities
			— a weakness
			— output
		— character elemental affinities
			(TODO: physical vs magical)

	Text generation
		— a whole lot of tracery
		— “fill in the blank” vs “dynamic grammars”
			— try and find out
			(TODO: ASCII art, tables)
			(generating tables of random enemies)
			(and other stuff)

## TODO:
- start with some graphs with semantically loaded IDs
- - Char for characters
- - -  each Char node also has an elemental affinity
- - - so "Char_[name]_fire"
- - Town for town
- - "Town_[name]"
- - - each town has a Weap (weapon) or Arm (armor) nodes, which have affinities
- - - "Weap_[name]_ice", "Arm_[name]_wind"
- - Dun for dungeon
- - "Dun_[name]"
- - - dungeons have bosses, which have a weakness
- - - "Boss_[name]_darkness"
- - Key for key item
- - - "Key_[name]"
- - start and end for those nodes

and the general plot is something like
"Char -> Char -> Char -> Town -> Weap -> Dun -> Boss -> Key -> Town..."

The most important kind of text we need to generate is _transition_ text:
*Town -> Weap*: go to the weapon shop in *Town*, and buy *Weap*. You may need to grind on some of the random mobs outside of town, but you'll need it later!
*(Town ->) Weap -> Dun*: After getting *Weap*, head east from *Town* to *Dun*. It's far, but keep going.
*(Weap ->) Dun -> Boss*: explore the five levels of *Dun*. Eventually, you'll run into *Boss*! 
*(Weap -> Dun ->) Boss -> Key*: beat *Boss* by using *Weap*! Once you kill *Boss*, you'll get *Key*.
*Key -> Town*: Now that you have *Key*, you can head north to make it to *Town* 

The other big text generation need is _node names_: character names, town names, weapon names, dungeon names, boss names. The start node probably needs to have preamble data attached, and the end node needs a Congrats!!11!1 bit of text generation.

# Graph generation ideas:
- problems begat solutions: start by picking a list of boss affinities, this tells you exactly what kind of affinities your weapons / armor / characters need. This also gives you your number of bosses, generate boss nodes
- then work backwards, pick a boss order and generate dungeon and key nodes for each boss node, a weapon/armor node for the next boss.
- use towns to fill in the gap between key items and weapons / armor
- characters are last: the "prologue" gets added before the first town node
- well, also add a start / end node in there 
- - optional: embellish boss nodes by adding the missing affinity (output or weakness) to something that comes before in the graph
- - done last so we can also look at character nodes

# Lessons learned from this little prototype:
- we want grammars based on graph edges, which means _edge labeling sure would be nice_
- dot is a great language to slam out a graph real quick, but pydot is designed for visualization, not graph querying
- - networkx might be better at this? I wonder if we can get a networkx graph from a dot... file
- -  we can!
- - pydot's API is the worst
- current way of holding onto context (just a list) ain't it, chief. We probably want some combined object that can, given an edge, run some queries against the graph to pull in the context it needs before grammar expansions
- - a faq generator is
- - - the graph
- - - static graph queries to get context and "fill in the blanks of grammars"
- - -  grammars
- - - you can bake "the information you need to query for" into the dictionary that'll become the grammar. Something like `"_queries": [obj to deserialize, obj to deserialize]` could do it, and then all your authoring is separate from your code (just remove the `_queries` key before expanding)
- - - - something something mutation something something terrible copy operations something something more thinking required
- current prototype requires you to keep a lot in your head, we'd want to formalize a lot of these dictionaries out to dataclasses (or JS equivelent) to get things like sweet, sweet autocompletion
- - there's almost assuredly a better way to set up the data structures here to make adding a new edge type and grammar easy
- - - visitor pattern? or am I high on PL bullshit again
- we're gonna need to write a lot of grammars, but it might not be as bad as I was originally worried about! Each edge grammar needs to be fairly rich, but you can _probably_ capture the vibe in two weeks of dedicated writing