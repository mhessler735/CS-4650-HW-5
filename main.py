# import libraries
import spacy
from newsapi.newsapi_client import NewsApiClient
import pandas as pd
from collections import Counter
from string import punctuation
from wordcloud import WordCloud
import matplotlib.pyplot as plt

nlp_eng = spacy.load('en_core_web_lg')
newsapi = NewsApiClient(api_key='f413cad50d644bc3a323881e49b648fe')  # API key is available at https://newsapi.org/


def getArticles(x):

    data = newsapi.get_everything(q='coronavirus', language='en', from_param='2022-02-28', to='2022-03-27',
                              sort_by='relevancy', page_size =20)
    return data


articles = list(map(getArticles, range(1, 6)))

dados = []

for i, article in enumerate(articles):
    for x in article['articles']:
        title = x['title']
        description = x['description']
        content = x['content']
        dados.append({'title': title, 'desc': description, 'content': content})

df = pd.DataFrame(dados)
df = df.dropna()
df.head()

results = []

def get_keywords_eng(text):
    result = []
    pos_tag = ['PROPN', 'VERB', 'NOUN']
    doc = nlp_eng(text.lower())
    for token in doc:
        if token.text in nlp_eng.Defaults.stop_words or token.text in punctuation:
            continue
        if token.pos_ in pos_tag:
            result.append(token.text)
    #print(result)
    return result


for content in df.content.values:
    results.append([('#' + x[0]) for x in Counter(get_keywords_eng(content)).most_common(5)])

df['keywords'] = results

print(df)
df.to_excel('output.xlsx', index=True)
text = ''
for x in results:
    for y in x:
        text += " " + y

wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="black", collocations = False).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()