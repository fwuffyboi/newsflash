<script>
    import {LocateFixedIcon, Cloud} from "lucide-svelte";

    let desc = "overcast clouds";
    let loc = "Twickenham";
    let humidity = 90;
    let sunrise = 1757136132;
    let sunset = 1757183852;
    let temp = 14.95;
    let wind = 2.57;
    let time = "08:41";
    let day = "Saturday";
    let icon = "01d";
    let weather_alerts = ["Yemlow warmimg :cc it wainy...."];
</script>


<section class="flex flex-col h-auto w-auto rounded-2xl bg-blue-500 p-4">

    <div class="flex flex-row gap-2">
        <LocateFixedIcon/>
        <p class="italic">{loc}</p>
    </div>

    <div class="flex flex-row gap-2">
        <Cloud class=""/>
    </div>

</section>


{#if (weather_alerts.length !== 0)}
    <section class="flex flex-row gap-2">

    </section>
{/if}
