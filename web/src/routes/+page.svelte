<script lang="ts">
    import { onMount } from 'svelte';
    import {CloudAlert} from 'lucide-svelte';
    import bwipjs from '@bwip-js/browser';
    import Spotify from "../components/Spotify.svelte";
    import Weather from "../components/Weather.svelte";
    import WeatherAlert from "../components/WeatherAlert.svelte";

    let time: string = '';
    let activity = true;
    let activityHTTPError = '';

    let enabled_apis: [string] = ['']

    let users_name = 'User';

    let spotifyFixedData = {
        "title":       "",
        "album":       "",
        "artists":     "",
        "cover":       "",
        "device_name": "",
        "device_type": "",
        "duration_ms": 1000,
        "progress_ms": 0,
        "is_playing":  false,
        "id":          "",
        "link":        "",

        "queue":       {}
    };

    onMount(() => {
        const updateTime = () => {
            const now = new Date();
            time = now.toLocaleTimeString([], { hour12: false });
        };

        updateTime();
        pingMirrorAPI();

        // Draw the datamatrix barcode after the canvas is mounted
        try {
            bwipjs.toCanvas("dmcanvas", {
                bcid:        'datamatrix',
                text:        VERSION,
                scale:       5,
                height:      5,
                width:       5
            });
        } catch (e) {
            console.error("bwipjs error:", e);
        }

        // here, check what apis are enabled and store it, as well as the main user's name
        fetch("http://192.168.0.226:8080/api/config")
            .then(response => response.json())
            .then(data => {
                console.log("dnata", data);
                users_name = data.user_name;
                console.log(users_name);
                enabled_apis.pop()
                for (let item of data.enabled_apis) {
                    enabled_apis.push(item);
                }
                console.log(enabled_apis);
            })


        if ('spotify' in enabled_apis) {
            getSpotifyNowPlayingData();
            console.log('spotify WORKS 1');
        }

        const timeInterval = setInterval(updateTime, 200);
        const activityInterval = setInterval(pingMirrorAPI, 3000);
        const gsnpd = setInterval(getSpotifyNowPlayingData, 3000);

        return () => {
            clearInterval(timeInterval);
            clearInterval(activityInterval);
            if ('spotify' in enabled_apis) {
                clearInterval(gsnpd);
            }
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
                let spotifyQueueList = {};

                // check if the user has any playback
                if (data.message == "User is not listening to anything or there was a spotify API error.") {

                    // There __IS NOT__ playback data. Populate the fixedData struct with FAKE data.
                    spotifyFixedData = {
                        "title":       "Nothing is playing right now...",
                        "album":       "",
                        "artists":     "",
                        "cover":       "/blank_album_spotify.png",
                        "device_name": "",
                        "device_type": "",
                        "duration_ms": 0,
                        "progress_ms": 0,
                        "is_playing":  false,
                        "id":          "",
                        "link":        "",

                        "queue": {}
                    };


                } else { // There __IS__ playback data. Populate the fixedData struct with the real data.
                    for (spotifyQueueItem in data.next_tracks) {
                        spotifyQueueList += data.next_tracks[spotifyQueueItem];
                    }

                    spotifyFixedData = {
                        "title":       data.current_track.track_name,
                        "album":       data.current_track.album,
                        "artists":     data.current_track.artists,
                        "cover":       data.current_track.cover,
                        "device_name": data.current_track.device,
                        "device_type": data.current_track.device_type,
                        "duration_ms": data.current_track.duration_ms,
                        "progress_ms": data.current_track.progress_ms,
                        "is_playing":  data.current_track.is_playing,
                        "id":          data.current_track.id,
                        "link":        data.current_track.link,

                        "queue":       spotifyQueueList
                    };
                    console.log(spotifyFixedData)
                }

            })
    }

    const VERSION = "ALPHA-0.1.0";
    const pageTitle = "NewsFlash Application"

</script>

<svelte:head>
	<title>{pageTitle}</title>
	<meta name="description" content="The KIRASTAR NewsFlash application." />
</svelte:head>

{#if activity}
    <div class="w-screen h-screen">
        <section class="flex flex-col justify-right items-end pr-5 pb-4 italic text-white">

            <span class="font-[Funnel_Display] font-bold text-5xl">{time}</span>

            {#if activityHTTPError !== ''}
                <section class="flex flex-row justify-right items-end p-1 gap-2 text-white">
                    <CloudAlert />
                    <h3 class="italic text-right">{activityHTTPError}</h3>
                </section>
            {/if}
        </section>


        <section class="flex flex-col justify-right items-end gap-5 pr-2">
            <!--Here, add all the nested components.
            Use svelte's html logic to check if that one should be active right now.-->

            {#if enabled_apis.includes('spotify')}
                <Spotify
                        albumImg = {spotifyFixedData.cover} albumName = {spotifyFixedData.album}
                        songName = {spotifyFixedData.title} songArtists={spotifyFixedData.artists}
                        duration={spotifyFixedData.duration_ms} nowPlaying={spotifyFixedData.is_playing}
                        songURL={spotifyFixedData.link} pgs={spotifyFixedData.progress_ms}
                />
            {/if}
            <div class="flex flex-row gap-2">
                <Weather/>
                <!-- Calendar or day overview goes here?-->
            </div>

            <WeatherAlert />
        </section>


    </div>

    <!-- Bottom right and left corners -->
    <div class="text-right text-white fixed bottom-1 left-1 mb-0">
        <span class="italic">{VERSION}</span>
        <div class="w-23 h-23 bg-white">
            <canvas class="w-full h-full aspect-square p-1" id="dmcanvas" ></canvas>
        </div>

    </div>
    <div class="text-right text-white fixed bottom-0 right-1.5 mb-0 w-190">
        <div class="flex flex-col italic font-thin tracking-tighter animate-pulse">
            <span class="font-bold">!!!! DISCLAIMER: All information displayed is for informational purposes only. Do not rely on this device's information for ANY type of emergency or critical activity. ALWAYS consult official sources for important information !!!!</span>
            <span></span>

        </div>

    </div>


{/if}