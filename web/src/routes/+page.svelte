<script lang="ts">

import { onMount } from 'svelte';
import { m } from '$lib/paraglide/messages.js'; // i18n
import {CloudAlert} from 'lucide-svelte';
import bwipjs from '@bwip-js/browser';
import Spotify from "../components/Spotify.svelte";
import CurrentWeather from "../components/CurrentWeather.svelte";
import WeatherAlertUkMetOfficeUkMetOffice from "../components/WeatherAlertUkMetOffice.svelte";
import TFLTrainStatuses from "../components/TFLTrainStatuses.svelte";
import ICalendar from "../components/ICalendar.svelte";
import {getLocale} from "$lib/paraglide/runtime";
import Hello from "../components/Hello.svelte";
import FaceInfoWidget from "../components/FaceInfoWidget.svelte";

let videoEl!: HTMLVideoElement;
let canvasEl!: HTMLCanvasElement;
let CameraStatus = $state("Connecting..."); // todo: translate
let CameraResult = $state("...");
let CameraFaces = $state(0);
const CAMERA_CAPTURE_INTERVAL_MS = 3000;

let time: string = $state('LOADING...'); // todo: translate

const ACTIVITY_TIMEOUT = 15
let activity = $state(false);
let activity_ttl = 0;

let greetingActive = $state(false);
let greetingBool = $state(true);

let activityHTTPError = $state('');
let WebUIHalt = $state('');

let enabled_apis: [string] = $state(['']);

let spotifyQueueList = [];

let spotifyFixedData = $state({
    "title":       "Loading...", // todo: translate this
    "album":       "Loading...",
    "artists":     "Loading...", // todo: translate this
    "cover":       "",
    "device_name": "Loading...", // todo: translate this
    "device_type": "Loading...",
    "duration_ms": 1000,
    "progress_ms": 0,
    "is_playing":  false,
    "id":          "Loading...",
    "link":        "",

    "queue":       [
        {
            "artists": "Loading...", // todo: translate this
            "cover": "",
            "track_name": "Loading...", // todo: translate this
        }]
});

async function startCamera() {
    try {
        videoEl.srcObject = await navigator.mediaDevices.getUserMedia({
            video: {width: 640, height: 480},
            audio: false,
        });
        CameraStatus = "Ready"; // todo: translate this
    } catch (err) {
        console.error(err);
        CameraStatus = "Unknown error"; // todo: translate this
    }
}

async function captureAndSend() {
    // Draw current frame onto the canvas
    const ctx = canvasEl.getContext("2d");
    if (!ctx) return;

    ctx.drawImage(videoEl, 0, 0, canvasEl.width, canvasEl.height);

    // Convert canvas to JPEG blob
    canvasEl.toBlob(async (blob) => {
        if (!blob) return;

        const formData = new FormData();
        formData.append("file", blob, "capture.jpg");

        try {
            CameraStatus = "Processing...";
            const resp = await fetch("http://localhost:8080/api/v1/face", {
                method: "POST",
                body: formData,
            });

            const resjson = await resp.json();

            if (resp.ok) {

                CameraFaces = resjson.faces;

                if (resjson.faces > 0) {
                    CameraResult = "True" // todo: translate this

                    // add time to activity_ttl
                    activity_ttl = Math.floor(Date.now() / 1000) + ACTIVITY_TIMEOUT+4;
                    activity = true;
                } else {
                    CameraResult = "False" // todo: translate this
                }
            } else {
                CameraResult = "Error";  // todo: translate this
            }
        } catch (e) {
            console.error(e);
            CameraResult = "Network error"; // todo: translate this
        } finally {
            CameraStatus = "Ready"; // todo: translate this
        }
    }, "image/jpeg", 0.9);
}

function ActivityCountdown () {
    let t = new Date();

    if (activity) {

        // fuck your "no nested ifs"
        if (Math.floor(Date.now() / 1000) > activity_ttl) {
            console.log(Math.floor(Date.now() / 1000));
            console.log(activity_ttl);

            activity = false;
            greetingActive = false;
        }

    } else {
        return
    }
}

