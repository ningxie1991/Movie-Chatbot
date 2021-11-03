
# Examples of wh_pattern:
#
# Who is [the director] of the [Batman] movie?
# What is [the name of the lead actor] in the movie [Catch Me If You Can]?
# Which is [the main character] of the [Avengers] movie?
# Where is [the film location] of the [Iron Man] movie?
# Who is the actor for Tony Stark?
# Which character did Robert Downy Jr play in the Avengers movie?
wh_pattern = "(?:Who |What |Which |Where )(?:is |are |was |were )(.*)(?: in| of| from| for)(?: the)?(?: movie)?(?: character)? {}(?: movie)?(?:\?)"

main_actor_character_pattern = 'main actor|lead actor|main character|lead character'