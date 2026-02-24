<script>
import {ScanFace} from "lucide-svelte";

let {FaceDetected, FaceNo, Status = "Processing...", Timeout} = $props();

function StatusFunc() {
    if (Status === "Ready") {
        return "text-green-400"
    } else if (Status === "Processing..." || Status === "Connecting...") {
        return "text-yellow-400"
    } else {
        return "text-red-500"
    }
}
</script>

<div class="w-60 max-h-5 flex flex-row gap-1 text-white">
    <div class="animate-pulse">
        <ScanFace size={48}/>
    </div>
<!-- todo: translate-->
    <div class="flex flex-col font-semibold tracking-tight">
        <span>Faces detected?: {FaceDetected} : {FaceNo}</span>
        <div class="flex flex-row gap-1">
            <span>Status:</span>
            <span class="{StatusFunc()} animate-pulse">{Status}</span>
            <span>TTE: {Timeout-Math.floor(Date.now() / 1000)}</span>
        </div>
    </div>

</div>