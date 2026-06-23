from django.core.management.base import BaseCommand
from movies.models import Genre, Movie

GENRES = [
    'Action', 'Drama', 'Comedy', 'Thriller', 'Sci-Fi', 'Romance',
    'Crime', 'Animation', 'Fantasy', 'Horror', 'Mystery', 'Adventure',
]

MOVIES = [
    # title, year, language, director, duration, genres, description
    ("Inception", 2010, "English", "Christopher Nolan", 148, ["Sci-Fi", "Thriller", "Action"],
     "A skilled thief who steals secrets from people's dreams is given a chance at redemption if he can plant an idea instead of stealing one."),
    ("The Dark Knight", 2008, "English", "Christopher Nolan", 152, ["Action", "Crime", "Drama"],
     "Batman faces his greatest psychological and physical test when a criminal mastermind known as the Joker wreaks havoc on Gotham City."),
    ("Interstellar", 2014, "English", "Christopher Nolan", 169, ["Sci-Fi", "Drama", "Adventure"],
     "A team of explorers travel through a wormhole in search of a new habitable planet as Earth becomes unable to sustain life."),
    ("Parasite", 2019, "Korean", "Bong Joon-ho", 132, ["Drama", "Thriller", "Comedy"],
     "Greed and class discrimination threaten the newly formed symbiotic relationship between a wealthy family and a poor one."),
    ("Train to Busan", 2016, "Korean", "Yeon Sang-ho", 118, ["Horror", "Action", "Thriller"],
     "Passengers on a train to Busan must fight for survival as a zombie outbreak spreads across the country."),
    ("Spirited Away", 2001, "Japanese", "Hayao Miyazaki", 125, ["Animation", "Fantasy", "Adventure"],
     "A young girl wanders into a world ruled by spirits and must find a way to free herself and her parents."),
    ("Your Name", 2016, "Japanese", "Makoto Shinkai", 106, ["Animation", "Romance", "Fantasy"],
     "Two strangers find themselves linked in a bizarre way, swapping bodies and slowly falling for one another across time."),
    ("3 Idiots", 2009, "Hindi", "Rajkumar Hirani", 170, ["Comedy", "Drama"],
     "Two friends search for their long-lost companion, recalling their college years and his rebellious approach to education."),
    ("Dangal", 2016, "Hindi", "Nitesh Tiwari", 161, ["Drama", "Action"],
     "A former wrestler trains his daughters to become India's first world-class female wrestlers."),
    ("Lagaan", 2001, "Hindi", "Ashutosh Gowariker", 224, ["Drama", "Adventure"],
     "Villagers stake their future on a cricket match against their British rulers to escape an oppressive tax."),
    ("Baahubali: The Beginning", 2015, "Telugu", "S. S. Rajamouli", 159, ["Action", "Fantasy", "Adventure"],
     "A young man raised by tribal villagers sets out to discover his royal origins and an ancient kingdom's secrets."),
    ("RRR", 2022, "Telugu", "S. S. Rajamouli", 187, ["Action", "Drama", "Adventure"],
     "A fictional account of two real revolutionaries and their fight against the British colonial empire in India."),
    ("Arjun Reddy", 2017, "Telugu", "Sandeep Reddy Vanga", 182, ["Drama", "Romance"],
     "A short-tempered surgeon descends into self-destructive habits after losing the love of his life."),
    ("Vikram", 2022, "Tamil", "Lokesh Kanagaraj", 174, ["Action", "Thriller", "Crime"],
     "A special agent investigates a series of murders carried out by a masked group, uncovering a larger conspiracy."),
    ("96", 2018, "Tamil", "C. Prem Kumar", 158, ["Romance", "Drama"],
     "Former high school sweethearts reunite at a school reunion after 22 years apart, reliving old memories."),
    ("Drishyam", 2013, "Malayalam", "Jeethu Joseph", 160, ["Thriller", "Drama", "Mystery"],
     "A man goes to extreme lengths to protect his family after they become entangled in a crime."),
    ("Pather Panchali", 1955, "Hindi", "Satyajit Ray", 125, ["Drama"],
     "A poor family in rural Bengal struggles to survive while their young son discovers the wider world around him."),
    ("Pulp Fiction", 1994, "English", "Quentin Tarantino", 154, ["Crime", "Drama"],
     "The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in four tales of violence."),
    ("The Shawshank Redemption", 1994, "English", "Frank Darabont", 142, ["Drama"],
     "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."),
    ("Forrest Gump", 1994, "English", "Robert Zemeckis", 142, ["Drama", "Romance", "Comedy"],
     "The presidencies of Kennedy and Johnson, Vietnam, and other history unfold through the perspective of an Alabama man."),
    ("The Matrix", 1999, "English", "Lana Wachowski", 136, ["Sci-Fi", "Action"],
     "A computer hacker learns about the true nature of reality and his role in the war against the controllers of it."),
    ("Coco", 2017, "English", "Lee Unkrich", 105, ["Animation", "Fantasy", "Adventure"],
     "A boy is transported to the Land of the Dead, where he seeks the help of his deceased musician great-great-grandfather."),
    ("Amélie", 2001, "French", "Jean-Pierre Jeunet", 122, ["Comedy", "Romance"],
     "A shy waitress decides to change the lives of those around her for the better, while struggling with her own isolation."),
    ("Intouchables", 2011, "French", "Olivier Nakache", 112, ["Comedy", "Drama"],
     "After a paralyzing accident, an aristocrat hires a young caretaker from the projects, forming an unlikely friendship."),
    ("Pan's Labyrinth", 2006, "Spanish", "Guillermo del Toro", 118, ["Fantasy", "Drama", "Horror"],
     "In fascist Spain, a girl retreats into an imaginary world while facing the dangers of the real one."),
    ("The Secret in Their Eyes", 2009, "Spanish", "Juan Jose Campanella", 129, ["Mystery", "Drama", "Crime"],
     "A retired legal counselor writes a novel hoping to find closure for one of his old, unresolved homicide cases."),
    ("Oldboy", 2003, "Korean", "Park Chan-wook", 120, ["Thriller", "Mystery", "Action"],
     "After being mysteriously imprisoned for fifteen years, a man is released only to find he must find his captor in five days."),
    ("Memories of Murder", 2003, "Korean", "Bong Joon-ho", 132, ["Crime", "Mystery", "Drama"],
     "Detectives in a small Korean town struggle to solve a series of murders based on the country's first real-life serial killings."),
    ("Akira", 1988, "Japanese", "Katsuhiro Otomo", 124, ["Animation", "Sci-Fi", "Action"],
     "A secret military project endangers Neo-Tokyo when it turns a biker gang member into a rampaging psychic psychopath."),
    ("Ratatouille", 2007, "English", "Brad Bird", 111, ["Animation", "Comedy", "Adventure"],
     "A rat who can cook makes an unusual alliance with a young kitchen worker at a famous Paris restaurant."),
    ("KGF: Chapter 2", 2022, "Kannada", "Prashanth Neel", 168, ["Action", "Drama"],
     "Rocky's reign begins as he takes control of the Kolar Gold Fields, but he must face powerful new enemies."),
    ("U-Turn", 2018, "Kannada", "Pawan Kumar", 124, ["Thriller", "Mystery", "Horror"],
     "A journalism student investigating a series of mysterious deaths on a flyover discovers something supernatural at play."),
    ("Eega", 2012, "Telugu", "S. S. Rajamouli", 130, ["Fantasy", "Action", "Romance"],
     "A man murdered by his rival for the affections of a woman is reincarnated as a housefly and seeks his revenge."),
    ("Andhadhun", 2018, "Hindi", "Sriram Raghavan", 139, ["Thriller", "Crime", "Comedy"],
     "A blind pianist gets caught in a web of murder and deceit after he witnesses what he should not have."),
    ("Jersey", 2019, "Telugu", "Gowtam Tinnanuri", 156, ["Drama"],
     "A failed cricketer in his mid-thirties decides to return to the sport to fulfil his dream and provide for his family."),
    ("Premam", 2015, "Malayalam", "Alphonse Putharen", 156, ["Romance", "Comedy", "Drama"],
     "A college student experiences three different phases of love through his school, college, and adult life."),
    ("La La Land", 2016, "English", "Damien Chazelle", 128, ["Romance", "Drama", "Comedy"],
     "A jazz pianist and an aspiring actress fall in love while pursuing their dreams in Los Angeles."),
    ("Whiplash", 2014, "English", "Damien Chazelle", 106, ["Drama"],
     "A promising young drummer enrolls at a cutthroat music conservatory where his dreams are mentored by a ruthless instructor."),
    ("Avengers: Endgame", 2019, "English", "Anthony Russo", 181, ["Action", "Sci-Fi", "Adventure"],
     "The remaining Avengers assemble once more to reverse the damage caused by Thanos and restore order to the universe."),
    ("Get Out", 2017, "English", "Jordan Peele", 104, ["Horror", "Mystery", "Thriller"],
     "A young man visiting his girlfriend's family estate uncovers a disturbing secret about their true intentions."),
    ("Roja", 1992, "Tamil", "Mani Ratnam", 153, ["Drama", "Romance"],
     "A newly married woman fights to free her husband, who is kidnapped by separatist militants in Kashmir."),
]


class Command(BaseCommand):
    help = "Populate the database with sample genres and movies"

    def handle(self, *args, **options):
        genre_objs = {}
        for name in GENRES:
            genre, _ = Genre.objects.get_or_create(name=name)
            genre_objs[name] = genre
        self.stdout.write(self.style.SUCCESS(f"{len(genre_objs)} genres ready."))

        created_count = 0
        for title, year, language, director, duration, genre_names, desc in MOVIES:
            movie, created = Movie.objects.get_or_create(
                title=title,
                release_year=year,
                defaults={
                    'language': language,
                    'director': director,
                    'duration_minutes': duration,
                    'description': desc,
                }
            )
            movie.genres.set([genre_objs[g] for g in genre_names])
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"{created_count} new movies added ({len(MOVIES)} total in seed list)."))
