<script lang="ts">
	import { Carousel, Login } from "$lib/components/login";
	import { Form, LoginForm, RegistrationForm } from "$lib/components/login/form";
</script>

<Login>
	<Form>
		<LoginForm />
		<RegistrationForm />
	</Form>
	<Carousel />
</Login>
