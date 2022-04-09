from datetime import datetime

class Title:
    spi_code: str
    spi_identifiers: str
    spi_title_type: str
    spi_year: int
    spi_titles: str
    spi_title_original: str
    spi_description: str
    spi_editorial_note: str
    spi_fb_regions: str
    spi_age: str
    spi_series_title: str
    spi_series_original_title: str
    spi_series_season_title: str
    spi_position: str
    spi_publish_date: str
    spi_release_date: str
    spi_directors: str
    spi_writer: str
    spi_producer: str
    spi_cast: str
    spi_tags: str
    spi_imdb_score: float
    spi_editors_score: float
    spi_duration_minutes: int
    spi_slug: str
    spi_url_webapp: str
    spi_url_paywall: str
    is_imdb_searched: bool
    is_imdb_found: bool
    got_imdb_details: bool
    imdb_id: str
    imdb_url: str
    imdb_imdb_score: float
    imdb_genre: str
    imdb_directors: str
    imdb_cast: str
    imdb_duration_minutes: int
    imdb_age_rating: str
    imdb_last_update_date: datetime

    notes: str

    def __init__(self, spi_code):
        self.spi_code = spi_code
        self.spi_title_type = "Movie" if spi_code.startswith("SPI") else "Series"

    def details(self):
        print("spi_code: " + self.spi_code
            + ", title_type: " + self.spi_title_type
            + ", year: " + str(self.spi_year)
            + ", title_original: " + self.spi_title_original
            + ", notes: " + self.notes
            + ", isImdbSearched: " + str(self.is_imdb_searched)
            + ", isImdbFound: " + str(self.is_imdb_found)
            + ", gotImdbDetails: " + str(self.got_imdb_details)
            + ", url_imdb: " + str(self.imdb_url)
            + ", imdbLastUpdate: " + str(self.imdb_last_update_date)
        )
