<script>
import BottomBorder from "./BottomBorder.svelte";

import Login from "./Login.svelte";
import MainPage from "./MainPage.svelte";
import TopBorder from "./TopBorder.svelte";

	let loggedin = false;
	function toggleLoggedIn() {
		loggedin = !loggedin;
	}
</script>

<main class="bg-banner bg-cover bg-center h-screen font-sans">
	<TopBorder></TopBorder>
	<BottomBorder></BottomBorder>
	{#if loggedin}
		<MainPage on:logOut={toggleLoggedIn}></MainPage>
	{:else}
		<Login on:loginSuccess={toggleLoggedIn}></Login>
	{/if}
</main>

<svelte:head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" >
</svelte:head>

<style global lang="postcss">
	
	@import url('https://fonts.googleapis.com/css2?family=Geo&family=Roboto&family=Rochester&display=swap');

	@tailwind base;
	@tailwind components;
	@tailwind utilities;
</style>