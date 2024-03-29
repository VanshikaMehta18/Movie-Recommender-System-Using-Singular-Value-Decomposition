# -*- coding: utf-8 -*-
# Movie Recommendations 
# Import all the required libraries
import numpy as np
import pandas as pd

"""## Reading the Data
Now that we have downloaded the files from the link above and placed them in the same directory as this Jupyter Notebook, we can load each of the tables of data as a CSV into Pandas. Execute the following, provided code.
"""

# Read the dataset from the two files into ratings_data and movies_data
#NOTE: if you are getting a decode error, add "encoding='ISO-8859-1'" as an additional argument
#      to the read_csv function
column_list_ratings = ["UserID", "MovieID", "Ratings","Timestamp"]
ratings_data  = pd.read_csv('ratings.dat',sep='::',names = column_list_ratings, engine='python')
column_list_movies = ["MovieID","Title","Genres"]
movies_data = pd.read_csv('movies.dat',sep = '::',names = column_list_movies, engine='python', encoding = 'latin-1')
column_list_users = ["UserID","Gender","Age","Occupation","Zixp-code"]
user_data = pd.read_csv("users.dat",sep = "::",names = column_list_users, engine='python')

"""`ratings_data`, `movies_data`, `user_data` corresponds to the data loaded from `ratings.dat`, `movies.dat`, and `users.dat` in Pandas.

## Data analysis

We now have all our data in Pandas - however, it's as three separate datasets! To make some more sense out of the data we have, we can use the Pandas `merge` function to combine our component data-frames. Run the following code:
"""

data=pd.merge(pd.merge(ratings_data,user_data),movies_data)
data

"""Next, we can create a pivot table to match the ratings with a given movie title. Using `data.pivot_table`, we can aggregate (using the average/`mean` function) the reviews and find the average rating for each movie. We can save this pivot table into the `mean_ratings` variable."""

mean_ratings=data.pivot_table('Ratings','Title',aggfunc='mean')
mean_ratings

"""Now, we can take the `mean_ratings` and sort it by the value of the rating itself. Using this and the `head` function, we can display the top 15 movies by average rating."""

mean_ratings=data.pivot_table('Ratings',index=["Title"],aggfunc='mean')
top_15_mean_ratings = mean_ratings.sort_values(by = 'Ratings',ascending = False).head(15)
top_15_mean_ratings

"""Let's adjust our original `mean_ratings` function to account for the differences in gender between reviews. This will be similar to the same code as before, except now we will provide an additional `columns` parameter which will separate the average ratings for men and women, respectively."""

mean_ratings=data.pivot_table('Ratings',index=["Title"],columns=["Gender"],aggfunc='mean')
mean_ratings

"""We can now sort the ratings as before, but instead of by `Rating`, but by the `F` and `M` gendered rating columns. Print the top rated movies by male and female reviews, respectively."""

data=pd.merge(pd.merge(ratings_data,user_data),movies_data)

mean_ratings=data.pivot_table('Ratings',index=["Title"],columns=["Gender"],aggfunc='mean')
top_female_ratings = mean_ratings.sort_values(by='F', ascending=False)
print(top_female_ratings.head(15))

top_male_ratings = mean_ratings.sort_values(by='M', ascending=False)
print(top_male_ratings.head(15))

mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sorted_by_diff = mean_ratings.sort_values(by='diff')
sorted_by_diff[:10]

"""Let's try grouping the data-frame, instead, to see how different titles compare in terms of the number of ratings. Group by `Title` and then take the top 10 items by number of reviews. We can see here the most popularly-reviewed titles."""

ratings_by_title=data.groupby('Title').size()
ratings_by_title.sort_values(ascending=False).head(10)

"""Similarly, we can filter our grouped data-frame to get all titles with a certain number of reviews. Filter the dataset to get all movie titles such that the number of reviews is >= 2500.

##

Create a ratings matrix using Numpy. This matrix allows us to see the ratings for a given movie and user ID. 

Additionally, choose 3 users that have rated the movie with MovieID "**1377**" (Batman Returns). Print these ratings, they will be used later for comparison.



"""

#all movies with reviews >= 2500
MOV = ratings_by_title[ratings_by_title >= 2500]
print(MOV)

