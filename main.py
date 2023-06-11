# Import Module
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tkinter import *
import tkinter.messagebox

# Load movie data from CSV file
df = pd.read_csv('movies.csv')

#Iniatilise DF
df["combined_features"]=''

# Clean and preprocess the data (if needed)
df.fillna('', inplace=True)

def getCriteria():
    try:
        if var1.get()==1:
            df["combined_features"] += ' ' + df['genres']
        if var2.get()==1:
            df["combined_features"] += ' ' + df['cast']
        if var3.get()==1:
            df["combined_features"] += ' ' + df['director']
        if var4.get()==1:
            df["combined_features"] += ' ' + df['writers']
        if var5.get()==1:
            df["combined_features"] += ' ' + df['year'].astype(str)
        if var6.get()==1:
            df["combined_features"] += ' ' + df['rating'].astype(str)
        if var7.get()==1:
            df["combined_features"] += ' ' + df['runtime'].astype(str)
        getRecc()
    except ValueError as ve:
        tkinter.messagebox.showinfo("ERROR", ve)
    except TypeError as te:
        tkinter.messagebox.showinfo("ERROR", te)
    except IndexError as ie:
        tkinter.messagebox.showinfo("ERROR", ie)

def getRecc():
    count_vectorizer = CountVectorizer()
    features = count_vectorizer.fit_transform(df['combined_features'])

    # Calculate the cosine similarity matrix
    cosine_sim = cosine_similarity(features)

    recommend_movies(movie_name.get(), int(recc_no.get()), cosine_sim)

def recommend_movies(movie_title, num_recommendations, cosine_sim):
    # Get the index of the movie with the given title
    movie_index = df[df['title'] == movie_title].index[0]

    # Get the pairwise similarity scores of the movie with others
    movie_scores = list(enumerate(cosine_sim[movie_index]))

    # Sort the movies based on the similarity scores
    sorted_movies = sorted(movie_scores, key=lambda x: x[1], reverse=True)

    # Get the top recommendations (excluding the input movie itself)
    top_movies = sorted_movies[1:num_recommendations + 1]

    # Retrieve the recommended movie titles
    recommended_titles = [df.iloc[movie[0]]['title'] for movie in top_movies]
    display(recommended_titles)

    #for testing purpose
    print(f"Recommended {num_recommendations} movies similar to '{movie_title}':")
    print(recommended_titles)

def display(titles):
    top = Toplevel(root)
    top.geometry("500x250")
    top.title("Recommendations")
    listbox = Listbox(top, height=12)  
    temp=1
    for x in titles:
        listbox.insert(temp, str(temp) + ". " + x)
        temp+=1

    listbox.pack(fill=X)
    button = Button(top, text="Dismiss", command=top.destroy)
    button.pack()

# create root window
root = Tk()

# root window title and dimension
root.title("Movie Recommendation Portal")
# Set geometry(widthxheight)
root.geometry("300x350")

frame_a = Frame()
frame_a.pack()


# adding a label to the root window
lbl = Label(master=frame_a, text = "Enter Movie Name:")
lbl.grid(column=0, row=0, sticky='W')

# adding Entry Field
movie_name = Entry(master=frame_a, width=10)
movie_name.grid(column=1, row=0)

lbl2 = Label(master=frame_a, text = "No. of Recommendations:")
lbl2.grid(column=0, row=1, sticky='W')

recc_no = Entry(master=frame_a, width=10)
recc_no.grid(column =1, row =1)


# Create a LabelFrame
frame = LabelFrame(root, text="Select the criteria:", padx=20, pady=20)
frame.pack(pady=20, padx=10)

var1 = IntVar()
var2 = IntVar()
var3 = IntVar()
var4 = IntVar()
var5 = IntVar()
var6 = IntVar()
var7 = IntVar()

# Create four checkbuttons inside the frame
C1 = Checkbutton(frame, text="Genre", variable=var1, onvalue=1, offvalue=0, width=200, anchor="w").pack()

C2 = Checkbutton(frame, text = "Cast", variable=var2, onvalue=1, offvalue=0, width=200, anchor="w").pack()

C3 = Checkbutton(frame, text = "Director", variable=var3, onvalue=1, offvalue=0, width=200, anchor="w").pack()

C4 = Checkbutton(frame, text = "Writer", variable=var4, onvalue=1, offvalue=0, width=200, anchor="w").pack()
"""
C5 = Checkbutton(frame, text = "Year", variable=var5, onvalue=1, offvalue=0, width=200, anchor="w").pack()

C6 = Checkbutton(frame, text = "Rating", variable=var6, onvalue=1, offvalue=0, width=200, anchor="w").pack()

C7 = Checkbutton(frame, text = "Runtime", variable=var7, onvalue=1, offvalue=0, width=200, anchor="w").pack()
"""
getRec = Button(root, text = "Submit" , command=getCriteria).pack()

# Execute Tkinter
root.mainloop()