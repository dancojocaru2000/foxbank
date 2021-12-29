<script>
    import OrangeButton from "./OrangeButton.svelte";

    import CardBG from "./CardBG.svelte";
    import InputField from "./InputField.svelte";
    import {createEventDispatcher, onMount} from 'svelte';
    import Icon from "@iconify/svelte";
    import Overlay from "./Overlay.svelte";
    import { fade, fly, slide } from 'svelte/transition';
	import { flip } from 'svelte/animate';
    import { createaccount, getcurrencies, getaccounttypes } from "./api";
    import { getContext } from "svelte";

    const token = getContext("token");
    
    const dispatch = createEventDispatcher();

    let type = null;
    let name = "";
    let currency = null;
    let termsAccepted = false;
    $: placeholder = type==null ? "Checking Account" : `${type} Account`;

    async function create(){
        if(name == "" || name == null) {
            alert("Account Name field can not be empty!");
            console.debug(`account name: ${type}`)
        }else if(type == null){
            alert("Type is not selected!");
        }else if(currency == null){
            alert("Currency is not selected!");
        }else if (!termsAccepted){
            alert("Terms of Service not accepted!");
        }else{
            const result = await createaccount($token, name, currency, type);
            if(result.status == "success") {
                dispatch("createPopup",{type:"create_acc_success", account:{type:type, currency:currency, transactions:[]}});
            }else{
                dispatch("createPopup",{type:"create_acc_failed", reason:"Failed to create account. Error:"+result.status});
            }
        }
    }

    function cancelCreate(){
        dispatch("createPopup",{type:"create_acc_cancelled"});
    }

    function failCreate(){
        dispatch("createPopup",{type:"create_acc_failed", reason:"Invalid arguments. [type: "+type+", currency: "+currency});
    }

    function termsOfService() {
        termsAccepted = !termsAccepted;
    }

    onMount(() => {
        getcurrencies().then(result => currency = result.currencies[0]);
        getaccounttypes().then(result => type = result.accountTypes[0]);
    })

</script>


    <div class="h-full self-center" in:fade={{duration:300}} out:fade={{duration:300}}>
        <div class="h-full flex flex-col justify-center items-center md:items-start">
            <CardBG padding={false} class="flex flex-col items-stretch">
                <div class="m-3">
                    <div class="flex flex-row">
                        <h1 class='font-sans text-4xl text-gray-50 mt-6 mx-6 mb-1'>Open a new account</h1>
                        <button class="ml-auto mr-6" on:click={cancelCreate}> <Icon icon="akar-icons:cross" color="rgba(249, 250, 251, 1)" width="32" height="32" /> </button>  
                    </div>
                    <div class="w-full max-w-md self-start border-solid border-gray-50 border mb-3"></div> 
            
                    <div class="mx-1 flex-shrink">
                        <h2 class='font-sans text-2xl text-gray-50 mb-2 '>Account name:</h2>
                        <InputField placeholder={placeholder} isPassword={false} bind:value={name}></InputField>
                    </div>

                    <div class="mx-1 flex-shrink">
                        <h2 class='font-sans text-2xl text-gray-50 mb-2 '>Type:</h2>
                        <select bind:value={type}>
                            {#await getaccounttypes() then result} 
                                {#each result.accountTypes as option}
                                    <option class="custom-option" value={option}>{option}</option>
                                {/each}	
                            {/await}
                           
                        </select>
                    </div>
                    
                    <div class="mx-1 flex-shrink">
                        <h2 class='font-sans text-2xl text-gray-50 mb-2 '>Currency:</h2>
                        <select bind:value={currency}>
                            {#await getcurrencies() then result} 
                                {#each result.currencies as option}
                                    <option class="custom-option" value={option}>{option}</option>
                                {/each}	
                            {/await}
                           
                        </select>
                    </div>

                    <div class="mx-1 flex-shrink  max-w-2xl">
                        <h2 class=" font-sans text-2xl text-gray-50 mb-2 ">Terms of Service:</h2>
                        <button class="mb-1" on:click={termsOfService}> <Icon icon={termsAccepted ? "akar-icons:check-box" : "akar-icons:box"} color="rgba(249, 250, 251, 1)" width="18" height="18" /> </button>
                        <h3 class="inline m-0 mb-0 text-gray-300"> I have read and accepted the <a class="font-sans text-gray-50" href="https://c.tenor.com/TVRtbC8jKY0AAAAC/positive-fox-you-can-do-it.gif" target="_blank">terms and conditions</a> for creating a new account at FOXBANK. </h3>
                    </div>
                    
                    
                    <div class="m-10"></div>
                </div>

                <div class="flex-shrink flex flex-row mb-4" style="background: linear-gradient(89.1deg, rgba(236, 98, 68, 0.95) 0.77%, rgba(236, 98, 68, 0) 99.12%);">
                    <div class="flex-1"></div> 
                    <OrangeButton class="flex-1 m-4" on:click={create}>Confirm</OrangeButton>
                </div>
                
            </CardBG>
        </div>
        
    </div>


    <style>
        select{
            min-width: 120px;
            min-height: 32px;
            color: rgba(233, 231, 231, 0.842);

            background: linear-gradient(92.55deg, rgba(76, 172, 135, 0.95) -28.27%, rgba(249, 224, 127, 0.096) 115.79%);
            filter: drop-shadow(0px 8px 4px rgba(0, 0, 0, 0.25));
            border-radius: 3px;
        }

        select option{
            min-width: 120px;
            min-height: 32px;
            color: rgba(233, 231, 231, 0.842);

            background: linear-gradient(92.55deg, rgba(76, 172, 135, 0.95) -28.27%, rgba(249, 224, 127, 0.096) 115.79%);
            filter: drop-shadow(0px 8px 4px rgba(0, 0, 0, 0.25));
            border-radius: 3px;
        }

    
    </style>