<script>
	export let width;
	export let height;

	let clazz;
	export {clazz as class}
</script>

<main>
	<figure class="rounded-x p-3 m-14 {clazz}" style="--width: {width}; --height: {height};">
		<slot></slot>
	</figure>
</main>

<style>
	figure{
		width: var(--width);
		height: var(--height);

		background: linear-gradient(165.31deg, rgba(67, 151, 141, 0.44) 18.49%, rgba(67, 151, 141, 0) 97.15%);
		box-shadow: 0px 13px 6px 4px rgba(0, 0, 0, 0.25);
		backdrop-filter: blur(12px);
	}
</style>