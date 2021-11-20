<script>
import BaseButton from "./BaseButton.svelte";

let clazz = "";
export { clazz as class };

</script>

<div class="green {clazz}">
	<BaseButton on:click>
		<slot></slot>
	</BaseButton>
</div>

<style>
	.green {
		background: linear-gradient(92.55deg, rgba(67, 151, 141, 0.95) -28.27%, rgba(249, 224, 127, 0) 115.79%);
		filter: drop-shadow(0px 8px 4px rgba(0, 0, 0, 0.25));
		border-radius: 16px;
	}

</style>