onMount(() => {
    const updateTime = () => {
        time = (new Date).toLocaleTimeString([], { hour12: false });
    };

    // Draw the datamatrix barcode after the canvas is mounted
    try {
        bwipjs.toCanvas("dmcanvas", {
            bcid:        'datamatrix',
            text:        VERSION,
            scale:       9,
            height:      9,
            width:       9
        });
    } catch (e) {
        console.error("bwipjs error:", e);
    }

    startCamera();
    pingMirrorAPI();
    updateTime();

    if ("spotify" in enabled_apis) {
        getSpotifyNowPlayingData();
    }

    const timeInterval    = setInterval(updateTime, 200);
    const pingInterval    = setInterval(pingMirrorAPI, 10000);
    const SpotifyInterval = setInterval(getSpotifyNowPlayingData, 3000);
    const CameraInterval  = setInterval(captureAndSend, CAMERA_CAPTURE_INTERVAL_MS);
    const ActivityInterval = setInterval(ActivityCountdown, 500);


    return () => {
        clearInterval(timeInterval);
        clearInterval(pingInterval);
        clearInterval(SpotifyInterval);
        clearInterval(CameraInterval);
        clearInterval(ActivityInterval);

        if (videoEl.srcObject) {
            // Stop all webcam tracks
            const tracks = (videoEl.srcObject as MediaStream).getTracks();
            tracks.forEach((t) => t.stop());
        }
    }
});

// Ping the flask server every 3 seconds to see if the connection is active
const pingMirrorAPI = () => {
    fetch("http://localhost:8080/api/config", { signal: AbortSignal.timeout(2000) })
        .then(response => response.json())
        .then(data => {
            enabled_apis.pop()
            enabled_apis = data.enabled_apis
            WebUIHalt = ""
            // console.log("enabled apis: ", enabled_apis);
        }).catch(function(err) {
            enabled_apis = ['']
            WebUIHalt = "WebUI HALTED. Network error! - /api/config. Err: " + err;
        })

    fetch("http://localhost:8080/ping", { signal: AbortSignal.timeout(5000) })
        .then(response => response.json())
        .then(data => {
            activityHTTPError = '';
        }).catch(function(err) {
            console.log('Fetch Error: ', err);
            if (err == "TypeError: NetworkError when attempting to fetch resource.") {
                if (activityHTTPError !== "") {
                    activityHTTPError = ": Network error! - Could not ping API.";
                }
            } else {
                activityHTTPError = (err);
            }

    })
};

const getSpotifyNowPlayingData = () => {
    if (enabled_apis.includes('spotify')) {
        if (activity) {
            fetch("http://localhost:8080/api/v1/spotify/now-playing", { signal: AbortSignal.timeout(5000) })
                .then(response => response.json())
                .then(data => {
                    // console.log("spotify current data (playback):", data);

                    // Create a temp list var for the queue and each track in it
                    // let spotifyQueueItem;
                    // let spotifyQueueList = {};

                    // check if the user has any playback
                    if (data.error === "NPIF") {

                        // There __IS NOT__ playback data. Populate the fixedData struct with FAKE data.
                        spotifyFixedData = {
                            "title":       "Nothing is playing right now...",
                            "album":       "",
                            "artists":     "",
                            "cover":       "",
                            "device_name": "",
                            "device_type": "",
                            "duration_ms": 0,
                            "progress_ms": 0,
                            "is_playing":  false,
                            "id":          "",
                            "link":        "",

                            "queue": []
                        };


                    } else { // There __IS__ playback data. Populate the fixedData struct with the real data.
                        let spotifyQueueItem;
                        spotifyQueueList = [];
                        // console.log("data list:", data.data.next_tracks);

                        for (spotifyQueueItem in data.data.next_tracks) {
                            spotifyQueueList.push(data.data.next_tracks[spotifyQueueItem]);
                        }

                        spotifyFixedData = {
                            "title":       data.data.current_track.track_name,
                            "album":       data.data.current_track.album,
                            "artists":     data.data.current_track.artists,
                            "cover":       data.data.current_track.cover,
                            "device_name": data.data.current_track.device,
                            "device_type": data.data.current_track.device_type,
                            "duration_ms": data.data.current_track.duration_ms,
                            "progress_ms": data.data.current_track.progress_ms,
                            "is_playing":  data.data.current_track.is_playing,
                            "id":          data.data.current_track.id,
                            "link":        data.data.current_track.link,

                            "queue":       spotifyQueueList
                        };
                        // console.log("spotify current data (queue):", spotifyQueueList);
                    }
                })
        } else {

            // since activity is false, we can ignore actually returning real data.
            spotifyFixedData = {
                "title":       "Nothing is playing right now...",
                "album":       "",
                "artists":     "",
                "cover":       "",
                "device_name": "",
                "device_type": "",
                "duration_ms": 0,
                "progress_ms": 0,
                "is_playing":  false,
                "id":          "",
                "link":        "",

                "queue": []
            };
        }
    }
}

