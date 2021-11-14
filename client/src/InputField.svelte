<script>
	export let isPassword;
	export let placeholder;
	export let value;

	const handleInput = e => {
		value = e.target.value;
	}
</script>

<main>
	<input type={isPassword ? "password" : "text"} placeholder={placeholder} value={value} on:input={handleInput} class="placeholder-gray-300 p-3 text-gray-50 w-full text-3xl">
</main>

<style>
	input{
		background: linear-gradient(92.55deg, rgba(76, 172, 135, 0.95) -28.27%, rgba(249, 224, 127, 0.096) 115.79%);
		filter: drop-shadow(0px 8px 4px rgba(0, 0, 0, 0.25));
		border-radius: 3px;
	}

</style>
