<script>
import BottomBorder from "./BottomBorder.svelte";
import CheckNotifications from "./CheckNotifications.svelte";
import CreateAccount from "./CreateAccount.svelte";

import Login from "./Login.svelte";
import MainPage from "./MainPage.svelte";
import TopBorder from "./TopBorder.svelte";

	let loggedin = true;
	function toggleLoggedIn() {
		loggedin = !loggedin;
	}

	let isCreatingAccount = false;
	let isCheckingNotifications = false;
	let isSendingMoney = false;
	let sendingAccount = "";
	let notifications = [];

	function onCreatePopup(event) {
		const eventType = event.detail.type;
		switch (eventType) {
			case "new_account":
				isCreatingAccount = true;
			break;

			case "create_acc_success":
				isCreatingAccount = false;
			break;

			case "create_acc_cancelled":
				isCreatingAccount = false;
			break;

			case "create_acc_failed":
				isCreatingAccount = false;
				alert(`Account creation failed! Reason: ${event.detail.reason}`);
			break;

			case "send_money":
				sendingAccount = event.detail.iban;
				isSendingMoney = true;
			break;

			case "send_money_cancelled":
				isSendingMoney = false;
			break;

			case "send_money_failed":
				isSendingMoney = false;
				alert(`Sending money failed! Reason: ${event.detail.reason}`);
			break;

			case "check_notifications":
				notifications = event.detail.notifications;
				isCheckingNotifications = true;
			break;

			case "check_notifications_cancelled":
				isCheckingNotifications = false;
			break;

			default:
				alert(`Unhandled createPopup event: ${eventType}`);
		}
	}
</script>

<main class="flex flex-col items-stretch bg-banner bg-cover bg-center bg-fixed h-screen font-sans">
	{#if isCreatingAccount}
		<CreateAccount on:createPopup={onCreatePopup}> </CreateAccount>
	{:else if  isCheckingNotifications}
		 <CheckNotifications on:createPopup={onCreatePopup} notifications={notifications}></CheckNotifications>
	{:else if  isSendingMoney}
		 <!-- else if content here -->
	{/if}
	<TopBorder class="flex-shrink"></TopBorder>
	<div class="flex-grow max-h-full overflow-hidden">
		{#if loggedin}
			<MainPage on:logOut={toggleLoggedIn} on:createPopup={onCreatePopup}></MainPage>
		{:else}
			<Login on:loginSuccess={toggleLoggedIn}></Login>
		{/if}
	</div>
	<BottomBorder class="flex-none"></BottomBorder>
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