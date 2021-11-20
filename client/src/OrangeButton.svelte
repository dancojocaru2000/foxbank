<script>
import BaseButton from "./BaseButton.svelte";



</script>

<div class="orange">
	<BaseButton on:click>
		<slot></slot>
	</BaseButton>
</div>

<style>
	.orange {
		background: linear-gradient(272.39deg, rgba(247, 175, 67, 0.93) -34.2%, rgba(245, 72, 17, 0.93) 100%);
		box-shadow: 0px 8px 4px rgba(0, 0, 0, 0.25);
		border-radius: 20px;
	}

</style>