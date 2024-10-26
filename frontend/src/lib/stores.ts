import { writable, type Writable } from 'svelte/store';

export const theme: Writable<string> = writable("dark"); // Default theme is dark.

export const loginVisible: Writable<boolean> = writable(true);
export const signupMode: Writable<boolean> = writable(false);
