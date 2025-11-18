<script>

    import {m} from "$lib/paraglide/messages.js"

    let { songName = "Loading..", songArtists = "Loading..", albumName = "Loading..", albumImg, songURL, nowPlaying = true} = $props();

</script>

    <!-- When music is NOT playing -->
{#if songName === "Nothing is playing right now..." || !nowPlaying }
    <section class="h-12 flex flex-row">
        <div class="flex flex-col pr-4 text-gray-200 text-right">
            <span class="font-bold text-4xl italic tracking-tight animate-pulse line-clamp-3">{m.spotify_nothing_is_playing()}</span>
        </div>
    </section>
{/if}

    <!-- For when music is playing! -->
{#if songName !== "Nothing is playing right now..." && nowPlaying }
    <section class="h-60 flex flex-row gap-2">

<!--        Now playing -->
        <div class="flex flex-col pr-2 text-right mt-auto">

            <!-- Album name -->
            <span class="font-light text-gray-300 text-lg italic tracking-tight text-balance overflow-ellipsis line-clamp-1">{albumName}</span>

            <!-- Song name -->
            <span class="font-bold text-gray-200 text-4xl italic tracking-tight text-balance overflow-ellipsis line-clamp-3">{songName}</span>

            <!-- Artist name -->
            <span class="text-2xl text-gray-200 font-thin overflow-ellipsis line-clamp-2">{songArtists}</span>

        </div>
        <img class="h-full w-auto aspect-square rounded-lg" alt="The album cover for the album {albumName}" src={albumImg} id="aac" crossOrigin="anonymous" />

<!--        Queue -->
        <div class="flex flex-col min-w-45 bg-gray-800 rounded-md text-white">
            <span class="p-2 font-bold text-2xl">Up next</span>
            <hr class="">
        </div>

    </section>
{/if}