const VERSION = "BETA-0.15.0";
const COPYRIGHT = "© MIT 2025 Ashley Caramel (fwuffyboi) & Contributors.";
const pageTitle = "NewsFlash Application"

</script>

<svelte:head>
	<title>{pageTitle}</title>
	<meta name="description" content="The NewsFlash application." />
</svelte:head>


<div class="w-screen h-screen">
    <section class="flex flex-col justify-right items-end pr-5 pb-4 italic text-white">

        {#if activity || activityHTTPError !== ''}
            <div class="flex flex-row">
                <FaceInfoWidget FaceDetected={CameraResult} FaceNo={CameraFaces} Status={CameraStatus}/>
                <span class="font-[Funnel_Display] font-bold text-5xl">{time}</span>
            </div>
        {/if}

        {#if activityHTTPError !== '' || WebUIHalt !== ''}
            <section class="flex flex-row justify-right items-end p-1 gap-2 animate-pulse text-white">
                <CloudAlert />
                <div class="flex flex-col">
                    <span class="italic text-right">{activityHTTPError}</span>
                    <span class="italic text-right">{WebUIHalt}</span>
                </div>
            </section>
        {/if}
    </section>
    {#if activity}
        <section class="flex flex-col justify-right items-end gap-3 pr-1">
            <!--Here, add all the nested components.
            Use svelte's html logic to check if that one should be active right now.-->

            {#if enabled_apis.includes('spotify')}
                <Spotify
                        albumImg   = {spotifyFixedData.cover}      albumName = {spotifyFixedData.album}
                        songName   = {spotifyFixedData.title}    songArtists = {spotifyFixedData.artists}
                        nowPlaying ={spotifyFixedData.is_playing} devicetype = {spotifyFixedData.device_type}
                        devicename ={spotifyFixedData.device_name}     queue = {spotifyFixedData.queue}
                />
            {/if}
            <div class="flex flex-row gap-2">

                {#if enabled_apis.includes('owm')}
                    <CurrentWeather/>
                {/if}

                {#if enabled_apis.includes('tfl-trains')}
                    <TFLTrainStatuses />
                {/if}
            </div>
            {#if enabled_apis.includes('met-office-uk')}
                <WeatherAlertUkMetOfficeUkMetOffice />
            {/if}
            {#if enabled_apis.includes('ical')}
                <ICalendar />
            {/if}

        </section>
    {/if}

    <!--todo: make this show for 2 or 3 seconds when the mirror sees the user, as well as when the timeout ends-->
    {#if greetingActive}
        <div class="flex flex-col h-screen justify-center items-center">
            <Hello greeting={greetingBool}/>
        </div>
    {/if}

</div>

{#if activity || activityHTTPError !== ''}
    <!-- Bottom right and left corners -->
    <div class="text-white fixed bottom-1 left-1 mb-0 ml-24">
        <div class="flex flex-col">
            <span class="italic">{VERSION}</span>
            <span class="italic">{COPYRIGHT}</span>
        </div>

        <div class="flex flex-col italic font-thin tracking-tighter animate-pulse w-180">
            <span class="font-bold">{m.disclaimer()}</span>
            <span class="font-medium">{m.locale_visit()}<a href="/locale">/locale</a>. {m.locale_current({ locale: getLocale() })}</span>
        </div>
    </div>
{/if}

<div class="hidden">
    <video bind:this={videoEl} autoplay playsinline><track kind="captions" src=""></video>
    <canvas
            bind:this={canvasEl}
            width="640"
            height="480"
            style="display:none;"
    ></canvas>
</div>

<div class="w-23 h-23 bg-white rounded-sm fixed bottom-1 left-1 mb-0">
    <canvas class="w-full h-full aspect-square p-1" id="dmcanvas" ></canvas>
</div>
