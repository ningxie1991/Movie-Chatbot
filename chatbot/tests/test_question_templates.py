from chatbot.algorithm.model.query_templates import QuestionTemplates

qt = QuestionTemplates()

director_query = qt.generate_query('Batman', 'http://www.wikidata.org/prop/direct/P57')
print("\n------- Find director for movie: ------\n{}".format(director_query))

# actor_query = qt.title_related_query('Batman', 'actor')
# print("\n------- Find actor for movie ------\n{}".format(actor_query))
#
# character_query = qt.title_related_query('Batman', 'character')
# print("\n------- Find character for movie ------\n{}".format(character_query))
#
# movies_query = qt.director_related_query('Tim Burton', 'movies')
# print("\n------- Find movies for director ------\n{}".format(movies_query))
#
# movies_query_2 = qt.actor_related_query('Robert Downey Jr', 'movies')
# print("\n------- Find movies for actor ------\n{}".format(movies_query_2))
#
# character_query_2 = qt.actor_related_query('Robert Downey Jr', 'character')
# print("\n------- Find characters for actor ------\n{}".format(character_query_2))
#
# movies_query_3 = qt.character_related_query('Tony Stark', 'movies')
# print("\n------- Find movies for character ------\n{}".format(movies_query_3))
#
# actor_query_2 = qt.character_related_query('Tony Stark', 'actor')
# print("\n------- Find actor for character ------\n{}".format(actor_query_2))
#
# find_character_query = qt.find_movie_character_for_actor_query("Iron Man", "Robert Downey Jr")
# print("\n------- Find movie character for actor ------\n{}".format(find_character_query))
#
# find_actor_query = qt.find_actor_for_movie_character_query("Iron Man", "Tony Stark")
# print("\n------- Find actor for movie character ------\n{}".format(find_actor_query))