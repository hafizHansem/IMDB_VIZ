import pandas as pd
import plotly.express as px
import streamlit as st

# Set title of the Streamlit app
st.title('Analisis Film Berdasarkan Pendapatan Kotor, Distributor, dan Genre')

# Path to CSV file
file_path = 'film_data_preprocessed.csv'

# Read CSV file
df = pd.read_csv(file_path)

# Display the dataframe
st.write("Dataframe:", df)

# Pisahkan genre menjadi baris terpisah
df_genre = df.set_index(['Film Name', 'Pendapatan Kotor ($)', 'Distributor']).Genre.str.split(', ', expand=True).stack().reset_index(name='Genre').drop('level_3', axis=1)

# Sidebar for user selection
st.sidebar.header('Filter')
selected_genre = st.sidebar.multiselect('Pilih Genre', df_genre['Genre'].unique())
selected_distributor = st.sidebar.multiselect('Pilih Distributor', df['Distributor'].unique())

# Filter data based on selection
filtered_df_genre = df_genre
filtered_df = df

if selected_genre:
    filtered_df_genre = df_genre[df_genre['Genre'].isin(selected_genre)]
if selected_distributor:
    filtered_df = df[df['Distributor'].isin(selected_distributor)]
    filtered_df_genre = filtered_df_genre[filtered_df_genre['Distributor'].isin(selected_distributor)]

# Plotting
st.subheader('Visualisasi')

# Relation: Scatter plot antara pendapatan kotor dan genre film
st.write("### Pendapatan Kotor berdasarkan Genre dan Distributor")
fig = px.scatter(filtered_df_genre, x='Genre', y='Pendapatan Kotor ($)', color='Distributor', size='Pendapatan Kotor ($)', hover_data=['Film Name'])
st.plotly_chart(fig)
st.write("Grafik ini memperlihatkan bagaimana pendapatan kotor film-film berbeda-beda berdasarkan genre dan distributor. Anda dapat melihat distribusi dan pola umum di antara kombinasi genre dan distributor tertentu.")
st.write("Kesimpulan: bahwa distributor dengan pendapatan tertinggi adalah walt disney dengan film drama,action, adventure dan scifi, dan di susul dengan genre yang sama dari Warner bros.Ini juga menunjukan bahwa jika kita ingin membuat film dengan genre tersebut, kita harus mempelajari dari distributor tersebut. Dari melihat karyanya akan memberikan insight bagaiman mengemas genre tersebut agar memberikan keuntungan yang lebih.")

# Comparison: Bar chart yang menunjukkan rata-rata pendapatan kotor untuk setiap genre film
st.write("### Rata-rata Pendapatan Kotor untuk Setiap Genre")
avg_gross_per_genre = filtered_df_genre.groupby('Genre')['Pendapatan Kotor ($)'].mean().reset_index()
fig = px.bar(avg_gross_per_genre, x='Genre', y='Pendapatan Kotor ($)', color='Genre')
st.plotly_chart(fig)
st.write("Grafik ini menunjukkan rata-rata pendapatan kotor untuk setiap genre film. Hal ini membantu untuk memahami genre mana yang cenderung memberikan pendapatan lebih tinggi secara keseluruhan.")
st.write("Kesimpulan : seperti disinggung di grafik sebelumnya tentang pendapatan kotor dari distributor, tentunya genre yang sedang di geluti oleh distributor tersebut memberikan pendapatan kotor yang tinggi seperti genre adventure,fantasy,scifi,action. Ini menunjukan bahwa masyarakat indonesia sedang menggemari genre genre film tersebut selama 5 tahun terakhir. Ini juga bisa memberikan insight mengenai tema atau genre apa yang kemungkinan besar memberikan keuntungan.")

# Distribution: Histogram yang menunjukkan distribusi pendapatan kotor film-film
st.write("### Distribusi Pendapatan Kotor Film-film")
fig = px.histogram(filtered_df, x='Pendapatan Kotor ($)', nbins=20, marginal='box', hover_data=['Film Name'])
st.plotly_chart(fig)
st.write("Histogram ini menggambarkan distribusi pendapatan kotor film-film. Dengan melihat distribusi ini, Anda dapat mengidentifikasi apakah terdapat outlier atau pola distribusi yang menarik.")
st.write("kesimpulan : Banyak film yang memiliki pendapatan yang relative rendah (menurut interval). Dan hanya sedikit film yang memiliki pendapatan yang tinggi. Ini menunjukan bahwa film yang memiliki pendapatan tinggi memiliki kualitas yang berbeda(kemungkinan) yang benar benar di sukai.")

# Composition: Pie chart yang menunjukkan komposisi genre film-film
st.write("### Komposisi Genre Film-film")
genre_counts = filtered_df_genre['Genre'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'Count']
fig = px.pie(genre_counts, names='Genre', values='Count', title='Komposisi Genre Film-film')
st.plotly_chart(fig)
st.write("Diagram pie ini memberikan gambaran tentang komposisi genre film-film dalam dataset. Hal ini berguna untuk melihat seberapa besar proporsi setiap genre dalam keseluruhan dataset yang Anda analisis.")
st.write("Kesimpulan : Dari komposisi ini, kita bisa mengetahui bahwa ada berapa banyak distributor yang menggeluti genre tersebut dan juga bisa digunakan untuk melihat persaingan di genre yang dituju. Namun kenapa thriller lebih banyak daripada fantasy?, bukan kah dia bukan dari top 4?. Kemungkinan nya, banyak distributor sedang membuka strategi baru atau masuk ke pasar baru yang jernih tanpa persaingan (Blue Ocean Strategy).")
