
<script>
    import Icon from '@iconify/svelte';
    
    import CardBG from "./CardBG.svelte";    
    import DetailField from './DetailField.svelte';
    import GreenButton from './GreenButton.svelte';
    import {createEventDispatcher} from 'svelte';

    const dispatch = createEventDispatcher();


	export let type="RON Account";
	export let currency="RON";
    export let balance="5425";
    export let iban="RONFOX62188921";
    export let isExpanded=false;
    export let transactions=[
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
        {title:"Transaction Name#1", status:"PROCESSED", amount:"-45,09", time:"15:38 27/11/2021", type:"send"},
        {title:"Transaction Name#2", status:"PENDING", amount:"+25,00", time:"15:38 27/11/2021", type:"received"},
        {title:"Transaction Name#3", status:"CANCELLED", amount:"-469,09", time:"15:38 27/11/2021", type:"send"},
        {title:"Transaction Name#4", status:"DECLINED", amount:"+469,09", time:"15:38 27/11/2021", type:"received"},
    ];

    function copyIban(){
        //todo: Code here 
        dispatch("copiedIban",null);
    }

    function expand(){
        //todo: Code here 
        dispatch("expanded",isExpanded);
    }
</script>

<CardBG class="flex-shrink flex flex-col items-stretch md:self-start px-6 pt-6 pb-0 max-h-full overflow-clip min-h-0">
    <div class="flex flex-col flex-shrink">
        <div class='font-sans  mt-2 mx-2 border-b-1'>
            <h3 class="text-gray-50 inline mr-4">{type}</h3>
            <span class="text-gray-100">IBAN: {iban}</span>
            <button on:click={copyIban} class="inline"> <Icon icon="akar-icons:copy" color="rgba(249, 250, 251, 1)"/></button>
        </div>
        
        <div class="w-full max-w-sm self-start border-solid border-gray-50 border mb-2"></div>
    </div>

    <div class="flex flex-row flex-grow max-h-full min-h-0">
        <div class="flex flex-col">

            <div>
                <DetailField class="py-2 mt-4 flex-shrink">
                    <h2 class='font-sans ml-4 text-4xl text-gray-50'>Balance: <span style="color: #264D59">{balance}</span>{currency}</h2>
                </DetailField>
            </div>

            <div class="flex flex-col flex-grow max-h-full relative {isExpanded ? "overflow-auto" : ""}">

                {#if isExpanded }
                    {#each transactions as transaction}
                        <DetailField class="my-3 py-1 flex-shrink">   
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

            <GreenButton class="mx-8">
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