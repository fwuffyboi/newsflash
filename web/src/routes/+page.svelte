<script lang="ts">
    import { onMount } from 'svelte';
    import { CloudAlert } from 'lucide-svelte';
    import Spotify from "../components/Spotify.svelte";
    import Weather from "../components/Weather.svelte";

    let time: string = '';
    let activity = true;
    let activityHTTPError = '';
    let activeTopWidget = 'spotify';

    let spotifyFixedData = {};

    onMount(() => {
        const updateTime = () => {
            const now = new Date();
            time = now.toLocaleTimeString([], { hour12: false });
        };

        updateTime();
        pingMirrorAPI();
        getSpotifyNowPlayingData()

        const timeInterval = setInterval(updateTime, 200);
        const activityInterval = setInterval(pingMirrorAPI, 3000);
        const gsnpd = setInterval(getSpotifyNowPlayingData, 3000);

        return () => {
            clearInterval(timeInterval);
            clearInterval(activityInterval);
            clearInterval(gsnpd);
            // clearInterval(componentInterval);
        }
    });

    // Ping the flask server every 3 seconds to see if the connection is active
    const pingMirrorAPI = () => {
        fetch("http://192.168.0.226:8080/ping")
            .then(response => response.json())
            .then(data => {

                console.log(data);

                activityHTTPError = '';
            }).catch(function(err) {
                console.log('Fetch Error: ', err);
                if (err == "TypeError: NetworkError when attempting to fetch resource.") {
                    activity = false;
                    activityHTTPError = "Network error! - Could not ping API.";
                } else {
                    activity = false;
                    activityHTTPError = (err);
                }

        });
    }

    const getSpotifyNowPlayingData = () => {
        fetch("http://192.168.0.226:8080/api/v1/spotify/now-playing")
            .then(response => response.json())
            .then(data => {
                console.log(data);

                // Create a temp list var for the queue and each track in it
                let spotifyQueueItem;
                let spotifyQueueList;
                for (spotifyQueueItem in data.next_tracks) {
                    spotifyQueueList += data.next_tracks[spotifyQueueItem];
                }

                spotifyFixedData = {
                    "title": data.current_track.track_name,
                    "album": data.current_track.album,
                    "artists": data.current_track.artists,
                    "cover": data.current_track.cover,
                    "device_name": data.current_track.device,
                    "device_type": data.current_track.device_type,
                    "duration_ms": data.current_track.duration_ms,
                    "progress_ms": data.current_track.progress_ms,
                    "is_playing": data.current_track.is_playing,
                    "id": data.current_track.id,
                    "link": data.current_track.link,

                    "queue": spotifyQueueList
                };
                console.log(spotifyFixedData)

            })
    }


    const pageTitle = "NewsFlash"
</script>

<svelte:head>
	<title>{pageTitle}</title>
	<meta name="description" content="The KIRASTAR NewsFlash application." />
</svelte:head>

<section class="flex flex-col justify-right items-end pt-5 pr-6 italic text-white">

    <h1 class="font-[Funnel_Display] font-bold text-6xl">{time}</h1>

    {#if activityHTTPError !== ''}
        <section class="flex flex-row justify-right items-end p-1 gap-2 text-white">
            <CloudAlert />
            <h3 class="italic text-right">{activityHTTPError}</h3>
        </section>
    {/if}
</section>


<section class="flex flex-col justify-right items-end p-3 pt-0 gap-2 text-white">
    <!--Here, add all the nested components.
    Use svelte's html logic to check if that one should be active right now.-->

    {#if activeTopWidget === 'spotify'}
        <Spotify
                albumImg = {spotifyFixedData.cover} albumName = {spotifyFixedData.album}
                songName = {spotifyFixedData.title} songArtists={spotifyFixedData.artists}
                duration={spotifyFixedData.duration_ms} nowPlaying={spotifyFixedData.is_playing}
                songURL={spotifyFixedData.link} pgs={spotifyFixedData.progress_ms}/>
    {/if}
    <!--<Weather/>-->
</section>
