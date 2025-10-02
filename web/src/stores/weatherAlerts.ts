import { writable } from 'svelte/store';

export const weatherAlerts = writable<any[]>([]);