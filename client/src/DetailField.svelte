<script>
	export let width = "inherit";
	export let height = "inherit";

	let clazz;
	export {clazz as class}
</script>

<main class="rounded-x {clazz}" style="--width: {width}; --height: {height};">
	<slot></slot>
</main>

<style>
	main{
		width: var(--width);
		height: var(--height);

		background: linear-gradient(92.55deg, rgba(76, 172, 135, 0.95) -28.27%, rgba(249, 224, 127, 0.096) 115.79%);
		filter: drop-shadow(0px 8px 4px rgba(0, 0, 0, 0.25));
		border-radius: 3px;
	}

</style>
