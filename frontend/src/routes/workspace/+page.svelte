<script>
	import { Board, Node, Toggle } from '$lib/components/workspace';
	import { Header } from '$lib/components/header';
	import { Nav, NavLogo } from '$lib/components/header/nav';
	import { NavActions, NavLogin } from '$lib/components/header/nav/actions';

	let testMarkdown = `
# Sample Heading

- List item 1
- List item 2
- **Bold Text** in markdown
- *Italic Text* in markdown

1. Ordered List item 1
2. Ordered List item 2

[Link to Google](https://www.google.com)
	`;
</script>

<Header>
	<Nav>
		<NavLogo />
		<NavActions>
			<Toggle />
			<NavLogin />
		</NavActions>
	</Nav>
</Header>
<Board />
<Node content={testMarkdown} customStyles="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);" />
