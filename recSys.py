import pandas as pd
class Rec:
    def __init__(self,userr_coll, userr_name):
        self.userr_name = userr_name
        self.userr_coll = userr_coll
        movies_dff = pd.read_csv('data/dataset1.csv')
        movies_df = movies_dff.drop('rating',axis = 1)
        import re
        pat = r'[A-Z][a-z]*'
        movies_df['genres'] = movies_df['genres'].apply(lambda x:re.findall(pat,str(x)))

        moviesWithGenres_df = movies_df.copy()

        c = 1
        for index, row in movies_df.iterrows():
            c+=1
            try:
                for genre in row['genres']:

                    moviesWithGenres_df.at[index, genre] = 1
            except:
                movies_df.drop(c)
        moviesWithGenres_df = moviesWithGenres_df.fillna(0)
        userInput = userr_coll.find({})
        userInput = list(userInput)[0]['movie']
        inputMovies = pd.DataFrame(userInput)
        inputMovies.drop_duplicates(subset= 'title',keep = 'last',inplace=True)

        inputMovies = inputMovies.tail()
        try:
            inputMovies['rating'] = inputMovies['rating ']
        except:
            pass
        inputId = movies_df[movies_df['title'].isin(inputMovies['title'].tolist())]
        inputMovies = pd.merge( inputMovies,inputId,on = 'title')
        inputMovies = inputMovies.drop('genres', 1).drop('year', 1)

        userMovies = moviesWithGenres_df[moviesWithGenres_df['movieId'].isin(inputMovies['movieId'].tolist())]

        userMovies = userMovies.reset_index(drop=True)
        userGenreTable = userMovies.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)

        userProfile = userGenreTable.transpose().dot(inputMovies['rating'])

        userpf = pd.DataFrame(userProfile)
        userpf.to_csv('data/userProfile.csv')
        genreTable = moviesWithGenres_df.set_index(moviesWithGenres_df['movieId'])
        genreTable = genreTable.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)

        recommendationTable_df = ((genreTable*userProfile).sum(axis=1))/(userProfile.sum())
        

        recommendationTable_df = recommendationTable_df.sort_values(ascending=False)

        x =  movies_df.loc[movies_df['movieId'].isin(recommendationTable_df.head(10).keys())].reset_index()
        d = []
        for i in x['title']:

            d.append(i)
        userr_coll.update({'_id':self.userr_name},{'$set':{'recommanded':d}})