# Create the matrix
user_ID = ratings_data["UserID"].max()
movie_ID = ratings_data["MovieID"].max()
ratings = np.zeros((user_ID, movie_ID), dtype=np.uint8)

for index, row in ratings_data.iterrows():
    ratings[row["UserID"]-1, row["MovieID"]-1] = row["Ratings"]

# Print the shape
print("Shape of the ratings matrix is:", ratings.shape)

# Store and print ratings for Batman Returns
movie_ID = 1377
batman_movie_rating = np.where(ratings[:, movie_ID-1] > 0)[0][:3]

for user in batman_movie_rating:
    rating = ratings[user, movie_ID-1]
    print(f"User {user+1} rated Batman Returns movie: {rating}")

"""## Question 2

Normalize the ratings matrix using Z-score normalization. 
"""

# Compute mean ratings for each movie (excluding zeros)
column_mean = np.nanmean(ratings, axis=0)

# Find columns with non-zero standard deviation
non_zero_std_col = np.std(ratings, axis=0) != 0

# Normalize ratings only for columns with non-zero standard deviation
normlzd_ratings = np.zeros_like(ratings, dtype=np.float64)
for i in range(ratings.shape[1]):
    if non_zero_std_col[i]:
        normlzd_ratings[:, i] = (ratings[:, i] - column_mean[i]) / np.std(ratings[:, i])
    else:
        normlzd_ratings[:, i] = 0
print("normalized_ratings", normlzd_ratings.shape)

"""## 

We're now going to perform Singular Value Decomposition (SVD) on the normalized ratings matrix from the previous question. 
"""

# Compute the SVD of the normalized matrix
U, S, V = np.linalg.svd(normlzd_ratings, full_matrices=False)

# Print the shapes
print("Shape of U matrix:", U.shape)
print("Shape of S matrix:", S.shape)
print("Shape of V matrix:", V.shape)

"""

Reconstruct four rank-k rating matrix $R_k$, where $R_k = U_kS_kV_k^T$ for k = [100, 1000, 2000, 3000]. """

# Perform SVD on the original ratings matrix
U, S, V = np.linalg.svd(ratings, full_matrices=False)

# Reconstructing Rk for k = 100
k_100 = 100
Rk_100 = np.dot(U[:, :k_100], np.dot(np.diag(S[:k_100]), V[:k_100, :]))

# Reconstructing Rk for k = 1000
k_1000 = 1000
Rk_1000 = np.dot(U[:, :k_1000], np.dot(np.diag(S[:k_1000]), V[:k_1000, :]))

# Reconstructing Rk for k = 2000
k_2000 = 2000
Rk_2000 = np.dot(U[:, :k_2000], np.dot(np.diag(S[:k_2000]), V[:k_2000, :]))

# Reconstructing Rk for k = 3000
k_3000 = 3000
Rk_3000 = np.dot(U[:, :k_3000], np.dot(np.diag(S[:k_3000]), V[:k_3000, :]))

# Indices of the 3 users selected in Question 1
user_indices = [9, 12, 17]  #-- Replacing with the actual indices

# Index of the movie ID 1377
movieid_1377 = 1377 - 1

# The original ratings for the selected users and Batman Returns
original_ratings = []
for user_index in user_indices:
    original_ratings.append(ratings[user_index, movieid_1377])

# Predicted ratings for the selected users and Batman Returns for different values of k
pred_rat_k100 = Rk_100[user_indices, movieid_1377]
pred_rat_k1000 = Rk_1000[user_indices, movieid_1377]
pred_rat_k2000 = Rk_2000[user_indices, movieid_1377]
pred_rat_k3000 = Rk_3000[user_indices, movieid_1377]

# Original and predicted ratings for Batman Returns
print("Original ratings for Batman Returns:", original_ratings)
print("Predicted ratings for Batman Returns (k=100):", pred_rat_k100)
print("Predicted ratings for Batman Returns (k=1000):", pred_rat_k1000)
print("Predicted ratings for Batman Returns (k=2000):", pred_rat_k2000)
print("Predicted ratings for Batman Returns (k=3000):", pred_rat_k3000)

