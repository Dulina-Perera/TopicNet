import { writable, type Writable } from "svelte/store";

const user: Writable<null> = writable(null);

export default user;
