<script lang="ts">
	import user from '$lib/stores/user';
	import Login from '$lib/components/Login.svelte';

	$: isLoggedIn = $user === null ? false : true;

	const logout = () => {
		user.set(null);
	};
</script>

<h1>Welcome to TopicNet!</h1>
{#if isLoggedIn}
	<h2>Thank you {($user && $user.firstname) || 'User'} for logging in!</h2>
	<input type="button" value="Logout!" on:click={logout}>
{:else}
	<Login />
{/if}
