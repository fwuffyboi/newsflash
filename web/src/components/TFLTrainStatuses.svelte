<script lang="ts">
    import {onMount} from "svelte";

    let bak={}, cen={}, cir={}, dis={}, hac={}, jub={}, met={}, nor={}, pic={}, vic={}, wac = {};

    onMount(()=> {
        fetch("http://192.168.0.226:8080/api/v1/transport/tfl/train-status/", { signal: AbortSignal.timeout(5000) })
            .then(response => response.json())
            .then(data => {
                bak = data.data.Bakerloo;
                cen = data.data.Central;
                cir = data.data.Circle;
                dis = data.data.District;
                hac = data.data["Hammersmith & City"];
                jub = data.data.Jubilee;
                met = data.data.Metropolitan;
                nor = data.data.Northern;
                pic = data.data.Piccadilly;
                vic = data.data.Victoria;
                wac = data.data["Waterloo & City"];
            })
    })

</script>

<section class="">
    <div class="flex flex-col w-auto h-70 bg-gray-600 rounded-md p-1.5">

        <!-- All train lines go below -->
        <div class="flex flex-row">
            <div class="h-6 w-20 flex flex-row bg-orange-800 rounded-t-md text-white pl-1">
                <span class="font-semibold tracking-tight">Bakerloo</span>
            </div>
            <div class=" text-white pl-1 tracking-tight font-sans pr-2">
                <span>{bak.status}</span>
            </div>
        </div>

        <div class="flex flex-row bg-gray-700 rounded-r-md">
            <div class="h-6 w-20 flex flex-row bg-red-500 text-white pl-1">
                <span class="font-semibold tracking-tight">Central</span>
            </div>
            <div class=" text-white  pl-1 tracking-tight font-sans pr-2">
                <span>{cen.status}</span>
            </div>
        </div>

        <div class="flex flex-row">
            <div class="h-6 w-20 flex flex-row bg-yellow-400  text-white pl-2">
                <span class="font-semibold tracking-tight">Circle</span>
            </div>
            <div class=" text-white pl-1 tracking-tight font-sans pr-1">
                <span>{cir.status}</span>
            </div>
        </div>

        <div class="flex flex-row bg-gray-700 rounded-r-md">
            <div class="h-6 w-20 flex flex-row bg-green-800  text-white pl-1">
                <span class="font-semibold tracking-tight font-sans">District</span>
            </div>
            <div class=" text-white pl-1 tracking-tight font-sans pr-2">
                <span>{dis.status}</span>
            </div>
        </div>

        <div class="flex flex-row">
            <div class="h-6 w-20 flex flex-row bg-pink-300  text-white pl-1">
                <span class="font-semibold tracking-tight font-sans">H'sm. & C.</span>
            </div>
            <div class=" text-white pl-1 tracking-tight font-sans pr-2">
                <span>{hac.status}</span>
            </div>
        </div>

        <div class="flex flex-row bg-gray-700 rounded-r-md">
            <div class="h-6 w-20 flex flex-row bg-gray-400  text-white pl-1">
                <span class="font-semibold tracking-tight font-sans">Jubilee</span>
            </div>
            <div class=" text-white pl-1  tracking-tight font-sans pr-2">
                <span>{jub.status}</span>
            </div>
        </div>

        <div class="flex flex-row">
            <div class="h-6 w-20 flex flex-row bg-purple-800  text-white pl-1">
                <span class="font-semibold tracking-tight font-sans">Met'pol'n.</span>
            </div>
            <div class=" text-white pl-1 tracking-tight font-sans pr-2">
                <span>{met.status}</span>
            </div>
        </div>

        <div class="flex flex-row bg-gray-700 rounded-r-md">
            <div class="h-6 w-20 flex flex-row bg-black  text-white pl-1">
                <span class="font-semibold tracking-tight font-sans">Northern</span>
            </div>
            <div class=" text-white pl-1  tracking-tight font-sans pr-2">
                <span>{nor.status}</span>
            </div>
        </div>

        <div class="flex flex-row">
            <div class="h-6 w-20 flex flex-row bg-blue-900  text-white pl-1">
                <span class="font-semibold tracking-tight font-sans">Piccadilly</span>
            </div>
            <div class=" text-white pl-1 tracking-tight font-sans pr-2">
                <span>{pic.status}</span>
            </div>
        </div>

        <div class="flex flex-row bg-gray-700 rounded-r-md">
            <div class="h-6 w-20 flex flex-row bg-blue-500  text-white pl-1">
                <span class="font-semibold tracking-tight font-sans">Victoria</span>
            </div>
            <div class=" text-white pl-1 tracking-tight font-sans pr-2">
                <span>{vic.status}</span>
            </div>
        </div>

        <div class="flex flex-row">
            <div class="h-6 w-20 flex flex-row bg-blue-300 rounded-b-md text-white pl-1">
                <span class="font-semibold tracking-tight font-sans">W'loo & C.</span>
            </div>
            <div class=" text-white pl-1 tracking-tight font-sans pr-2">
                <span>{wac.status}</span>
            </div>
        </div>

    </div>
</section>