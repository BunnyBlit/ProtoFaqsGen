""" Module of various tracery grammars. We probably want some representation that also
    requires less mental overhead to remember what symbols need to be added at runtime before
    the grammar becomes valid, but this works for now.
"""
# gotta augment this with town and weap rules
town_weap_grammar = {
    'origin': ["#townTitle#\n\n#shopDirections#\n#aquireItem#"],
    'townTitle': ["!!!!!!!!!!!#town#!!!!!!!!!!!", "**********#town#**********", "><><><><><#town#><><><><><"],
    'town':[],
    'weap':[],
    'shopDirections': ["Head #screens# #direction#, past the #landmark# to get to the shop"],
    'screens': ["one", "two", "three"],
    'direction': ["north", "south", "east", "west"],
    'landmark': ["fountain", "statue", "big house", "castle"],
    'aquireItem': ["Go grab #weap#", "Buy #weap#", "Pick up #weap#, you'll want it for later"]
}

#gotta gument this with town and arm rules
town_arm_grammar = {
    'origin': ["#townTitle#\n\n#shopDirections#\n#aquireItem#"],
    'townTitle': ["!!!!!!!!!!!#town#!!!!!!!!!!!", "**********#town#**********", "><><><><><#town#><><><><><"],
    'town':[],
    'arm':[],
    'shopDirections': ["Head #screens# #direction#, past the #landmark# to get to the shop"],
    'screens': ["one", "two", "three"],
    'direction': ["north", "south", "east", "west"],
    'landmark': ["fountain", "statue", "big house", "castle"],
    'aquireItem': ["Go grab #arm#", "Buy #arm#", "Pick up #arm#, you'll want it for later"] 
}

# augment this grammar with weapon, dungeon and town rules
weap_dun_grammar = {
    'origin': ["#worldMapTitle#\n\n#worldDirections#"],
    'worldMapTitle': ["!!!!!!!!!!!World Map!!!!!!!!!!!", "**********World Map**********", "><><><><><World Map><><><><><"],
    'weap':[],
    'dun':[],
    'town': [],
    'worldDirections': ["#weapMention#Head #direction# from #town# past the #worldFeature# to get to #dun#"],
    'weapMention': ["After getting #weap#, leave #town#. ", ""],
    'direction': ["north", "south", "east", "west"],
    'worldFeature': ["mountains", "swamps", "glacier", "volcano"]
}

# augment this grammar with armor, dungeon and town rules
arm_dun_grammar = {
    'origin': ["#worldMapTitle#\n\n#worldDirections#"],
    'worldMapTitle': ["!!!!!!!!!!!World Map!!!!!!!!!!!", "**********World Map**********", "><><><><><World Map><><><><><"],
    'arm':[],
    'dun':[],
    'town': [],
    'worldDirections': ["#armMention#Head #direction# from #town# past the #worldFeature# to get to #dun#"],
    'armMention': ["After getting #arm#, leave #town#. ", ""],
    'direction': ["north", "south", "east", "west"],
    'worldFeature': ["mountains", "swamps", "glacier", "volcano"] 
}

# augment this grammar with dungeon, boss, weapon and elem rules
dun_boss_weap_grammar = {
    'origin': ["#dungeonTitle#\n#dungeonDirections#\n#bossPrep#\n#bossDirections#"],
    'dungeonTitle':["!!!!!!!!!!!#dun#!!!!!!!!!!!", "**********#dun#**********", "><><><><><#dun#><><><><><"],
    'dungeonDirections':["Proceed through all the levels of #dun#, the bottom floor is your target-- #boss#",
                         "#dun# is really small, the boss is right at the start! Make sure to prepare before going in",
                         "This is a frustrating one, the water level management sucks. But keep at it, until you get to the room with #boss#"],
    'bossPrep':["Make sure to equip #weap#, #boss# is weak to it's #elem# damage", "You'll have a bad time unless you equip #weap#. It makes the #boss# fight a breeze."],
    'bossDirections':["Just keep attacking-- #weap#'ll get it done in no time",
                      "The #boss#'s sleep attacks are really annoying, but keep your #weap# holder awake and you'll clear eventually",
                      "The #boss#'s instant death attacks are trash, spam some revives to keep #weap# holder swinging"],
    'dun':[],
    'weap':[],
    'boss':[],
    'elem':[]
}

# augment this grammar with dungeon, boss, weapon and elem rules
dun_boss_arm_grammar = {
    'origin': ["#dungeonTitle#\n#dungeonDirections#\n#bossPrep#\n#bossDirections#"],
    'dungeonTitle':["!!!!!!!!!!!#dun#!!!!!!!!!!!", "**********#dun#**********", "><><><><><#dun#><><><><><"],
    'dungeonDirections':["Proceed through all the levels of #dun#, the bottom floor is your target-- #boss#",
                         "#dun# is really small, the boss is right at the start! Make sure to prepare before going in",
                         "This is a frustrating one, the water level management sucks. But keep at it, until you get to the room with #boss#"],
    'bossPrep':["Make sure to equip #arm#, #boss#'s #elem# attacks sting without it", "You'll have a bad time unless you equip #arm#. It makes the #boss# fight a breeze."],
    'bossDirections':["#arm#'ll help you with the constant #elem# attacks, stick it out and you'll win",
                      "The rest of your party may bite it, but the character with #arm# should be ok. Power through with them for victory",
                      "Keep defending when the boss prepares an #elem# attack. Withstand the onslaught and you'll get through"],
    'dun':[],
    'arm':[],
    'boss':[],
    'elem':[]
}

# augment this with a key item rule
boss_key_grammar = {
    'origin': ["#keyItemDescription#"],
    'keyItemDescription': ["After a hard fought battle, go to the next room to get #key#", "Watch the extremely cool cutscene, then grab #key# on your way out"],
    'key': []
}

# augment this with key item and town rules
key_town_grammar = {
    'origin': ["#worldMapTitle#\n#nextTownDirections#"],
    'worldMapTitle': ["!!!!!!!!!!!World Map!!!!!!!!!!!", "**********World Map**********", "><><><><><World Map><><><><><"],
    'nextTownDirections': ["Next you'll want to head in #direction# to #town#. You'll need to use #key# at #feature#",
                           "Head #direction# until you can't go any further, then use #key#. #town# will be revealed!"],
    'direction': ["north", "south", "east", "west"],
    'feature': ["mountains", "swamps", "glacier", "volcano"],
    'key': [],
    'town': []
}
