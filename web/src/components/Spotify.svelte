<script>
    import {DiscAlbum, Music, Music2} from "lucide-svelte";
    import ColorThief from 'colorthief';
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

<section class="w-5/6 h-50 flex flex-row">

    <img class="h-full w-auto aspect-square bg-black rounded-l-2xl rounded-tr-2xl" alt="The album cover for the album {albumName}." src={albumImg} id="aac" crossOrigin="anonymous" />

    <!-- Right side -->
    <div class="grow h-4/5 bg-gray-100 my-10 rounded-r-2xl">

        <div class="p-3">
            <div class="flex flex-col gap-1 pl-2 text-black">

                <!-- Song name -->
                <div class="flex flex-row gap-1">
                    <span class="gap-4 text-black items-center">
                    <span class="font-bold italic">{songName}</span>
                </span>
                </div>

                <!-- Album name -->
                <div class="flex flex-row gap-1">

                    <span class="gap-4 text-black items-center">
                    <span class="">{albumName}</span>
                </span>
                </div>

                <!-- Artist name -->
                <div class="flex flex-row gap-1">
                    <span class="gap-4 text-black items-center">
                    <span class="font-stretch-50% italic">{songArtists}</span>
                </span>
                </div>

            </div>

            <!-- Progress Bar-->
            <div class="flex flex-col gap-1">
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
            </div>

        </div>



    </div>

</section>
