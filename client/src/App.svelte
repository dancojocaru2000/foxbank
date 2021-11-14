<script>
	import Card from "./Card.svelte";


	export let name;
</script>

<main>
	<h1 class="text-yellow-400">Hello {name}!</h1>
	<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
	<Card title="Test" text="123"></Card>
	<Card title="Test 2" text="Hello, world!"></Card>
</main>

<style global lang="postcss">
	@tailwind base;
	@tailwind components;
	@tailwind utilities;
</style>