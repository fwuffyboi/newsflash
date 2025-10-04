<script lang="ts">
    import {getLocale, setLocale} from '$lib/paraglide/runtime';
    import { m } from '$lib/paraglide/messages.js';
</script>

<div class="flex flex-col bg-white w-screen h-screen items-center">
    <span class="text-3xl mt-40 italic">{m.locale_changed({ locale: getLocale() })}</span>
    <span class="font-bold text-lg">{m.choose_locale({})}</span>
    <div class="flex flex-col gap-2">
        <button onclick={() => setLocale('en')}>en</button>
        <button onclick={() => setLocale('ru')}>ru</button>
        <button onclick={() => setLocale('pl')}>pl</button>
        <button onclick={() => setLocale('ie')}>ie</button>
    </div>
    <span class="font-medium">{m.back_to_main_page_locale()}<a href="/">__/__</a>.</span>
</div>