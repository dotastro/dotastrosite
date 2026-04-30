import markovify

with open("clickbait.txt") as f:
    clicktext = f.read()
titles_model = markovify.NewlineText(clicktext, state_size=1)
    
# Print five randomly-generated sentences
for i in range(10):
    print(titles_model.make_sentence())