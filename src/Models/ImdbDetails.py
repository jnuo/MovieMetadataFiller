
class ImdbDetails:
    spi_code: str
    title_type: str
    year: int
    title_original: str 
    language_original: str
    imdb_id: str 
    director: str
    genre: str
    cast: str
    imdb_score: float
    editor_score: float
    duration_minutes: int
    url_webapp: str
    url_paywall: str
    notes: str
    isImdbSearched: bool
    gotImdbDetails: bool
    imdbLastUpdate: datetime

    def __init__(self, spi_code):
        self.spi_code = spi_code
        self.title_type = "Movie" if spi_code.startswith("SPI") else "Series"
    
    def details(self):
        print("spi_code: " + self.spi_code
            + ", title_type: " + self.title_type
            + ", year: " + str(self.year)
            + ", title_original: " + self.title_original
            + ", language_original: " + self.language_original
            + ", imdb_id: " + self.imdb_id
            + ", director: " + str(self.director)
            + ", genre: " + self.genre
            + ", cast: " + str(self.cast)
            + ", imdb_score: " + str(self.imdb_score)
            + ", editor_score: " + str(self.editor_score)
            + ", duration_minutes: " + str(self.duration_minutes)
            + ", url_webapp: " + self.url_webapp
            + ", url_paywall: " + self.url_paywall
            + ", notes: " + self.notes
            + ", isImdbSearched: " + str(self.isImdbSearched)
            + ", gotImdbDetails: " + str(self.gotImdbDetails)
            + ", imdbLastUpdate: " + str(self.imdbLastUpdate)
        )