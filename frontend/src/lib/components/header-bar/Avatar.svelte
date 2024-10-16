<script lang="ts">
	import { createAvatar, melt } from "@melt-ui/svelte";

	export let profile = {
		firstname: "",
		lastname: "",
		picture: ""
	}

	const getInitials = (firstname: string, lastname: string) => {
		const firstInitial: string = firstname ? firstname.charAt(0).toUpperCase() : "";
		const lastInitial: string = lastname ? lastname.charAt(0).toUpperCase() : "";
		return `${firstInitial}${lastInitial}`;
	}

	let avatarSrc: string = profile.picture ? profile.picture : getInitials(profile.firstname, profile.lastname);

	const {
		elements: { image, fallback }
	} = createAvatar({
		src: avatarSrc,
		delayMs: 0
	});
</script>

<div class="flex h-16 items-center justify-center w-16">
	<img use:melt={$image} alt="Avatar" class="h-full rounded-[inherit] w-full" />
	<span use:melt={$fallback} class="font-medium text-3xl">{getInitials(profile.firstname, profile.lastname)}</span>
</div>

<style>
	div {
		background-color: var(--color-surface-200);
		border-radius: var(--theme-rounded-container);
		z-index: var(--theme-z-index-fixed);
	}

	img {
		object-fit: cover;
	}

	span {
		color: var(--color-primary-700);
		font-family: var(--theme-font-family-logo);
	}
</style>
