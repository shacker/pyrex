from django.db import models


class Year(models.Model):
    year = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.year)

    class Meta:
        indexes = [
            models.Index(fields=['year', ]),
        ]


class Artist(models.Model):
    name = models.CharField(default="Artist Unknown", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name', ]),
        ]


class Album(models.Model):
    title = models.CharField(default="Album Unknown", max_length=255)
    artist = models.ForeignKey(Artist, null=True, blank=True, on_delete=models.SET_NULL)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    album_rating = models.IntegerField(null=True, blank=True)
    album_loved = models.BooleanField(default=False)

    def get_album_rating(self):
        # Convert e.g. 80 (implied 80/100) to 4
        try:
            return int(self.album_rating) / 10 / 2
        except (ValueError, ZeroDivisionError):
            return None

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['title', ]),
        ]


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Kind(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class TrackType(models.Model):
    # e.g. "Remote" or "Local"
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Playlist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Track(models.Model):
    '''
    # Raw field dump from pyitunes, i.e. the data we need to shadow:
    ['album_rating', 'album_rating_computed', 'artist', 'bit_rate', 'comments', 'compilation', 'composer',
    'date_added', 'date_modified', 'disc_count', 'disc_number', 'genre', 'grouping', 'kind',
    'lastplayed', 'length', 'location', 'location_escaped', 'movement_count', 'movement_name',
    'movement_number', 'name', 'persistent_id', 'play_count', 'playlist_order', 'rating', 'rating_computed',
    'sample_rate', 'size', 'skip_count', 'skip_date', 'total_time', 'track_count', 'track_id', 'track_number',
    'track_type', 'work', 'year']

    Not implemented:
    'location', 'location_escaped'
    '''

    album = models.ForeignKey(Album, blank=True, null=True)
    artist = models.ForeignKey(Artist, blank=True, null=True)
    bit_rate = models.IntegerField(null=True, blank=True)
    comments = models.CharField(blank=True, null=True, max_length=255)
    compilation = models.BooleanField(default=False)
    composer = models.ForeignKey(Artist, blank=True, null=True, related_name="track_composer")
    date_added = models.DateTimeField(blank=True, null=True)
    date_modified = models.DateTimeField(blank=True, null=True)
    disc_count = models.IntegerField(null=True, blank=True)
    disc_number = models.IntegerField(null=True, blank=True)
    genre = models.ForeignKey(Genre, blank=True, null=True)
    grouping = models.CharField(blank=True, null=True, max_length=255)
    kind = models.ForeignKey(Kind, blank=True, null=True)
    lastplayed = models.DateTimeField(blank=True, null=True)
    length = models.IntegerField(null=True, blank=True)
    loved = models.BooleanField(default=False)
    movement_count = models.IntegerField(null=True, blank=True)
    movement_name = models.CharField(blank=True, null=True, max_length=255)
    movement_number = models.IntegerField(null=True, blank=True)
    persistent_id = models.CharField(max_length=255, blank=True)
    play_count = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    sample_rate = models.IntegerField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    skip_count = models.IntegerField(null=True, blank=True)
    skip_date = models.DateTimeField(blank=True, null=True)
    title = models.CharField(default="Unknown", max_length=255)
    total_time = models.IntegerField(null=True, blank=True)
    track_id = models.IntegerField(null=True, blank=True)
    track_number = models.IntegerField(null=True, blank=True)
    track_count = models.IntegerField(null=True, blank=True)
    track_type = models.ForeignKey(TrackType, blank=True, null=True, related_name="track_type")
    work = models.CharField(blank=True, null=True, max_length=255)
    year = models.ForeignKey(Year, blank=True, null=True)

    def get_artist(self):
        if self.artist:
            return self.artist
        elif self.album.artist:
            return self.album.artist
        else:
            return None

    def microseconds_to_time(self):
        # Convert microseconds to e.g. 01:23:52 or 04:09
        seconds = int(self.length / 1000)
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)

        s = str(s).zfill(2)
        m = str(m).zfill(2)

        if h:
            h = str(h).zfill(2)
            return("{0}:{1}:{2}".format(h, m, s))
        else:
            return("{0}:{1}".format(m, s))

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['comments', 'persistent_id', 'title', ]),
        ]


class PlaylistEntry(models.Model):
    # Connect a track to a playlist, preserving playlist_order
    track = models.ForeignKey(Track)
    playlist = models.ForeignKey(Playlist)
    playlist_order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.track.title

    class Meta:
        ordering = ["playlist_order"]


class LibraryData(models.Model):
    # Metadata for the Library. Should be just one row of this table.
    last_snapshot = models.DateTimeField(null=True)
    twitter = models.CharField(max_length=255, blank=True)
    facebook = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "Metadata for this library"

    class Meta:
        verbose_name_plural = "Library Metadata"
