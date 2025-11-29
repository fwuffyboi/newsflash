<script>
// todo: translate this file
import {ScanFace} from "lucide-svelte";

let greeting = $props(); // This decides if we are saying hello or goodbye.

let message = $state("");
let lowerText = $state("fix me :3c");

let t = new Date().getHours();

if (greeting === true) {
    if (Math.random() > 0.4) {
        // 60% chance this happens

        if (t > 20) {       message='Good night!'          }
        else if (t >= 17) { message='Good evening!'        }
        else if (t >= 12) { message='Good afternoon!'      }
        else if (t >= 5) {  message='Good morning!'        }
        else {              message='Go (back) to sleep!!' }

        // todo: change the messages around, add more and fix lowerText to be more reactive/do more.
    } else {
        if (Math.random() > 0.5) {
            // 20% this happens instead
            message = 'Heya!';
        } else {
            message = 'Nice to see you!';
        }
    }

    if (t <= 4) {
        lowerText = 'good morning i guess'
    }
} else {
    if (Math.random() > 0.4) {
        // 60% chance this happens

        if (t > 20) {       message='Good night!'           }
        else if (t >= 17) { message='Enjoy your evening!'   }
        else if (t >= 12) { message='Enjoy your afternoon!' }
        else if (t >= 5) {  message='Enjoy your morning!'   }
        else {              message='thats what i thought.' }

        // todo: change the messages around, add more and fix lowerText to be more reactive/do more.
    } else {
        if (Math.random() > 0.5) {
            // 20% this happens instead
            message = 'See ya!';
        } else {
            message = 'Bye Bye!';
        }
    }
}

</script>

<section class="justify-center items-center">

        <div class="flex flex-col text-white mr-5  tracking-tight">
            <div class="flex flex-row gap-2 text-4xl">
                <div class="animate-pulse">
                    <ScanFace size={45} />
                </div>
                <span class="font-black">{message}</span>

            </div>

            <span class="text-gray-400 animate-pulse text-lg pl-0.5">{lowerText}</span>


        </div>

</section>