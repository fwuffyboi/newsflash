<script lang="ts">
    import {onMount} from "svelte";

    let tfld = {};

    const lineColour = {
        Bakerloo: "bg-orange-800",
        Central: "bg-red-500",
        Circle: "bg-yellow-400",
        District : "bg-green-800",
        "Hammersmith & City": "bg-pink-300",
        Jubilee: "bg-gray-400",
        Metropolitan: "bg-purple-800",
        Northern: "bg-black",
        Piccadilly: "bg-blue-900",
        Victoria: "bg-blue-500",
        "Waterloo & City": "bg-blue-300"
    }

    onMount(()=> {
        fetch("http://192.168.0.226:8080/api/v1/transport/tfl/train-status/", { signal: AbortSignal.timeout(5000) })
            .then(response => response.json())
            .then(data => {
                // todo: if line says "Part Suspended" it will push out further

                tfld = data.data;
                console.log(tfld);
                console.log(Object.entries(tfld))
            })
    })

</script>

<section class="">
    <div class="flex flex-col w-auto h-70 bg-gray-600 rounded-md p-1.5">

<!-- All train lines go below -->
        {#each Object.entries(tfld) as [lineName, lineStatus], index}
            <div class="flex flex-row {index % 2 ? '' : 'bg-gray-500' } rounded-md">
                <div class="h-6 w-21 flex flex-row {lineColour[lineName]} {index === 0 ? 'rounded-t-md' : ''} {index === 10 ? 'rounded-b-md' : ''} text-white pl-1">
                    <span class="font-semibold tracking-tight truncate">{lineName}</span>
                </div>
                <div class="text-white pl-1 max-w-26 tracking-tight font-sans pr-2 truncate">
                    <span>{lineStatus.status}</span>
                </div>
            </div>
        {/each}

    </div>
</section>