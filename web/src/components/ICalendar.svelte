<script>
    import {onMount} from "svelte";
    import {m} from "$lib/paraglide/messages.js"
    import {getLocale} from "$lib/paraglide/runtime.js";
    import {CalendarFold} from "lucide-svelte";

    let events = $state([
        {
            "desc": "Loading...",
            "duration": "24:00:00",
            "end": "24:00",
            "hasEnded": false,
            "location": "",
            "start": "00:00",
            "title": "Loading...",
        }
    ]);
    let ecount = $derived(events.length);
    let message = $state();
    let d = new Date();

    onMount(() => {
        fetch("http://192.168.0.226:8080/api/v1/ical/", { signal: AbortSignal.timeout(8000) })
            .then(response => response.json())
            .then(data => {

                events = data.next_events;
                // console.log(events);
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

<section class="h-fit w-100 max-w-127 rounded-md bg-gradient-to-tr from-blue-800 to-cyan-900">

    <div class="pt-2 px-3 pb-1 flex flex-row text-white font-bold text-lg ">
        <CalendarFold size="25" />
        <span class="pl-1 underline">{m.ical_today()}, {d.getDate()} {d.toLocaleString(getLocale(), { month: 'long' })} {d.getFullYear()}</span>

    </div>

    <div class="flex flex-col rounded-lg pl-4 pb-4 pt-1 text-white">
        <div class="flex flex-col">

            {#each events as e}
                <div class="max-w-120">

                    <div class="{Coie(e.hasEnded)}">
                        <div class="flex flex-col">
                            <div class="flex flex-row justify-between pr-4">
                                <span class="truncate font-semibold">{e.title}</span>
                                <span>{e.start} - {e.end}</span>
                            </div>

                            <!--{#if e.desc.length > 0}-->
                            <!--    <div class="flex flex-row line-clamp-2 italic font-thin">-->
                            <!--        <span class="font-bold">{m.ical_desc()}:&nbsp;</span>-->
                            <!--        <span>{e.desc}</span>-->
                            <!--    </div>-->
                            <!--{/if}-->

                            {#if e.location.length > 0}
                                <div class="flex flex-row line-clamp-2 italic font-thin tracking-tighter">
<!--                                    <span class="font-semibold">{m.ical_location()}:&nbsp;</span>-->
                                    <span>{e.location}</span>
                                </div>
                            {/if}

                        </div>
                    </div>

                </div>
            {/each}
            <!-- todo {#if not events}-->
            <!--    <span>Theres no events today! Enjoy a clear calendar!</span>-->
            <!--{#if ecount = 0}-->
            <!--    <span>no events :c</span>-->
            <!--{/if}-->

        </div>
    </div>

</section>