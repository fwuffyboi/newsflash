<script>
    import {onMount} from "svelte";
    import {m} from "$lib/paraglide/messages.js"
    import {CalendarFold} from "lucide-svelte";

    let events = $state([
        {
            "desc": "",
            "duration": "",
            "end": "",
            "hasEnded": false,
            "location": "",
            "start": "",
            "title": "Loading events...",
        }
    ]);
    let message = $state();
    let d = new Date();

    onMount(() => {
        fetch("http://localhost:4000/api/v1/ical/", { signal: AbortSignal.timeout(8000) })
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

    function allday (start, end) {
        if (start === "" && end === "") {
            return "bg-blue-500"
        }
    }

</script>

<section class="h-fit w-100 max-w-127 rounded-md bg-gradient-to-tr from-blue-800 to-cyan-900">

    <div class="pt-2 px-3 pb-1 flex flex-row text-white font-bold text-lg ">
        <CalendarFold size="25" />
<!--        <span class="pl-1 underline">{m.ical_today()}, {d.getDate()} {d.toLocaleString(getLocale(), { month: 'long' })} {d.getFullYear()}</span>-->
        <span class="pl-1 underline">{m.ical_today()}</span>

    </div>

    <div class="flex flex-col rounded-lg pl-2 pb-4 pt-1 text-white">
        <div class="flex flex-col max-w-160">

            {#each events as e}
                <div class="{Coie(e.hasEnded)} pb-1">
                    <div class="flex flex-col">
                        <div class="flex flex-row justify-between pr-4">

                            <span class="w-67 truncate font-semibold pl-2 rounded-md {allday(e.start, e.end)}">{e.title}</span>

                            {#if e.start !== "" && e.end !== ""}
                                <span>{e.start} - {e.end}</span>
                            {/if}

                        </div>

                        <!--{#if e.desc.length > 0}-->
                        <!--    <div class="flex flex-row line-clamp-2 italic font-thin">-->
                        <!--        <span class="font-bold">{m.ical_desc()}:&nbsp;</span>-->
                        <!--        <span>{e.desc}</span>-->
                        <!--    </div>-->
                        <!--{/if}-->

                        {#if e.location.length > 0}
                            <div class="flex flex-row line-clamp-2 italic font-thin tracking-tighter">
<!--                                <span class="font-semibold">{m.ical_location()}:&nbsp;</span>-->
                                <span>{e.location}</span>
                            </div>
                        {/if}

                    </div>
                </div>
            {/each}

        </div>
    </div>

</section>