-- A seed for the application's SQLite database describing two queued downloads.

INSERT INTO metadata (track_name, main_artist, album_name, track_number, disc_number, release_date)
VALUES ("The Girl Is Mine", "Michael Jackson", "Thriller", 3, 1, "1982"); -- metadata id: 1

INSERT INTO artists (name)
VALUES ("Paul McCartney"); -- artist id: 1

INSERT INTO metadata_artists (metadata_id, artist_id)
VALUES (1, 1);

INSERT INTO downloads (url, codec, bitrate, metadata_id, status, download_dir)
VALUES ("https://www.youtube.com/watch?v=8GB9BULxZ8c", "flac", 320, 1, "queued", "/home/user/music"); -- downloads id: 1

INSERT INTO metadata (track_name, main_artist, album_name, release_date, album_cover_path)
VALUES ("Radio Ga Ga", "Queen", "The Works", "20-02-1984", "/home/user/pictures/cover.jpg"); -- metadata id: 2

INSERT INTO downloads (url, codec, bitrate, metadata_id, status, download_dir)
VALUES ("https://www.youtube.com/watch?v=azdwsXLmrHE", "mp3", 320, 2, "queued", "/home/user/music"); -- downloads id: 2
