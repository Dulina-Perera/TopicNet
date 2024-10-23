import { type Writable, writable } from 'svelte/store';

export const isVisible: Writable<boolean> = writable(false);
