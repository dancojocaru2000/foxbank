<script>
	import { onMount, setContext } from "svelte";
	import { writable, readable } from "svelte/store";
	import { whoami, createnotification, getaccountlist, getnotificationlist } from "./api";

	import BottomBorder from "./BottomBorder.svelte";
	import CheckNotifications from "./CheckNotifications.svelte";
	import CreateAccount from "./CreateAccount.svelte";

	import Login from "./Login.svelte";
	import MainPage from "./MainPage.svelte";
	import Overlay from "./Overlay.svelte";
	import SendMoney from "./SendMoney.svelte";
	import TopBorder from "./TopBorder.svelte";

	const userToken = writable(sessionStorage.getItem("token"));
	userToken.subscribe(newToken => {
		sessionStorage.setItem("token", newToken);
	})

	setContext("token", userToken);
	
	const user = readable(null, set => {
		const unsubscribe = userToken.subscribe(token => {
			if(token == null) {
				set(null);
			}else{
				whoami(token) 
					.then(result =>{
						if(result.status != "success") {
							$userToken = null;
						}else {
							set(result);
						}
					})
			}
		})

		return () => {
			unsubscribe();
		}
	})

	setContext("user", user);

	const accounts = readable(null, set => {
		const unsubscribe = userToken.subscribe(token => {
			if(token == null) {
				set(null);
			}else{
				getaccountlist(token) 
					.then(result =>{
						set(result);
					})
			}
		})

		return () => {
			unsubscribe();
		}
	})

	setContext("accounts", accounts);

	const refreshNotifications = writable(null);
	setContext("refreshNotifications", refreshNotifications);

	const notifications = readable(null, set=> {
		function getNotifications(token){
			if(token==null){
				set(null);
			}else{
				getnotificationlist(token)
					.then(result => {
						set(result);
					})
			}
		}

		let token = null;

		refreshNotifications.set( () => {
			getNotifications(token);
		});

		const unsubscribe = userToken.subscribe(newToken => {
			token = newToken;
			getNotifications(token);
		})

		const intervalId = setInterval(() => {
			getNotifications(token);
		}, 10000);

		return () => {
			unsubscribe();
			clearInterval(intervalId);
		}
	})

	setContext("notifications", notifications);

	let isCreatingAccount = false;
	let isCheckingNotifications = false;
	let isSendingMoney = false;
	let sendingAccount = "";

	function onCreatePopup(event) {
		const eventType = event.detail.type;
		switch (eventType) {
			case "new_account":
				isCreatingAccount = true;
			break;

			case "create_acc_success":
				var today = new Date();
				var date = today.getDate()+'/'+(today.getMonth()+1)+'/'+today.getFullYear();
				var time = today.getHours() + ":" + today.getMinutes();
				var body = "The "+ eventType.currency + " account with the name " + eventType.type + " was created succesfully!";

				//add notification about created account
				createnotification(async function() {
					const result = await createnotification($userToken, body, date+time);
					if(result.status == "success") {
						console.log("Succesfully created notification.");
					}else{
                        console.log("Failed to create notification.");
                    }
				})

				isCreatingAccount = false;
			break;

			case "create_acc_cancelled":
				isCreatingAccount = false;
			break;

			case "create_acc_failed":
				// isCreatingAccount = false;
				alert(`Account creation failed! Reason: ${event.detail.reason}`);
			break;

			case "send_money":
				sendingAccount = event.detail.account;
				isSendingMoney = true;
			break;

			case "send_money_cancelled":
				isSendingMoney = false;
			break;

			case "send_money_success":
				isSendingMoney = false;
			break;

			case "check_notifications":
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
	
	<TopBorder class="flex-shrink"></TopBorder>
	<div class="flex-grow max-h-full overflow-hidden">
		{#if $user}
			
			{#if isCreatingAccount}
				<Overlay>
					<div class="flex items-center justify-center h-full">
						<CreateAccount class="" on:createPopup={onCreatePopup}> </CreateAccount>
					</div>
				</Overlay>
			{:else if  isCheckingNotifications}
				<Overlay>
					<div class="flex items-center justify-center h-full">
						<CheckNotifications on:createPopup={onCreatePopup}></CheckNotifications>
					</div>
				</Overlay>
			{:else if  isSendingMoney}
				<Overlay>
					<div class="flex items-center justify-center h-full w-full">
						<SendMoney on:createPopup={onCreatePopup} account={sendingAccount}></SendMoney>
					</div>
				</Overlay>
			{/if}

			<MainPage on:createPopup={onCreatePopup} on:logOut={()=>$userToken=null}></MainPage>

		{:else}
			<Login on:loginSuccess={(e)=> $userToken = e.detail.token}></Login>
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