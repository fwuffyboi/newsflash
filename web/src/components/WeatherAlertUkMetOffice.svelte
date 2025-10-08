<script lang="ts">
    import {onMount} from "svelte";
    import {weatherAlerts} from "../stores/weatherAlerts";

    let weather_alerts: any[] = $state([]);

    onMount(() => {
        fetch("http://192.168.0.226:8080/api/v1/weather/warnings/", { signal: AbortSignal.timeout(5000) })
            .then(response => response.json())
            .then(data => {
                console.log(data);

                // check if not empty
                if (data.warnings.length !== 0) {
                    weatherAlerts.set(data.warnings);
                    for (const element of data.warnings) {
                        weather_alerts.push({
                            'title': element.title,
                            'desc':  element.desc,
                            'level': element.level,
                            'link':  element.link,
                        });
                    }
                }
            });
    });
</script>

<!-- CurrentWeather Alert Area -->
{#if (weather_alerts.length > 0)}
    <section class=" flex flex-col h-auto min-w-60 max-w-140 rounded-lg grad p-3 from-amber-600 to-red-700 bg-linear-140 text-white">
        <div class="w-auto h-auto flex flex-row gap-2 pb-1">
            <img class="w-50 p-2" src="/mo-green-white.svg" alt="met office logo">
        </div>
        <div class="flex flex-col gap-2">
            {#each weather_alerts as wa_item}
                {#if wa_item.level !== 'Unknown'}

                    {#if wa_item.level === 'Yellow'}
                        <div class="rounded-xl bg-yellow-500 w-auto p-2">
                            <div class="flex flex-col">
                                <div class="animate-pulse">
                                    <span class="font-black text-lg tracking-tight">{wa_item.level} weather alert: </span>
                                    <span class="font-bold">{wa_item.title}</span>
                                </div>
                                <span class="font-light">{wa_item.desc}</span>

                            </div>

                        </div>
                    {/if}

                    {#if wa_item.level === 'Amber'}
                        <div class="rounded-xl bg-orange-500 w-auto p-2">
                            <div class="flex flex-col">
                                <div class="animate-pulse">
                                    <span class="font-black text-lg tracking-tight">{wa_item.level} weather alert: </span>
                                    <span class="font-bold">{wa_item.title}</span>
                                </div>
                                <span class="font-light">{wa_item.desc}</span>

                            </div>

                        </div>
                    {/if}

                    {#if wa_item.level === 'Red'}
                        <div class="rounded-xl bg-red-500 w-auto p-2">
                            <div class="flex flex-col">
                                <div class="animate-pulse">
                                    <span class="font-black text-lg tracking-tight">{wa_item.level} weather alert: </span>
                                    <span class="font-bold">{wa_item.title}</span>
                                </div>
                                <span class="font-light">{wa_item.desc}</span>

                            </div>

                        </div>
                    {/if}

                {/if}

                {#if wa_item.level === 'Unknown'}
                    <div class="rounded-xl bg-gray-400 w-auto p-2">
                        <div class="flex flex-col">
                            <div class="animate-pulse">
                                <span class="font-black text-lg tracking-tight">{wa_item.level} weather alert: </span>
                                <span class="font-bold">{wa_item.title}</span>
                            </div>
                            <span class="font-light">{wa_item.desc}</span>

                        </div>

                    </div>
                {/if}

            {/each}
        </div>
        <div class="p-2 pr-4 max-w-160 animate-pulse">
            <span class="text-red-300">DISCLAIMER!: Data is for informational purposes only and may be incorrect.</span>
        </div>
    </section>
{/if}