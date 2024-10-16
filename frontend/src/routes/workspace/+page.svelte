<script lang="ts">
	import Board from "$lib/components/Board.svelte";
	import { Avatar, HeaderBar, Logo } from "$lib/components/header-bar";

	let profile = {
		firstname: "John",
		lastname: "Doe",
		picture: ""
	};
</script>

<HeaderBar>
	<Logo logoText="TopicNet" />
	<Avatar {profile} />
</HeaderBar>
<Board />
