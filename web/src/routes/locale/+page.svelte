<script lang="ts">
    import {getLocale, setLocale} from '$lib/paraglide/runtime';
    import { m } from '$lib/paraglide/messages.js';
</script>

<div class="flex flex-col bg-white w-screen h-screen items-center">
    <span class="text-3xl mt-40 italic">{m.locale_changed({ locale: getLocale() })}</span>
    <span class="font-bold text-lg">{m.locale_choose({})}</span>
    <div class="flex flex-col gap-2 underline">
			<button onclick={() => setLocale('en')}>English</button>
			<button onclick={() => setLocale('ru')}>Русский</button>
			<button onclick={() => setLocale('pl')}>Polski</button>
			<button onclick={() => setLocale('ie')}>Gaeilge</button>
			<button onclick={() => setLocale('shavian')}>𐑖𐑱𐑝𐑰𐑩𐑯</button>
    </div>
    <span class="font-medium">{m.locale_back_home()}<a href="/">__/__</a>.</span>
</div>