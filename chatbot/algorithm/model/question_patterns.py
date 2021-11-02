
# Examples of wh_pattern:
#
# Who is [the director] of the [Batman] movie?
# What is [the name of the lead actor] in the movie [Catch Me If You Can]?
# Which is [the main character] of the [Avengers] movie?
# Where is [the film location] of the [Iron Man] movie?
# Who is the actor for Tony Stark?
# Which character did Robert Downy Jr play in the Avengers movie?
wh_pattern = "(?:Who |What |Which |Where )(?:is |are |was |were )(.*)(?: in| of| from| for)(?: the)?(?: movie)? {}(?: movie)?(?:\?)"


# title = entities.loc[entities["Tag"] == 'TITLE', 'Entity'].values[0]
# director = entities.loc[entities["Tag"] == 'DIRECTOR', 'Entity'].values[0]
# actor = entities.loc[entities["Tag"] == 'ACTOR', 'Entity'].values[0]
# character = entities.loc[entities["Tag"] == 'CHARACTER', 'Entity'].values[0]
# relation = ""
# if bos['POS'].iloc[0] in self.wh_pos:
#     if title:
#         pattern = wh_pattern.format(title)
#     elif character:
#         pattern = wh_pattern.format(character)
#     relation = re.match(pattern, sentence).group(1)