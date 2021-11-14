<script>
import Login from "./Login.svelte";
import MainPage from "./MainPage.svelte";

	let loggedin = false;
	function toggleLoggedIn() {
		loggedin = !loggedin;
	}
</script>

<main class="bg-banner bg-cover bg-center h-screen font-sans">
	{#if loggedin}
		<MainPage></MainPage>
	{:else}
		<Login on:loginSuccess={toggleLoggedIn}></Login>
	{/if}
</main>

<style global lang="postcss">
	
	@import url('https://fonts.googleapis.com/css2?family=Geo&family=Roboto&family=Rochester&display=swap');

	@tailwind base;
	@tailwind components;
	@tailwind utilities;
</style>