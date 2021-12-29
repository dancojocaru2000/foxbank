
<script>
    import Icon from '@iconify/svelte';
    
    import CardBG from "./CardBG.svelte";    
    import DetailField from './DetailField.svelte';
    import GreenButton from './GreenButton.svelte';
    import {createEventDispatcher} from 'svelte';
    import { fade, fly, slide } from 'svelte/transition';
	import { flip } from 'svelte/animate';


    const dispatch = createEventDispatcher();


	export let name="RON Account";
	export let currency="RON";
    export let balance="5425";
    export let iban="RONFOX62188921";
    export let isExpanded=false;
    export let transactions=[];

    let copied = false;

    function copyIban(){
        if(!copied){
            navigator.clipboard.writeText(iban)
            .then(() => copied = true)
            .then(() => setTimeout(() => {
                copied = false;
            }, 1000));
        }
    }

    function expand(){
        //todo: Code here 
        dispatch("expanded",isExpanded);
    }

    function send(){
        //todo: CHeck here 
        dispatch("createPopup",{
            type: 'send_money',
            account: {
                type: name,
                currency,
                balance,
                iban,
            }
        });
    }
</script>

 
<CardBG class="flex-shrink flex flex-col items-stretch md:self-start mt-16 mb-6 px-6 pt-6 pb-0 max-h-full overflow-clip min-h-0">
    <div class="flex flex-col flex-shrink">
        <div class='font-sans  mt-2 mx-2 border-b-1'>
            <h3 class="text-gray-50 inline mr-4">{name}</h3>
            <span class="text-gray-100">IBAN: {iban}</span>
            <button on:click={copyIban} class="inline {copied ? "cursor-default" : ""}"> <Icon icon={copied ? "akar-icons:check" : "akar-icons:copy"} color="rgba(249, 250, 251, 1)"/></button>
        </div>
        
        <div class="w-full max-w-sm self-start border-solid border-gray-50 border mb-3"></div>
    </div>

    <div class="flex flex-row flex-grow max-h-full min-h-0">
        <div class="flex flex-col">

            <div>
                <DetailField class="p-1  flex-shrink">
                    <h2 class='font-sans mt-3 mb-2 pl-2 text-4xl text-gray-50'>Balance: <span style="color: #264D59">{balance}</span>{currency}</h2>
                </DetailField>
            </div>

            <div class="flex flex-col flex-grow pr-2 max-h-full relative scroller {isExpanded ? "overflow-auto overflow-x-hidden" : ""}">

                {#if isExpanded }
                    {#each transactions as transaction,i (i)}
                        <div in:slide={{delay:100*i}} out:slide={{delay:50*(transactions.length-i)}}>
                    
                            <DetailField class="my-3 py-1 flex-shrink min-w-transaction">   
                                <div class='font-sans text-gray-50 mt-2 mx-4 border-b-1'>
                                    <h3 class="inline mr-3">{transaction.title}: </h3>
                                    <span class="text-4xl {transaction.type == "send" ?  "text-red-c" : "text-lime-c"}">{transaction.amount}</span>
                                    <span class="text-4xl">{currency}</span>
                                </div>
                                <div class='font-sans text-2xl text-gray-100 mt-2 mx-6 border-b-1'>
                                    <p class="inline">at {transaction.time} </p>

                                    {#if transaction.status == "PROCESSED"}
                                        <span>
                                            <Icon class="inline mb-1" icon="akar-icons:circle-check" color="#6DE25ACC"/>
                                        </span>
                                    {:else if  transaction.status == "PENDING"}
                                        <span>
                                            <Icon class="inline mb-1" icon="akar-icons:arrow-cycle" color="#F6AF43"/>
                                        </span>
                                    {:else if  transaction.status == "CANCELLED"}
                                        <span>
                                            <Icon class="inline mb-1" icon="akar-icons:circle-x" color="#F7630C"/>
                                        </span>
                                    {:else}
                                        <span>
                                            <Icon class="inline mb-1" icon="akar-icons:triangle-alert" color="#F7630C"/>
                                        </span>
                                    {/if}
                                    {transaction.status}
                                    
                                </div>
                            </DetailField> 
                        </div>
                    {/each}
                    
                {:else if transactions.length > 0}
                    <DetailField class="my-3 py-2  flex-shrink min-w-transaction">   
                        <div class='font-sans text-gray-50 mt-2 mx-4 border-b-1'>
                            <h3 class="inline mr-3">{transactions[0].title}: </h3>
                            <span class="text-4xl {transactions[0].type == "send" ?  "text-red-c" : "text-lime-c"}">{transactions[0].amount}</span>
                            <span class="text-4xl">{currency}</span>
                        </div>
                        <div class='font-sans text-2xl text-gray-100 mt-2 mx-6 border-b-1'>
                        <p class="inline">at {transactions[0].time} </p>

                            {#if transactions[0].status == "PROCESSED"}
                                <span>
                                    <Icon class="inline mb-1" icon="akar-icons:circle-check" color="#6DE25ACC"/>
                                </span>
                            {:else if  transactions[0].status == "PENDING"}
                                <span>
                                    <Icon class="inline mb-1" icon="akar-icons:arrow-cycle" color="#F6AF43"/>
                                </span>
                            {:else if  transactions[0].status == "CANCELLED"}
                                <span>
                                    <Icon class="inline mb-1" icon="akar-icons:circle-x" color="#F7630C"/>
                                </span>
                            {:else}
                                <span>
                                    <Icon class="inline mb-1" icon="akar-icons:triangle-alert" color="#F7630C"/>
                                </span>
                            {/if}
                            {transactions[0].status}
                            
                        </div>
                    </DetailField>
                {:else}
                    <DetailField class="my-3 py-2  flex-shrink min-w-transaction">
                        <div class='font-sans text-gray-200 mt-2 mx-4 border-b-1'>
                            <h3 class="inline mr-3">No transactions made on this account.</h3>            
                        </div>

                    </DetailField>
                {/if}


                
            </div>

        </div>

        <div class="flex flex-col flex-shrink">

            <GreenButton on:click={send} class="mx-8">
                <Icon class="inline" icon="akar-icons:arrow-right" color="rgba(249, 250, 251, 1)"/>
                send money
            </GreenButton>
            
        </div>
        
    </div>

    <div class="self-center p-2">
        {#if transactions.length > 1}
            {#if isExpanded == false }
                <button on:click={expand}><Icon icon="akar-icons:chevron-down" color="rgba(249, 250, 251, 1)"/></button>
            {:else}
                <button on:click={expand}><Icon icon="akar-icons:chevron-up" color="rgba(249, 250, 251, 1)"/></button>
            {/if}
        {/if}
    </div>
    
</CardBG>


<style>
    /* width */
::-webkit-scrollbar {
  width: 3px;
}

/* Track */
::-webkit-scrollbar-track {
  box-shadow: inset 0 0 2px rgba(141, 140, 140, 0.281); 
  border-radius: 10px;
}
 
/* Handle */
::-webkit-scrollbar-thumb {
  background: rgba(238, 236, 236, 0.897); 
  border-radius: 10px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: rgba(182, 182, 182, 0.918); 
}

.scroller {
  scrollbar-width: thin;
  scrollbar-color: rgba(238, 236, 236, 0.897) rgba(141, 140, 140, 0.281);
}
</style>