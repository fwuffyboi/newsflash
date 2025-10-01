<script>

    import {CloudAlert, Frown, Laugh, Meh, Smile} from "lucide-svelte";
    import {onMount} from "svelte";

    let aqi = $state(0);

    let message = $state('');
    let bg_gradient = $state('');

    onMount(() => {
        fetch("http://192.168.0.226:8080/api/v1/air-quality/current/", { signal: AbortSignal.timeout(5000) })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                console.log(data.aqi);
                aqi = data.aqi;

                if ([1,2,3,4,5].includes(aqi)) {
                    if (aqi === 1) {
                        bg_gradient = 'from-green-400 to-green-600';
                        message = 'Great air quality!'
                    } else if (aqi === 2) {
                        bg_gradient = 'from-green-400 to-yellow-400';
                        message = 'Good air quality!'
                    } else if (aqi === 3) {
                        bg_gradient = 'bg-amber-600';
                        message = 'Moderate air quality'
                    } else if (aqi === 4) {
                        bg_gradient = 'from-orange-400 to-amber-800';
                        message = 'Bad air quality!'
                    } else if (aqi === 5) {
                        bg_gradient = 'from-orange-500 to-red-600';
                        message = 'Hazardous air quality'
                    }
                } else {
                    bg_gradient = 'from-gray-400 to-gray-600';
                    message = 'AQI Error'
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