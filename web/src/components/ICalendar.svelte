<script>
    import {onMount} from "svelte";
    import {m} from "$lib/paraglide/messages.js"
    import {getLocale} from "$lib/paraglide/runtime.js";

    let events = $state();
    let message = $state();
    let d = new Date();

    onMount(() => {
        fetch("http://127.0.0.1:8080/api/v1/ical/", { signal: AbortSignal.timeout(5000) })
            .then(response => response.json())
            .then(data => {

                events = data.next_events;
                message = data.error;

            })
    });

    function Coie (hasEnded) {
        if (hasEnded) {
            return "line-through"
        } else {
            return ""
        }
    }

</script>

<section class="h-fit w-125 rounded-md bg-gradient-to-tr from-blue-950 to-cyan-950">

    <div class="pt-2 px-3 text-white font-bold text-lg">
        <span class="underline">{m.ical_today()}, {d.getDate()} {d.toLocaleString(getLocale(), { month: 'long' })} {d.getFullYear()}</span>
    </div>

    <div class="flex flex-col rounded-lg pl-4 pb-4 pt-1 text-white">
        <div class="flex flex-col">

            {#each events as e}
                <div class="max-w-120 pb-3">

                    <div class="{Coie(e.hasEnded)}">

                        <div class="flex flex-col">
                            <div class="flex flex-row justify-between pr-4">
                                <span>{e.title}</span>
                                <span>{e.start} - {e.end}</span>
                            </div>
                            {#if e.desc.length > 0}
                                <div class="flex flex-row line-clamp-2 italic font-thin">
                                    <span class="font-bold">{m.ical_desc()}:&nbsp;</span>
                                    <span>{e.desc}</span>
                                </div>
                            {/if}

                            {#if e.location.length > 0}
                                <div class="flex flex-row line-clamp-2 italic font-thin">
                                    <span class="font-bold">{m.ical_location()}:&nbsp;</span>
                                    <span>{e.location}</span>
                                </div>
                            {/if}

                        </div>

                    </div>

                    <hr class="w-85">

                </div>
            {/each}
            <!-- todo {#if not events}-->
            <!--    <span>Theres no events today! Enjoy a clear calendar!</span>-->
            <!--{/if}-->

        </div>
    </div>

</section>