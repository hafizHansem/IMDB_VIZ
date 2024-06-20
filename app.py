import pandas as pd
import plotly.express as px
import streamlit as st

# Set title of the Streamlit app
st.title('Analisis Film Berdasarkan Pendapatan Kotor, Distributor, dan Genre')

# Path to CSV file
file_path = 'IMBD_movie_data.csv'

# Read CSV file
df = pd.read_csv(file_path)

# Rename columns for consistency
df.columns = ['Title', 'Rating', 'Genre', 'Release Date', 'Production Company', 'Budget', 'Gross Worldwide']

# Replace missing values
df['Gross Worldwide'].replace('Gross worldwide not found', pd.NA, inplace=True)
df['Budget'].replace('Budget not found', pd.NA, inplace=True)
df['Release Date'].replace('Release date not found.', pd.NA, inplace=True)
df['Production Company'].replace('Production company not found.', pd.NA, inplace=True)

# Convert columns to appropriate data types
df['Gross Worldwide'] = pd.to_numeric(df['Gross Worldwide'], errors='coerce')
df['Budget'] = pd.to_numeric(df['Budget'], errors='coerce')

# Calculate median values for replacement
median_gross_worldwide = df['Gross Worldwide'].median()
median_budget = df['Budget'].median()

# Replace missing numeric values with median
df['Gross Worldwide'].fillna(median_gross_worldwide, inplace=True)
df['Budget'].fillna(median_budget, inplace=True)

# Replace missing string values with a placeholder
df['Release Date'].fillna('Unknown', inplace=True)
df['Production Company'].fillna('Unknown', inplace=True)

# Display the dataframe after filling missing values
st.write("Dataframe after preprocessing:", df)

# Pisahkan genre menjadi baris terpisah
df_genre = df.set_index(['Title', 'Gross Worldwide', 'Production Company']).Genre.str.split(', ', expand=True).stack().reset_index(name='Genre').drop('level_3', axis=1)

# Sidebar for user selection
st.sidebar.header('Filter')
selected_genre = st.sidebar.multiselect('Pilih Genre', df_genre['Genre'].unique())
selected_distributor = st.sidebar.multiselect('Pilih Production Company', df['Production Company'].unique())

# Filter data based on selection
filtered_df_genre = df_genre
filtered_df = df

if selected_genre:
    filtered_df_genre = df_genre[df_genre['Genre'].isin(selected_genre)]
if selected_distributor:
    filtered_df = df[df['Production Company'].isin(selected_distributor)]
    filtered_df_genre = filtered_df_genre[filtered_df_genre['Production Company'].isin(selected_distributor)]

# Plotting
st.subheader('Visualisasi')

# Relation: Scatter plot antara pendapatan kotor dan genre film
st.write("### Pendapatan Kotor berdasarkan Genre dan Production Company")
fig = px.scatter(filtered_df_genre, x='Genre', y='Gross Worldwide', color='Production Company', size='Gross Worldwide', hover_data=['Title'])
st.plotly_chart(fig)
st.write("Grafik ini memperlihatkan bagaimana pendapatan kotor film-film berbeda-beda berdasarkan genre dan production company. Anda dapat melihat distribusi dan pola umum di antara kombinasi genre dan production company tertentu.")
st.write("Kesimpulan: Dalam 5 tahun terakhir ini ditunjukan, bahwa ada distributor dengan pendapatan tertinggi dengan membawa nama besar seperti godzilla x kong, ini membuktikan nama besar sebuah franchise juga punya pengaruh pada pendapatan kotor. Padahal saya juga tidak pernah mendengar nama production company ini yaitu Legendary pictures. disusul dengan film bergenre documenter dan music dari perusahaan yang belum pernah saya dengar juga, dan yang selanjutnya ialah columbia pictures dengan seri bad boy nya. memang kemungkinan, nama besar juga akan memberikan pengaruh daya tarik kepada penonton yang nanti nya akan memberikan pendapatan yang lebih")

# Comparison: Bar chart yang menunjukkan rata-rata pendapatan kotor untuk setiap genre film
st.write("### Rata-rata Pendapatan Kotor untuk Setiap Genre")
avg_gross_per_genre = filtered_df_genre.groupby('Genre')['Gross Worldwide'].mean().reset_index()
fig = px.bar(avg_gross_per_genre, x='Genre', y='Gross Worldwide', color='Genre')
st.plotly_chart(fig)
st.write("Grafik ini menunjukkan rata-rata pendapatan kotor untuk setiap genre film. Hal ini membantu untuk memahami genre mana yang cenderung memberikan pendapatan lebih tinggi secara keseluruhan.")
st.write("Kesimpulan:di lima tahun terakhir ini, genre film dengan pendapatan kotor terbanyak ialah genre fantasy,action dan adventure. Genre fantasy memberikan pendapatan yang fantastis ketimbang genre lainya ($80m). ini bisa memberikan gambaran, bahwa genre yang akan menarik banyak peminat dari penonton dan bagi pembuat film, ini akan menjadi insight yang penting dalam memasukan unsur genre yang sedang diminati 5 tahun terakhir ini.")

# Distribution: Histogram yang menunjukkan distribusi pendapatan kotor film-film
st.write("### Distribusi Pendapatan Kotor Film-film")
fig = px.histogram(filtered_df, x='Gross Worldwide', nbins=20, marginal='box', hover_data=['Title'])
st.plotly_chart(fig)
st.write("Histogram ini menggambarkan distribusi pendapatan kotor film-film. Dengan melihat distribusi ini, Anda dapat mengidentifikasi apakah terdapat outlier atau pola distribusi yang menarik.")
st.write("Kesimpulan:Ini menunjukan bahwa banyak genre film yang hanya mendapatkan keuntungan minim, dan ada sedikit fil yang mempunyai pendapatan yang tinggi. mungkin, pendapatan kotor dipengaruhi juga dengan kualitas, momentum, dan lain lain. jadi, ini akan memberikan insight yang tepat bagaimana sedikit film itu bisa memenangkan persaingan.")

# Composition: Pie chart yang menunjukkan komposisi genre film-film
st.write("### Komposisi Genre Film-film")
genre_counts = filtered_df_genre['Genre'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'Count']
fig = px.pie(genre_counts, names='Genre', values='Count', title='Komposisi Genre Film-film')
st.plotly_chart(fig)
st.write("Diagram pie ini memberikan gambaran tentang komposisi genre film-film dalam dataset. Hal ini berguna untuk melihat seberapa besar proporsi setiap genre dalam keseluruhan dataset yang Anda analisis.")
st.write("Kesimpulan: Di komposisi genre film, malah drama yang mendominasi lima tahun terakhir ini, padahal genre ini tidak pernah masuk 5 jenis genre yang memiliki pendapatan yang banyak. disusul dengan action, adventure, comedy. Mungkin genre drama melakukan strategy, quantity over quality karena berbanding terbalik dengan jumlah pendapatan. jika genre action, comedy, dan adventure dalam 5 tahun ini, yang merajai adalah yang membawa nama besar dari franchise atau seri yang sudah populer dari dulu")
