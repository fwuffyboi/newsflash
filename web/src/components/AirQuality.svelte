<script>

    import {CloudAlert, Frown, Laugh, Meh, Smile} from "lucide-svelte";
    import {onMount} from "svelte";
    import {m} from "$lib/paraglide/messages.js"

    let aqi = $state(0);

    let message = $state('');
    let bg_gradient = $state('');

    onMount(() => {
        fetch("http://localhost:4000/api/v1/air-quality/current/", { signal: AbortSignal.timeout(5000) })
            .then(response => response.json())
            .then(data => {
                aqi = data.data.aqi;

                if ([1,2,3,4,5].includes(aqi)) {
                    if (aqi === 1) {
                        bg_gradient = 'from-green-400 to-green-600';
                        message = m.aqi_great_air_quality();
                    } else if (aqi === 2) {
                        bg_gradient = 'from-green-400 to-yellow-300';
                        message = m.aqi_good_air_quality();
                    } else if (aqi === 3) {
                        bg_gradient = 'bg-amber-600';
                        message = m.aqi_moderate_air_quality();
                    } else if (aqi === 4) {
                        bg_gradient = 'from-orange-400 to-amber-800';
                        message = m.aqi_bad_air_quality();
                    } else if (aqi === 5) {
                        bg_gradient = 'from-orange-500 to-red-600';
                        message = m.aqi_hazardous_air_quality();
                    }
                } else {
                    bg_gradient = 'from-gray-400 to-gray-600';
                    message = m.aqi_error();
                }
            })
    });

</script>

<section class="{bg_gradient} bg-linear-150 min-w-10 max-w-65 w-fit h-10 rounded-lg text-white">

    <div class="flex flex-row rounded-lg p-1 gap-1.5">
        <span class="font-bold pt-1 pl-1 font-4xl">{message}</span>

        {#if aqi === 1}
            <Laugh size="32"/>
        {/if}
        {#if aqi === 2}
            <Smile size="32"/>
        {/if}
        {#if aqi === 3}
            <Meh   size="32" />
        {/if}
        {#if aqi === 4}
            <Frown size="32"/>
        {/if}
        {#if aqi === 5}
            <Frown size="32"/>
        {/if}
        {#if message==="AQI Error"}
            <CloudAlert size="30" />
        {/if}
    </div>

</section>