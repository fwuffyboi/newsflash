<script>

    import {onMount} from "svelte";
    import bwipjs from '@bwip-js/browser';

    let { songName = "Loading..", songArtists = "Loading..", albumName = "Loading..", albumImg, songURL, nowPlaying = true} = $props();

    onMount(() => {
        // Draw the datamatrix barcode after the canvas is mounted
        try {
            bwipjs.toCanvas("qrcanvas", {
                bcid:        'datamatrix',
                text:        songURL,
                scale:       5,
                height:      5,
                width:       5
            });
        } catch (e) {
            console.error("bwipjs error:", e);
        }
    })

</script>

    <!-- When music is NOT playing -->
{#if songName === "Nothing is playing right now..." || !nowPlaying }
    <section class="h-12 flex flex-row">
        <div class="flex flex-col pr-4 text-gray-200 text-right">
            <span class="font-bold text-4xl italic tracking-tight animate-pulse line-clamp-3">Nothing's playing...</span>
        </div>
    </section>
{/if}

    <!-- For when music is playing! -->
{#if songName !== "Nothing is playing right now..." && nowPlaying }
    <section class="h-60 flex flex-row">
        <div class="flex flex-col pr-2 text-right mt-auto">

            <!-- Album name -->
            <span class="font-light text-gray-300 text-lg italic tracking-tight text-balance overflow-ellipsis line-clamp-1">{albumName}</span>

            <!-- Song name -->
            <span class="font-bold text-gray-200 text-4xl italic tracking-tight text-balance overflow-ellipsis line-clamp-3">{songName}</span>

            <!-- Artist name -->
            <span class="text-2xl text-gray-200 font-thin overflow-ellipsis line-clamp-2">{songArtists}</span>

        </div>
        <img class="h-full w-auto aspect-square bg-black border-gray-400 border-2 rounded-lg " alt="The album cover for the album {albumName}" src={albumImg} id="aac" crossOrigin="anonymous" />

<!--        <div class="text-right text-white">-->
<!--            <span class="italic">Scan for song bleh</span>-->
<!--            <div class="w-23 h-23 bg-white">-->
<!--                <canvas class="w-full h-full aspect-square p-1" id="qrcanvas" ></canvas>-->
<!--            </div>-->

<!--        </div>-->

    </section>
{/if}
