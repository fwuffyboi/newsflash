<script>
    import {onMount} from "svelte";

    let { songName = "Loading..", songArtists = "Loading..", albumName = "Loading..", albumImg, duration = 1188125, songURL, nowPlaying = true, pgs = 0 } = $props();
    let progress   = $state();
    progress = pgs


    onMount(() => {
        progress = pgs;
        let startTime = Date.now() - progress;

        function animateProg() {
            if (!nowPlaying) return;
            const elapsed = Date.now() - startTime;
            progress = Math.min(elapsed, duration);
            if (progress < duration) {
                requestAnimationFrame(animateProg);
            }
        }

        animateProg();
    });

    // todo: leftover code, idk what to fuckin do with this
    function msToMinSec(millis) {
        let minutes;
        let seconds;

        minutes = Math.floor(millis / 60000);
        seconds = ((millis % 60000) / 1000).toFixed(0);
        return (
            seconds === "60" ?
                (minutes+1) + ":00" :
                minutes + ":" + (seconds < 10 ? "0" : "") + seconds
        );
    }

</script>


<!--This component handles the spotify integration.-->

<section class="h-50 max-h-full flex flex-row">

    <!-- Left side -->
    {#if songName === "Nothing is playing right now..."}
        <div class="flex flex-col gap-2 p-4 text-gray-200 text-right">
            <span class="font-bold text-4xl italic tracking-tight line-clamp-3">{songName}</span>
        </div>
    {/if}

            <!-- Progress Bar-->
            <!--<div class="flex flex-col gap-1">
                <div class="flex flex-col w-auto p-2 rounded-lg bg-gray-200">
                    <div class="flex flex-row justify-between text-black">
                        <p class="italic">{msToMinSec(progress)}</p>
                        <p>{msToMinSec(duration)}</p>
                    </div>
                    <progress
                            class="w-auto h-2 rounded-lg bg-gray-100"
                            value={progress}
                            max={duration}
                            id="progbar"
                    ></progress>
                </div>
            </div>-->

    {#if songName !== "Nothing is playing right now..."}
        <div class="flex flex-col gap-2 p-4 text-gray-200 text-right">

            <!-- Song name -->
            <span class="font-bold text-4xl italic tracking-tight text-balance mt-auto line-clamp-3">{songName}</span>

            <!-- Artist name -->
            <span class="text-2xl font-thin overflow-ellipsis line-clamp-2">{songArtists}</span>

        </div>
        <img class="h-full w-auto aspect-square bg-black border-gray-400 border-2 rounded-lg " alt="The album cover for the album {albumName}." src={albumImg} id="aac" crossOrigin="anonymous" />
    {/if}

</section>
