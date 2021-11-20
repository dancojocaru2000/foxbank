<script>
    import Icon from '@iconify/svelte';
    
    import CardBG from "./CardBG.svelte";
    import {createEventDispatcher} from 'svelte';
import AccountCard from './AccountCard.svelte';
    
    const dispatch = createEventDispatcher();

    let username = "Firstname Lastname";
    let code = "";
    let totalbalance = "2455,22";
    let accountnr = "2";
    let maincurrency = "RON";

    let accounts = [
        {type:"RON Account", currency:"RON", balance:"420,42", iban:"RONFOX62188921", isExpanded: false, 
            transactions: [
                {title:"Transaction Name#1", status:"PROCESSED", amount:"-45,09", time:"15:38 27/11/2021", type:"send"},
                {title:"Transaction Name#2", status:"PENDING", amount:"+25,00", time:"15:38 27/11/2021", type:"received"},
                {title:"Transaction Name#3", status:"CANCELLED", amount:"-469,09", time:"15:38 27/11/2021", type:"send"},
                {title:"Transaction Name#1", status:"PROCESSED", amount:"-45,09", time:"15:38 27/11/2021", type:"send"},
                {title:"Transaction Name#2", status:"PENDING", amount:"+25,00", time:"15:38 27/11/2021", type:"received"},
                {title:"Transaction Name#3", status:"CANCELLED", amount:"-469,09", time:"15:38 27/11/2021", type:"send"},
                {title:"Transaction Name#1", status:"PROCESSED", amount:"-45,09", time:"15:38 27/11/2021", type:"send"},
                {title:"Transaction Name#2", status:"PENDING", amount:"+25,00", time:"15:38 27/11/2021", type:"received"},
                {title:"Transaction Name#3", status:"CANCELLED", amount:"-469,09", time:"15:38 27/11/2021", type:"send"},
                {title:"Transaction Name#1", status:"PROCESSED", amount:"-45,09", time:"15:38 27/11/2021", type:"send"},
                {title:"Transaction Name#2", status:"PENDING", amount:"+25,00", time:"15:38 27/11/2021", type:"received"},
                {title:"Transaction Name#3", status:"CANCELLED", amount:"-469,09", time:"15:38 27/11/2021", type:"send"},
                {title:"Transaction Name#1", status:"PROCESSED", amount:"-45,09", time:"15:38 27/11/2021", type:"send"},
                {title:"Transaction Name#2", status:"PENDING", amount:"+25,00", time:"15:38 27/11/2021", type:"received"},
                {title:"Transaction Name#3", status:"CANCELLED", amount:"-469,09", time:"15:38 27/11/2021", type:"send"},
            ]
        }, 
        {type:"EUR Account", currency:"EUR", balance:"620,42", iban:"EURFOX62188921", isExpanded: false, 
            transactions: [
                {title:"Transaction Name#1", status:"PROCESSED", amount:"-45,09", time:"15:38 27/11/2021", type:"send"},
                {title:"Transaction Name#2", status:"PENDING", amount:"+25,00", time:"15:38 27/11/2021", type:"received"},
                {title:"Transaction Name#3", status:"CANCELLED", amount:"-469,09", time:"15:38 27/11/2021", type:"send"},
            ]
        },
    ];
    let expandedAccount = null;

    function dispatchLogout(){
        //todo: CHeck here 
        dispatch("logOut",null);
    }

    function showNotifications(){
        //todo: CHeck here 
        dispatch("showNotifications",null);
    }

   

    function expanded(index) {
        if (!expandedAccount && expandedAccount !== 0) {
            expandedAccount = index;
        }
        else {
            expandedAccount = null;
        }
    }

</script>

<main class="h-full flex flex-col items-stretch md:flex-row">
    <div class="flex flex-col items-stretch max-h-full">
        {#if expandedAccount || expandedAccount === 0}
            <AccountCard type={accounts[expandedAccount].type} currency={accounts[expandedAccount].currency} balance={accounts[expandedAccount].balance} iban={accounts[expandedAccount].iban} transactions={accounts[expandedAccount].transactions} isExpanded={true} on:expanded={() => expanded(null)}></AccountCard>
        {:else}
            {#each accounts as account,i}
                <AccountCard type={account.type} currency={account.currency} balance={account.balance} iban={account.iban} transactions={account.transactions} isExpanded={false} on:expanded={() => expanded(i)}></AccountCard>
            {/each}
        {/if}
    </div>

    <div class="flex-shrink md:flex-shrink-0 md:flex-grow"></div>

    <CardBG class="flex-shrink flex flex-col items-stretch md:self-start p-6">
        <div class="flex flex-row"> 
            <h1 class='font-sans text-5xl text-gray-50 m-6 border-b-2'>{username}</h1>
            <button on:click={showNotifications} style=" filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));"> <Icon icon="akar-icons:envelope" color="#FB6666" width="36" height="36" /></button>
        </div>
        
        <div class="m-3 flex-shrink">
            <h2 class='font-sans text-4xl text-gray-50'>Total balance: <span style="color: #264D59">{totalbalance}</span>{maincurrency}</h2>
            <p class='font-sans text-1xl text-gray-50 m-2'>➜ from {accountnr} accounts</p>
        </div>
        
        <div class="m-3 flex-shrink">
            <h2 class='font-sans text-4xl text-gray-50'>Total balance: <span style="color: #264D59">{totalbalance}</span>{maincurrency}</h2>
            <p class='font-sans text-1xl text-gray-50 m-2'>➜ from {accountnr} accounts</p>
        </div>

        <div class="m-16"></div>

        <div class="flex flex-row">
                <button on:click={dispatchLogout}> <Icon icon="ri:logout-box-line" color="gray" width="34" height="34"/></button>
                <div class="flex-grow"></div>
                <div class="flex-grow"></div>
                <div class="flex-grow"></div>
                <div class="flex-grow"></div>
                <a href='https://google.com' target="_blank" class='text-3xl text-gray-400 m-6 flex-auto text-center'>Help!</a>
                <a href='mailto:foxbank.fx@gmail.com' target="_blank" class='text-3xl text-gray-400 m-6 flex-auto text-center'>Feedback</a>
        </div>
        
    </CardBG>
    
</main>

