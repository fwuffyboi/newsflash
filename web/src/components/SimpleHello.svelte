<script>
    let name = "Ashley";
    let message = $state("");

    let t = new Date().getHours();

    if (t > 20) {       message='Good night, '     + name + "!" }
    else if (t >= 17) { message='Good evening, '   + name + "!" }
    else if (t >= 12) { message='Good afternoon, ' + name + "!" }
    else if (t >= 5) {  message='Good morning, '   + name + "!" }
    else {              message='Good night, '     + name + "!" }

    if (new Date().getMonth() === 11) { //december
        if (new Date().getDate() === 7) {
            // it's Ashley's birthday!!! say it's Ashley's birthday :3c.
            message = "Happy Birthday, " + name + "!!!!"
        }
    }
</script>

<div class="">

    <div class="flex flex-col text-white">
        <div class="flex flex-row gap-2 text-lg">
            <span class="font-white">{message}</span>
        </div>
    </div>

</div>