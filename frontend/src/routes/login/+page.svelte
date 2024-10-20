<script lang="ts">
	import { Carousel, Login } from "$lib/components/login_and_registration";
	import { Form, LoginForm, RegistrationForm } from "$lib/components/login_and_registration/form";
</script>

<Login>
	<Form>
		<LoginForm />
		<RegistrationForm />
	</Form>
	<Carousel />
</Login>
