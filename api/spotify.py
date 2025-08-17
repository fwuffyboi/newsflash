from api.qrcode import make_qr_code


def get_current_track_spotify(access_token, access_secret, spotify_language, logger):
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

    if playback and playback.get('item'):
        track = playback['item']
        artists = [artist for artist in track['artists']]
        if len(artists) == 2:
            # If there are two artists, join it together with " & "
            artist_names = ' & '.join([artist['name'] for artist in artists])
        else:
            # If there are more than two artists, join them with ", ", then join the last two with " & "
            if len(artists) > 2:
                artist_names = ', '.join([artist['name'] for artist in artists[:-1]]) + ' & ' + artists[-1]['name']
            else:
                # If there is only one artist, just return the name
                artist_names = artists[0]['name']

        # Convert the QR code to a normal string so it can be returned in the response
        qr_code = make_qr_code(track['external_urls']['spotify'])
        qr_code = qr_code.decode('utf-8') if isinstance(qr_code, bytes) else qr_code

        current_track_info = {
            "id": track['id'],
            "track_name": track['name'],
            "artists": artist_names,
            "link": track['external_urls']['spotify'],
            "album": track['album']['name'],
            "cover": track['album']['images'][0]['url'],
            "qr_code": qr_code
        }

        return current_track_info

    logger.error("No current playback found or playback item is empty.")
    return None