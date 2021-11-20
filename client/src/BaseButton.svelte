<script>
    let clazz = "";
    export { clazz as class };
</script>

<main class={clazz}>
	<button on:click class="rounded-2xl p-6 w-full text-center text-3xl text-gray-50">
		<slot></slot>
	</button>
</main>