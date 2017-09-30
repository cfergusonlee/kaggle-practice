import pandas as pd
fight_urls = pd.read_csv('fight urls.csv', encoding='utf-8')['link'].values.tolist()
print len(fight_urls)