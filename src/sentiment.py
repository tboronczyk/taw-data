import re
import matplotlib.pyplot as plt
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

character = 'DATA'
filename = 'TNG-5x11.txt'

with open(filename, 'r') as fp:
    script = fp.readlines()

episode = script[1]
script = script[3:]

# extraxt character's lines, accounting for (VO) etc.
p = re.compile(f'^{character}( \([^\)]+\))?:')

lines = []
for ln in script:
    if p.match(ln):
        i = ln.find(':') + 1
        lines.append(ln[i:].strip())
del script

# remove stage directions from dialog (parenthesized text)
p = re.compile('\([^)]+\) ?')
lines = [p.sub('', ln) for ln in lines]

analyzer = SentimentIntensityAnalyzer()
y = [analyzer.polarity_scores(ln)['compound'] for ln in lines]

def display_dialog(evt):
    i = round(evt.xdata)
    if (i >= 0 and i < len(lines)):
        print(i, y[i], lines[i], "\n")

fig, ax = plt.subplots()
fig.canvas.mpl_connect('button_press_event', display_dialog)

ax.plot(y)
ax.set_xlabel('Dialog')
ax.set_ylabel('Sentiment')

plt.title(f'Sentiment for {character} in episode {episode}')
plt.ylim([-1, 1])
plt.show()
