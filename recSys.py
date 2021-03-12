import pandas as pd
class Rec:
    def __init__(self,userr_coll, userr_name):
        self.userr_name = userr_name
        self.userr_coll = userr_coll
        self.movies_dff = pd.read_csv('data/dataset1.csv')
        self.movies_df = self.movies_dff.drop('rating',axis = 1)
        import re
        pat = r'[A-Z][a-z]*'
        self.movies_df['genres'] = self.movies_df['genres'].apply(lambda x:re.findall(pat,str(x)))

        self.moviesWithGenres_df = self.movies_df.copy()

        c = 1
        for index, row in self.movies_df.iterrows():
            c+=1
            try:
                for genre in row['genres']:

                    self.moviesWithGenres_df.at[index, genre] = 1
            except:
                self.movies_df.drop(c)
        self.moviesWithGenres_df = self.moviesWithGenres_df.fillna(0)
        self.userInput = self.userr_coll.find({})
        self.userInput = list(self.userInput)[0]['movie']
        self.inputMovies = pd.DataFrame(self.userInput)
        self.inputMovies.drop_duplicates(subset= 'title',keep = 'last',inplace=True)

        self.inputMovies = self.inputMovies.tail()
        try:
            self.inputMovies['rating'] = self.inputMovies['rating ']
        except:
            pass
        self.inputId = self.movies_df[self.movies_df['title'].isin(self.inputMovies['title'].tolist())]
        self.inputMovies = pd.merge( self.inputMovies,self.inputId,on = 'title')
        self.inputMovies = self.inputMovies.drop('genres', 1).drop('year', 1)

        self.userMovies = self.moviesWithGenres_df[self.moviesWithGenres_df['movieId'].isin(self.inputMovies['movieId'].tolist())]

        self.userMovies = self.userMovies.reset_index(drop=True)
        self.userGenreTable = self.userMovies.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)

        self.userProfile = self.userGenreTable.transpose().dot(self.inputMovies['rating'])

        userpf = pd.DataFrame(self.userProfile)
        userpf.to_csv('data/userProfile.csv')
        self.genreTable = self.moviesWithGenres_df.set_index(self.moviesWithGenres_df['movieId'])
        self.genreTable = self.genreTable.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)

        self.recommendationTable_df = ((self.genreTable*self.userProfile).sum(axis=1))/(self.userProfile.sum())
        

        self.recommendationTable_df = self.recommendationTable_df.sort_values(ascending=False)

        self.x =  self.movies_df.loc[self.movies_df['movieId'].isin(self.recommendationTable_df.head(10).keys())].reset_index()
        d = []
        for i in self.x['title']:

            d.append(i)
        self.userr_coll.update({'_id':self.userr_name},{'$set':{'recommanded':d}})


