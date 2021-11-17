<script>
    import Icon from '@iconify/svelte';
    
    import CardBG from "./CardBG.svelte";
    import {createEventDispatcher} from 'svelte';
    
    const dispatch = createEventDispatcher();

    let username = "Firstname Lastname";
    let code = "";
    let totalbalance = "2455,22";
    let accountnr = "2";
    let maincurrency = "RON"

    function dispatchLogout(){
        //todo: CHeck here 
        dispatch("logOut",null);
    }

    function showNotifications(){
        //todo: CHeck here 
        dispatch("showNotifications",null);
    }

</script>

<main class="h-full flex flex-col items-stretch md:flex-row">
    <div class="flex flex-col items-stretch">
        <CardBG>Item 1</CardBG>
        <CardBG>Item 2</CardBG>
    </div>

    <div class="flex-shrink md:flex-shrink-0 md:flex-grow"></div>

    <CardBG class="flex-shrink flex flex-col items-stretch md:self-start">
        <div class="flex flex-row"> 
            <h1 class='font-sans text-5xl text-gray-50 m-6 border-b-2'>{username}</h1>
            <button on:click={showNotifications} style=" filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));"> <Icon icon="akar-icons:envelope" color="#FB6666" width="64" height="64" /></button>
        </div>
        
        <div class="m-3 flex-shrink">
            <h2 class='font-sans text-4xl text-gray-50'>Total balance: <span style="color: #264D59">{totalbalance}</span>{maincurrency}</h2>
            <p class='font-sans text-1xl text-gray-50 m-2'>➜ from {accountnr} accounts</p>
        </div>
        
        <div class="m-3 flex-shrink">
            <h2 class='font-sans text-4xl text-gray-50'>Total balance: <span style="color: #264D59">{totalbalance}</span>{maincurrency}</h2>
            <p class='font-sans text-1xl text-gray-50 m-2'>➜ from {accountnr} accounts</p>
        </div>
        
        <div class="flex-grow"></div>
        <div class="flex-grow"></div>
        <div class="flex-grow"></div>

        <div class="flex flex-row">
                <button on:click={dispatchLogout}> <Icon icon="ri:logout-box-line" color="gray" width="44" height="44"/></button>
                <div class="flex-grow"></div>
                <div class="flex-grow"></div>
                <div class="flex-grow"></div>
                <div class="flex-grow"></div>
                <a href='https://google.com' class='text-3xl text-gray-400 m-6 flex-auto text-center'>Help!</a>
                <a href='https://google.com' class='text-3xl text-gray-400 m-6 flex-auto text-center'>Feedback</a>
        </div>
        
    </CardBG>
    
</main>

