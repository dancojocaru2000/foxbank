<script>
    import OrangeButton from "./OrangeButton.svelte";

    import CardBG from "./CardBG.svelte";
    import InputField from "./InputField.svelte";
    import {createEventDispatcher} from 'svelte';
    import Icon from "@iconify/svelte";
    import Overlay from "./Overlay.svelte";
    import TextareaField from "./TextareaField.svelte";
    import { fade, fly, slide } from 'svelte/transition';
	import { flip } from 'svelte/animate';

    
    const dispatch = createEventDispatcher();

    export let account={type: "", currency:"", balance:0};
    let receivername="";
    let receiveriban="";
    let amount=0.00;
    let description="";

    let send_details={receivername:"", receiveriban:"", amount:0, description:""};

    function create(){
        if(receivername == "" || receivername == null) {
            alert("Receiver's name field can not be empty!");
        }else if(receiveriban == "" || receiveriban == null){
            alert("Receiver's iBan field can not be empty!");
        }else if (amount > parseFloat(account.balance) ){
            alert("Not enough money in your account!");
        }else if (amount <= 0.00 ){
            alert("Insert a valid amount!");
        }else{
            //TODO Create account with provided details on the server
            send_details={receivername:receivername, receiveriban:receiveriban, amount:amount, description:description}
            dispatch("createPopup",{type:"send_money_success", send_details:{send_details}});
        }
    }

    function cancelSend(){
        dispatch("createPopup",{type:"send_money_cancelled"});
    }


</script>


<div class="h-full flex flex-col justify-center items-center md:items-start" in:fade={{duration:300}} out:fade={{duration:300}}>
    <CardBG padding={false} class="flex flex-col items-stretch md:min-w-full">
        <div class="flex-grow m-3 flex flex-col items-stretch">
            <div class="flex flex-row ">
                <h1 class='inline mt-6 mx-6 mb-1 font-sans text-4xl text-gray-50'>Send money</h1>
                <span class="mb-1 ml-4 mr-2 mt-auto text-2xl text-gray-50"> from</span>
                <span class="mb-1 mt-auto font-sans text-4xl">{account.type}</span>
                <button class="mb-1 ml-auto" on:click={cancelSend}> <Icon icon="akar-icons:cross" color="rgba(249, 250, 251, 1)" width="32" height="32" /> </button>  
            </div>
            <div class="w-full max-w-md self-start border-solid border-gray-50 border mb-3"></div> 
    
            <div class="mx-1 flex-shrink">
                <h2 class='font-sans text-2xl text-gray-50 mb-2 '>Receiver's full name:</h2>
                <InputField placeholder="Mr Foxy Fox" isPassword={false} bind:value={receivername}></InputField>
            </div>
            
            <div class="mx-1 flex-shrink">
                <h2 class='font-sans text-2xl text-gray-50 mb-2 '>IBAN:</h2>
                <InputField placeholder={account.currency +"-0000-0000-0000-0000"} isPassword={false} bind:value={receiveriban}></InputField>
            </div>
    
            <div class="mx-1 flex-shrink">
                <h2 class='font-sans text-2xl text-gray-50 mb-2 '>Amount:</h2>
                <InputField style="color: #264D59" placeholder=0 isPassword={false} bind:value={amount}>
                    <span class="text-gray-50">{account.currency}</span>
                </InputField>
            </div>     
            
            <div class="mx-1 flex-shrink">
                <h2 class='font-sans text-2xl text-gray-50 mb-2 '>Description:</h2>
                <TextareaField class="flex-grow mb-0" placeholder="Sent from FOXBANK!" rows={5} bind:value={description}></TextareaField>
            </div>
        </div>
        
        
        <div class="m-4"></div>

        <div class="flex-shrink flex flex-row mb-4 mt-0" style="background: linear-gradient(89.1deg, rgba(236, 98, 68, 0.95) 0.77%, rgba(236, 98, 68, 0) 99.12%);">
            <div class="flex-1"></div> 
            <OrangeButton class="flex-1 m-4" on:click={create}>Confirm</OrangeButton>
        </div>
        
    </CardBG>
</div>

