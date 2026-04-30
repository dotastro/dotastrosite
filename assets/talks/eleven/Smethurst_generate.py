import markovify

# Get raw text as string.
with open("drag_queen_names.txt") as f:
    dragtext = f.read()
drag_model = markovify.NewlineText(dragtext, state_size=1)

with open("astro.txt") as f:
    astrotext = f.read()
astro_model = markovify.NewlineText(astrotext, state_size=1)

with open("clickbait.txt") as f:
    clicktext = f.read()
click_model = markovify.NewlineText(clicktext, state_size=1)

with open("rupaul.txt") as f:
    rutext = f.read()
ru_model = markovify.NewlineText(rutext, state_size=1)

with open("abstracts.txt") as f:
    abs_text = f.read()
abs_model = markovify.NewlineText(abs_text, state_size=1)

model_combo = markovify.combine([ click_model, ru_model ], [ 1, 1 ])
    
# Print five randomly-generated sentences
for i in range(10):
    print(ru_model.make_sentence())