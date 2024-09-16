<script lang="ts">
	import user from '$lib/stores/user';

	let username: string = '';
	let password: string = '';
	let currentError: string = '';

	const login = async () => {
		fetch('http://localhost:8080/api/v1/login', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ username, password })
		})
		.then(response => {
			if (response.ok) {
				return response.json();
			} else {
				currentError = 'Invalid username or password!';
			}
		})
		.then(data => {
			user.update(u => u = data);
		})
		.catch(error => {
			currentError = error;
			console.error(error);
		});
	};
</script>

<form on:submit|preventDefault={login}>
	<div>
		<label for="username">Username</label>
		<input type="text" id="username" bind:value={username} />
	</div>
	<div>
		<label for="password">Password</label>
		<input type="password" id="password" bind:value={password} />
	</div>
	<button type="submit">Submit</button>
</form>