"""

### Cosine Similarity
Cosine similarity is a metric used to measure how similar two vectors are. Mathematically, it measures the cosine of the angle between two vectors projected in a multi-dimensional space. Cosine similarity is high if the angle between two vectors is 0, and the output value ranges within $cosine(x,y) \in [0,1]$. $0$ means there is no similarity (perpendicular), where $1$ (parallel) means that both the items are 100% similar.

$$ cosine(x,y) = \frac{x^T y}{||x|| ||y||}  $$

**Based on the reconstruction rank-1000 rating matrix $R_{1000}$ and the cosine similarity,** sort the movies which are most similar. You will have a function `top_movie_similarity` which sorts data by its similarity to a movie with ID `movie_id` and returns the top $n$ items, and a second function `print_similar_movies` which prints the titles of said similar movies. Return the top 5 movies for the movie with ID `1377` (*Batman Returns*)

Note: While finding the cosine similarity, there are a few empty columns which will have a magnitude of **zero** resulting in NaN values. These should be replaced by 0, otherwise these columns will show most similarity with the given movie.
"""

def top_movie_similarity(movie_id, Rk, n=5):
    # The index of the target movie
    target_movie_index = movie_ID.tolist().index(movie_id)

    # cosine similarity between the target movie and all remaining movies
    cosine_similarity = np.dot(Rk, Rk[target_movie_index]) / (np.linalg.norm(Rk, axis=1) * np.linalg.norm(Rk[target_movie_index]))

    # Replace NaN values with 0 to avoid incorrect similarity comparisons
    cosine_similarity[np.isnan(cosine_similarity)] = 0

    # Sort movies based on cosine similarity (starting from higher similarity)
    similar_movies_indices = np.argsort(cosine_similarity)[::-1]

    # Return top n similar movies (not including the target movie itself)
    top_movies_indices = similar_movies_indices[similar_movies_indices != target_movie_index][:n]

    print("Similar Scores:", cosine_similarity)  # Add this line to see the similarity scores
    print("Sorted Ind:", similar_movies_indices)  # Add this line to see the sorted indices
    return top_movies_indices

def print_similar_movies(top_movie_indices):
    # Printing the titles of similar movies
    similar_movie_titles = []
    for movie_ind in top_movie_indices:
        if movie_ind < len(movies_data):
            similar_movie_titles.append(movies_data.iloc[movie_ind]['Title'])
        else:
            similar_movie_titles.append("Unknown Movie")

    print("Top Similar Movies:")
    for idx, title in enumerate(similar_movie_titles, start=1):
        print(f"{idx}. {title}")

# top 5 similar movies for Batman Returns id:1377
target_movie_id = 1377
top_movie_indices_r1000 = top_movie_similarity(target_movie_id, Rk_1000, n=5)
print_similar_movies(top_movie_indices_r1000)

"""

### Movie Recommendations
Using the same process write `top_user_similarity` which sorts data by its similarity to a user with ID `user_id` and returns the top result. Then find the MovieIDs of the movies that this similar user has rated most highly, but that `user_id` has not yet seen. Find at least 5 movie recommendations for the user with ID `5954` and print their titles.

Hint: To check your results, find the genres of the movies that the user likes and compare with the genres of the recommended movies.
"""

# Sort users based on cosine similarity
def top_user_similarity(data, user_id):
    user_index = user_id - 1
    similarities = np.nan_to_num(np.nanmean(np.dot(data, data[user_index]) / (np.linalg.norm(data, axis=1) * np.linalg.norm(data[user_index]))))
    return np.argsort(similarities)[::-1]

# movie recommendations for user ID=5954
user_id = 5954
similar_users = top_user_similarity(normlzd_ratings, user_id)
movies_watched_by_user = set(np.where(ratings[user_id - 1] != 0)[0])
recomm_movies = []

for user in similar_users:
    if len(recomm_movies) >= 5:
        break
    movies_ratby_simi_user = set(np.where(ratings[user] != 0)[0])
    movies_to_recommend = movies_ratby_simi_user - movies_watched_by_user
    recomm_movies.extend(movies_to_recommend)

# Print recommended movie titles
print("Recommended movies for user 5954:")
for movie_index in recomm_movies[:5]:
    print(movies_data.iloc[movie_index]["Title"])
