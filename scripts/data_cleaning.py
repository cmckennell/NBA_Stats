import pandas as pd

# Load the data
df = pd.read_csv('data/raw/vgchartz-2024.csv')

"""
Column Descriptions:
img : URL slug for the box art at vgchartz.com
title : Game title
console : Console the game was released for
genre : Genre of the game
publisher : Publisher of the game
developer: Developer of the game
critic_score: Metacritic score (out of 10)
total_sales : Global sales of copies in millions
na_sales : North American sales of copies in millions
jp_sales : Japanese sales of copies in millions
pal_sales : European & African sales of copies in millions
other_sales : Rest of world sales of copies in millions
release_date : Date the game was released on
last_update : Date the data was last updated
"""

# Drop the img column
df = df.drop(columns=['img'])
print(df.info())