<script lang="ts">
    import {onMount} from "svelte";

    import {TriangleAlert} from "lucide-svelte";

    let weather_alerts: any[] = $state([]);

    onMount(() => {
        fetch("http://localhost:4000/api/v1/weather/warnings/", { signal: AbortSignal.timeout(5000) })
            .then(response => response.json())
            .then(data => {
                // console.log(data);

                // check if not empty
                if (data.warnings.length !== 0) {
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

    function bgColour(color: string) {
        if (color === "Red") {
            return "bg-red-500"
        } else if (color === "Amber") {
            return "bg-orange-500"
        } else if (color === "Yellow") {
            return "bg-amber-400"
        } else if (color === "Unknown") {
            return "bg-"
        } else {
            return "bg-amber-500"
        }
    }
</script>

<!-- CurrentWeather Alert Area -->
{#if (weather_alerts.length > 0)}
    <section class="flex flex-col h-auto text-white">

        <div class="flex flex-col gap-2 max-w-127">
            {#each weather_alerts as wa_item}
                <div class="rounded-lg {bgColour(wa_item.level)} w-auto p-2 pt-1">
                    <div class="flex flex-col">
                        <div class="flex flex-row gap-2">
                            <TriangleAlert class="animate-pulse rounded-md p-0.5" size={56} />
                            <span class="text-lg font-bold">{wa_item.title}</span>
                        </div>
                        <hr>
                        <span>{wa_item.desc}</span>
                    </div>
                </div>
            {/each}
        </div>

    </section>
{/if}