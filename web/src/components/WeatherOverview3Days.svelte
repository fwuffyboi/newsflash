<script>
    import {
        Cloud, Sun, CloudRain, CloudLightning,
        CloudDrizzle, CloudSnow, CloudFog, CloudAlert,
        Droplet, Wind, Sunrise, Sunset, TriangleAlert
    } from "lucide-svelte";
    import { weatherAlerts } from '../stores/weatherAlerts';
    let alerts = $state($weatherAlerts);

    import {onMount} from "svelte";

    let desc =       $state("Loading...");
    let loc =        $state("Loading...");
    let humidity =   $state(0);
    let sunrise =    $state(0);
    let sunset =     $state(0);
    let temp =       $state(0.0);
    let temp_str =   $state('??');
    let wind =       $state(7.77);
    let icon =       $state("01d");
    let units =      $state("Unknown");

    let bg_gradient = $state("")
    let lucide_icon = $state("")

    onMount(() => {
        fetch("http://192.168.0.226:8080/api/v1/weather/forecast/simplified", { signal: AbortSignal.timeout(5000) })
            .then(response => response.json())
            .then(data => {
                console.log(data);

                if (["01d", "01n", "02d", "02n"].includes(icon)) {
                    if (temp >= 18) {bg_gradient = "from-yellow-400 to-amber-600 bg-linear-150";
                        if (icon[2] === 'd') {lucide_icon = 'sun'} else {lucide_icon='cloud'}
                    } else {bg_gradient = "from-gray-400 to-gray-600 bg-linear-150";lucide_icon = 'cloud'}
                }

                else if (["03d", "03n", "04d", "04n"].includes(icon)) {
                    if (temp>=16) {
                        bg_gradient = "from-yellow-400 to-amber-600 bg-linear-150";lucide_icon='sun'
                    } else {
                        bg_gradient = "from-gray-400 to-gray-600 bg-linear-150";lucide_icon = 'cloud'
                    }
                }

                else if (["09d", "09n"].includes(icon)) {bg_gradient = "from-blue-400 to-gray-600 bg-linear-150";lucide_icon = 'rain'}

                else if (["10d", "10n"].includes(icon)) {bg_gradient = "from-blue-400 to-gray-400 bg-linear-150";lucide_icon = 'shower'}

                else if (["11d", "11n",].includes(icon)) {bg_gradient = "from-yellow-600 to-blue-200 to-blue-400 bg-linear-150";lucide_icon = 'thunder'}

                else if (["50d", "50n", "13d", "13n"].includes(icon)) {
                    bg_gradient = "from-gray-200 to-gray-500 bg-linear-160";
                    if (['50d', '50n'].includes(icon)) {lucide_icon = 'mist'} else {lucide_icon = 'snow'}
                }

                else {bg_gradient = "from-gray-400 to-gray-600 bg-linear-150";lucide_icon="cloud_err"}

            })
    });

</script>


<section class="flex flex-col min-w-75 max-w-110 h-70 rounded-xl grad p-4 {bg_gradient} text-white">

    <div class="flex flex-row gap-2 text-lg">
        <div class="flex flex-col">
            <div class="flex flex-row">
                {#if lucide_icon === "cloud"}
                    <Cloud size="30"/>
                {/if}
                {#if lucide_icon === "sun"}
                    <Sun size="30"/>
                {/if}
                {#if lucide_icon === "rain"}
                    <CloudDrizzle size="30"/>
                {/if}
                {#if lucide_icon === "shower"}
                    <CloudRain size="30"/>
                {/if}
                {#if lucide_icon === "thunder"}
                    <CloudLightning size="30"/>
                {/if}
                {#if lucide_icon === "mist"}
                    <CloudFog size="30"/>
                {/if}
                {#if lucide_icon === "snow"}
                    <CloudSnow size="30"/>
                {/if}
                {#if lucide_icon === "cloud_err"}
                    <CloudAlert size="30"/>
                {/if}
                <span class="italic text-gray-100 pl-2">Current weather in</span>
            </div>
            <div class="flex flex-row gap-2">
                <span class="font-bold text-xl">{loc}</span>
                {#if alerts.length > 0}
                    <!-- TODO/BUGFIX: doesnt show up sometimes and this is IMPORTANT -->
                    <TriangleAlert class="animate-pulse bg-red-500 rounded-md p-1" size="30" />
                {/if}
            </div>

        </div>


    </div>

    <div class="flex flex-row gap-2 ">

        <span class="text-7xl animate-pulse">{temp_str}°</span>

        <div class="flex flex-col">

            <span>{desc}</span>

            <div class="flex flex-row">
                <div class="flex flex-row">
                    <Droplet size="23"/>
                    <span>{humidity}%</span>
                </div>
                <div class="flex flex-row pl-2">
                    <Wind size="23"/>
                    <span class="pl-1">{wind}</span>
                </div>
            </div>
            <div class="text-gray-200"><span>All units in {units}</span></div>
        </div>

    </div>

    <div class="flex flex-row p-2 pl-1 gap-3">
        <div class="flex flex-row">
            <Sunrise />
            <span>{(new Date(sunrise*1000).toTimeString().substring(0,5))}</span>
        </div>
        <div class="flex flex-row">
            <Sunset />
            <span>{(new Date(sunset*1000).toTimeString().substring(0,5))}</span>
        </div>


    </div>

    <!-- Embed other air quality component-->
    <AirQuality />
    <div class="flex flex-row gap-1 pt-1 pl-1">
        <span class="text-gray-300">Last updated: </span>
        <span class="text-gray-300">{new Date().toLocaleTimeString([], { hour12: false }).toString().substring(0,5)}</span>
    </div>

</section>
