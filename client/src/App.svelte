<script>
import Login from "./Login.svelte";
import MainPage from "./MainPage.svelte";

	let loggedin = false;
	function toggleLoggedIn() {
		loggedin = !loggedin;
	}
</script>

<main class="bg-banner bg-cover bg-center h-screen">
	<button on:click={toggleLoggedIn}>
		toggle
	</button>
	{#if loggedin}
		<MainPage></MainPage>
	{:else}
		<Login></Login>
	{/if}
</main>

<style global lang="postcss">
	@tailwind base;
	@tailwind components;
	@tailwind utilities;
</style>