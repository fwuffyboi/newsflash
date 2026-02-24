<script>
// todo: translate this file
import {ScanFace} from "lucide-svelte";

let name = $props();
let message = $state("");
let lowerText = $state("fix me :3c");

let t = new Date().getHours();

if (t > 20) {       message='Good night ',     name, "!" }
else if (t >= 17) { message='Good evening ',   name, "!" }
else if (t >= 12) { message='Good afternoon ', name, "!" }
else if (t >= 5) {  message='Good morning ',   name, "!" }
else {              message='Good night ',     name, "!" }

if (t <= 4) {
    lowerText = 'good morning i guess'
} else {
    lowerText = 'Nice to see ya!'
}


</script>

<div class="justify-center items-center">

    <div class="flex flex-col text-white mr-5  tracking-tight">
        <div class="flex flex-row gap-2 text-4xl">
            <div class="animate-pulse">
                <ScanFace size={45} />
            </div>
            <span class="font-black">{message}</span>

        </div>

        <span class="text-gray-400 animate-pulse text-lg pl-0.5">{lowerText}</span>


    </div>

</div>