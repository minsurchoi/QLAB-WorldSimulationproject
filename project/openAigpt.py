from openai import OpenAI
client = OpenAI(
    api_key = ""
)

completion = client.chat.completions.create(
  model="gpt-4o",
  temperature=0,
  top_p=0,
  messages=[
    {"role": "system", "content": "You are a database holding import and export data or every major city in the world."},
    {"role": "system", "content": "You are only to return JSONs."},
    {"role": "user", "content": """Give me a sample record of Berlin's imports in tons for the year 2020, for 
1. Animals & Animal Products
2. Vegetable Products
3. Animal or Vegetable Fats and Oils and their Cleavage Products; Prepared Edible Fats; Animal or Vegetable Waxes
4. Prepared Foodstuffs; Beverages, Spirits, Vinegar, Tobacco and Manufactured Tobacco Substitutes
5. Mineral Products
6. Products of the Chemical or Allied Industries
7. Plastics and Articles thereof; Rubber and Articles thereof
8.Raw Hides and Skins, Leather, Furskins, and Articles thereof; Saddlery and Harness; Travel Goods, Handbags, and Similar Containers; Articles of Animal Gut (Other than Silk-worm Gut)
9.Wood and Articles of Wood; Wood Charcoal; Cork and Articles of Cork; Manufactures of Straw, of Esparto or of Other Plaiting Materials; Basketware and Wickerwork
10.Pulp of Wood or of Other Fibrous Cellulosic Material; Recovered (Waste and Scrap) Paper or Paperboard; Paper and Paperboard and Articles thereof
11.Textiles and Textile Articles
12.Footwear, Headgear, Umbrellas, Sun Umbrellas, Walking-sticks, Seat-sticks, Whips, Riding-crops, and Parts thereof; Prepared Feathers and Articles Made therewith; Artificial Flowers; Articles of Human Hair
13.Articles of Stone, Plaster, Cement, Asbestos, Mica or Similar Materials; Ceramic Products; Glass and Glassware
14.Natural or Cultured Pearls, Precious or Semi-precious Stones, Precious Metals, Metals Clad with Precious Metal, and Articles thereof; Imitation Jewellery; Coin
15.Base Metals and Articles of Base Metal
16.Machinery and Mechanical Appliances; Electrical Equipment; Parts thereof; Sound Recorders and Reproducers, Television Image and Sound Recorders and Reproducers, and Parts and Accessories of such Articles
17.Vehicles, Aircraft, Vessels, and Associated Transport Equipment
18.Optical, Photographic, Cinematographic, Measuring, Checking, Precision, Medical or Surgical Instruments and Apparatus; Clocks and Watches; Musical Instruments; Parts and Accessories thereof
19.Arms and Ammunition; Parts and Accessories thereof
20.Miscellaneous Manufactured Articles
21.Works of Art, Collectors' Pieces and Antiques"""}
  ]
)

print(completion.choices[0].message)


