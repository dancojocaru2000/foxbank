<script>
	export let placeholder;
	export let value;
	export let rows = 2;

	const handleInput = e => {
		value = e.target.value;
	}
</script>

<main>
	<textarea placeholder={placeholder} value={value} rows={rows} on:input={handleInput} class="placeholder-gray-300 p-3 text-gray-50 w-full text-3xl"></textarea>
</main>

<style>
	textarea {
		background: linear-gradient(92.55deg, rgba(76, 172, 135, 0.95) -28.27%, rgba(249, 224, 127, 0.096) 115.79%);
		filter: drop-shadow(0px 8px 4px rgba(0, 0, 0, 0.25));
		border-radius: 3px;
	}

	::-webkit-scrollbar {
		width: 3px;
	}

	/* Track */
	::-webkit-scrollbar-track {
		box-shadow: inset 0 0 2px rgba(141, 140, 140, 0.281); 
		border-radius: 10px;
	}
	
	/* Handle */
	::-webkit-scrollbar-thumb {
		background: rgba(238, 236, 236, 0.897); 
		border-radius: 10px;
	}

	/* Handle on hover */
	::-webkit-scrollbar-thumb:hover {
		background: rgba(182, 182, 182, 0.918); 
	}

	textarea {
		scrollbar-width: thin;
		scrollbar-color: rgba(238, 236, 236, 0.897) rgba(141, 140, 140, 0.281);
	}
</style>

