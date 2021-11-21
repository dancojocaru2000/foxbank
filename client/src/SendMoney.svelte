<script>
    import OrangeButton from "./OrangeButton.svelte";

    import CardBG from "./CardBG.svelte";
    import InputField from "./InputField.svelte";
    import {createEventDispatcher} from 'svelte';
import Icon from "@iconify/svelte";

    
    const dispatch = createEventDispatcher();

    let type = "";
    let currencies = ["RON", "EUR"];
    let currency = currencies[0];
    let termsAccepted = false;

    function create(){
        if(type == "" || type == null) {
            alert("Account Name field can not be empty!");
            console.debug(`account name: ${type}`)
        }else if(!currencies.includes(currency)){
            alert("Currency is not supported!");
        }else if (!termsAccepted){
            alert("Terms of Service not accepted!");
        }else{
            //TODO Create account with provided details on the server
            dispatch("createPopup",{type:"create_acc_success"});
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

</script>

<div class="h-full self-center">
    <div class="h-full flex flex-col justify-center items-center md:items-start">
        <CardBG class="flex flex-col items-stretch">
            <div class="flex flex-row">
                <h1 class='font-sans text-4xl text-gray-50 mt-6 mx-6 mb-1'>Open a new account</h1>
                <button class="ml-auto mr-6" on:click={cancelCreate}> <Icon icon="akar-icons:cross" color="rgba(249, 250, 251, 1)" width="32" height="32" /> </button>  
            </div>
            <div class="w-full max-w-md self-start border-solid border-gray-50 border mb-3"></div> 
     
            <div class="mx-1 flex-shrink">
                <h2 class='font-sans text-2xl text-gray-50 mb-2 '>Account name:</h2>
                <InputField placeholder="New Account" isPassword={false} bind:value={type}></InputField>
            </div>
            
            <div class="mx-1 flex-shrink">
                <h2 class='font-sans text-2xl text-gray-50 mb-2 '>Currency:</h2>
                <InputField placeholder="RON" isPassword={false} bind:value={currency}></InputField>
            </div>

            <div class="mx-1 flex-shrink  max-w-2xl">
                <h2 class=" font-sans text-2xl text-gray-50 mb-2 ">Terms of Service:</h2>
                <button class="mb-1" on:click={termsOfService}> <Icon icon={termsAccepted ? "akar-icons:check-box" : "akar-icons:box"} color="rgba(249, 250, 251, 1)" width="18" height="18" /> </button>
                <h3 class="inline m-0 mb-0 text-gray-300"> I have read and accepted the <a class="font-sans text-gray-50" href="https://c.tenor.com/TVRtbC8jKY0AAAAC/positive-fox-you-can-do-it.gif" target="_blank">terms and conditions</a> for creating a new account at FOXBANK. </h3>
            </div>
            
            
            <div class="m-10"></div>

            <div class="mx-1 flex-shrink"> 
                <OrangeButton on:click={create}>Confirm</OrangeButton>
            </div>
            
        </CardBG>
    </div>
    
</div>