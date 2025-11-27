<script>

    import {m} from "$lib/paraglide/messages.js"
    import {LaptopMinimal, Smartphone, Speaker} from "lucide-svelte";

    let { songName, songArtists, albumName, albumImg, nowPlaying = true, devicetype, devicename, queue = []} = $props();

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
        <div class="flex flex-col pr-1 text-right">

            <!-- Song name -->
            <div class="flex flex-col gap-2 text-white text-right ml-auto">
                <img class="w-11 ml-auto" src="/spotify_logo_white.svg" alt="">

                <div class="flex flex-row gap-1 ml-auto text-green-500">

                    {#if devicetype==="Computer"}
                        <LaptopMinimal/>
                    {:else if devicetype==="Smartphone"}
                            <Smartphone/>
                    {:else}
                        <Speaker/>
                    {/if}

                    <span>{devicename}</span>
                </div>


            </div>

            <span class="font-light text-gray-300 italic tracking-tight animate-pulse mt-auto">{m.spotify_now_playing()}</span>
            <span class="font-bold text-white text-4xl italic tracking-tight text-balance overflow-ellipsis line-clamp-2">{songName}</span>

            <!-- Artist name -->
            <span class="text-2xl text-white font-thin overflow-ellipsis line-clamp-2">{songArtists}</span>

        </div>
        <img class="h-full w-auto aspect-square rounded-lg" alt="The album cover for the album {albumName}" src={albumImg} id="aac" crossOrigin="anonymous" />

<!--        Queue -->
        <div class="flex flex-col w-50 bg-black rounded-md text-white">
            <span class="px-2 pb-0.5 font-black italic text-2xl">{m.spotify_up_next()}</span>
            <hr class="">

            {#each queue as q}
                <div class="flex flex-row gap-1 px-1 truncate">
                    <div class="max-w-10 pt-2 aspect-square">
                        <img class="rounded-sm" src={q.cover} alt="">
                    </div>
                    <div class="pt-0.5 flex flex-col truncate">
                        <span class="font-semibold">{q.track_name}</span>
                        <span class="italic">{q.artists}</span>
                    </div>
                </div>
            {/each}

        </div>

    </section>
{/if}
