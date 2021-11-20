<script>
    import OrangeButton from "./OrangeButton.svelte";

    import CardBG from "./CardBG.svelte";
    import InputField from "./InputField.svelte";
    import {createEventDispatcher} from 'svelte';

    
    const dispatch = createEventDispatcher();

    let username = "";
    let code = "";

    function checkLogin(){
        //todo: CHeck here 
        dispatch("loginSuccess",null);
    }

</script>

<main class="h-full">
    <div class="h-full flex flex-col justify-center items-center md:items-start">
        <CardBG class="flex flex-col items-stretch">
            <h1 class='font-welcome text-7xl text-gray-50 m-6 border-b-2'>Welcome,</h1>
            <div class="m-3 flex-shrink">
                <InputField placeholder="Username" isPassword={false} value={username}></InputField>
            </div>
            
            <div class="m-3 flex-shrink">
                <InputField placeholder="Code" isPassword={true} value={code}></InputField>
            </div>

            <div class="m-3 flex-shrink"> 
                <OrangeButton on:click={checkLogin}>Login</OrangeButton>
            </div>
            
            <div class="flex-grow">
                
            </div>

            <div class="flex">
                    <a href='https://support.google.com/accounts/answer/1066447?hl=ro&co=GENIE.Platform%3DAndroid' target="_blank" class='text-3xl text-gray-400 m-6 flex-auto text-center'>Help!</a>
                    <a href='https://support.google.com/accounts/answer/185834?hl=en' target="_blank" class='text-3xl text-gray-400 m-6 flex-auto text-center'>Can't login?</a>
            </div>
            
        </CardBG>
    </div>
    
</main>