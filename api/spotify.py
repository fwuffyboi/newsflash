def get_next_4_tracks_spotify(access_token, access_secret, spotify_language, logger):
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth

    sp = spotipy.Spotify(
        language=spotify_language,
        requests_timeout=2,
        retries=3,
        auth_manager=SpotifyOAuth(
            client_id=access_token,
            client_secret=access_secret,
            redirect_uri="http://127.0.0.1:8080",
            scope="user-read-playback-state"
        )
    )

    playback = sp.current_playback()
    if not playback:
        logger.warn("No playback information found, user is likely not listening to anything. Playback: {}".format(playback))
        return None

    def format_track(track):
        artists = [artist['name'] for artist in track['artists']]
        if len(artists) == 2:
            artist_names = ' & '.join(artists)
        elif len(artists) > 2:
            artist_names = ', '.join(artists[:-1]) + ' & ' + artists[-1]
        else:
            artist_names = artists[0]

        return {
            "id": track['id'],
            "track_name": track['name'],
            "artists": artist_names,
            "link": track['external_urls']['spotify'],
            "album": track['album']['name'],
            "cover": track['album']['images'][0]['url'],
            "duration_ms": track['duration_ms']
        }

    current_track_info = format_track(playback['item'])
    current_track_info.update({
        "is_playing": playback['is_playing'],
        "progress_ms": playback['progress_ms'],
        "device": playback['device']['name'],
        "device_type": playback['device']['type']
    })

    queue_playback = sp.queue()
    if not queue_playback:
        logger.error("No queue playback information found.")
        next_tracks = []
    else:
        next_tracks = [format_track(track) for track in queue_playback.get('queue', [])[:3]]

    return {
        "current_track": current_track_info,
        "next_tracks": next_tracks
    }