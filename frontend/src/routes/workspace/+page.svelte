<script lang="ts">
	import { type Writable, writable } from 'svelte/store';
	import { Node, Tree } from '$lib/components/workspace';
	import { Header, Logo } from '$lib/components';
	import { LoginButton } from '$lib/components/login';
	import { NavActions } from '$lib/components/nav';

	let loading: Writable<boolean> = writable(true);
	let content: Writable<string> = writable(`
# Understanding Cognitive Analytics: Enhancing Decision-Making with Human-Like Intelligence

Cognitive analytics leverages advanced technologies to uncover patterns and connections in data that traditional analytics cannot. By integrating artificial intelligence, machine learning, deep learning, and natural language processing, cognitive analytics mimics human-like intelligence, enabling it to tackle complex problems that fixed programming instructions cannot solve.

Cognitive systems continuously improve through self-learning from interactions with data and users, allowing them to analyze large datasets and provide structured insights from unstructured data. These systems can generate hypotheses from diverse data sources, offering real-time answers and insights that can create a competitive advantage for businesses.

Organizations can utilize cognitive analytics to monitor customer behavior and emerging trends, facilitating predictive analytics that inform future strategies and enhance performance. The adaptive nature of cognitive computing allows it to evolve alongside changing information and requirements, making it a powerful tool for decision-making.

Cognitive systems must be interactive, enabling users to define their needs easily and integrate with various data sources and devices. They
`);
</script>

<Header>
	<Logo />
	<NavActions>
		<LoginButton />
	</NavActions>
</Header>

<Tree>
	<ul>
		<li>
			<Node content={$content} />
			<ul>
				<li>
					<Node content={$content} />
					<ul>
						<li><Node content={$content} /></li>
						<li><Node content={$content} /></li>
					</ul>
				</li>
				<li><Node content={$content} /></li>
				<li>
					<Node content={$content} />
					<ul>
						<li><Node content={$content} /></li>
						<li><Node content={$content} /></li>
						<li><Node content={$content} /></li>
					</ul>
				</li>
			</ul>
		</li>
	</ul>
</Tree>

<style lang="scss">
	ul {
		display: flex;
		flex-wrap: nowrap;
		justify-content: center;
		padding-top: 20px;
		position: relative;
		transition: all 0.4s;

		&:not(:first-of-type)::before {
			border-left: 4px solid var(--theme-border-color);
			content: '';
			height: 20px;
			left: 50%;
			position: absolute;
			top: 0;
			width: 0;
		}
	}

	li {
		align-items: center;
		display: inline-flex;
		flex-direction: column;
		list-style-type: none;
		min-width: 100px;
		padding: 10px 20px;
		position: relative;
		transition: all 0.4s;

		&::after,
		&::before {
			border-top: 4px solid var(--theme-border-color);
			content: '';
			position: absolute;
			width: 50%;
			top: 0;
		}

		&::before {
			right: 50%;
		}

		&::after {
			left: 50%;
		}

		ul::before {
			border-left: 4px solid var(--theme-border-color);
			content: '';
			height: 20px;
			left: 50%;
			position: absolute;
			top: 0;
			width: 0;
		}

		&:first-child::before,
		&:last-child::after {
			border-top: none;
		}
	}
</style>
