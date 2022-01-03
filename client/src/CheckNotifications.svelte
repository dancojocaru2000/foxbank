<script>

    import CardBG from "./CardBG.svelte";
    import {createEventDispatcher, getContext} from 'svelte';
    import Icon from "@iconify/svelte";
    import { fade, fly, slide } from 'svelte/transition';
	import { flip } from 'svelte/animate';
    import DetailField from "./DetailField.svelte";
    import { marknotificationread } from "./api";

    
    const dispatch = createEventDispatcher();
    const notificationsStore = getContext("notifications");
    const refreshNotifications = getContext("refreshNotifications");
    const token = getContext("token");

    $: notifications = $notificationsStore ? $notificationsStore.notifications : [];

    function cancelCheckNotifications(){
        dispatch("createPopup",{type:"check_notifications_cancelled"});
    }

    async function onNotificationClick(id){
        await marknotificationread($token, id);
        if($refreshNotifications){
            $refreshNotifications();
        }
    }

</script>

<div class="h-full self-center">
    <div class="h-full flex flex-col justify-center items-center md:items-start overflow-clip">
        <CardBG class="flex flex-col items-stretch min-h-0">
            <div class="flex flex-row">
                <h1 class='font-sans text-4xl text-gray-50 mt-6 mx-6 mb-1'>Inbox</h1>
                <button class="ml-auto mr-6" on:click={cancelCheckNotifications}> <Icon icon="akar-icons:cross" color="rgba(249, 250, 251, 1)" width="32" height="32" /> </button>  
            </div>
            <div class="w-full max-w-md self-start border-solid border mb-3"></div> 

            <div class="flex flex-col flex-grow pl-8 pr-10 relative scroller overflow-auto overflow-x-hidden max-h-full min-h-0">
                {#if notifications.length > 0}
                    {#each notifications as notification,i (i)}
                        <div on:click={() => onNotificationClick(notification.id)} in:slide={{delay:100*i}} out:slide={{delay:50*(notifications.length-i)}}>
                    
                            <DetailField class="relative my-3 py-1 flex-shrink min-w-transaction max-w-4xl">   
                                <div class='font-sans text-gray-50 text-2xl mt-2 mx-4 border-b-1'>
                                    {notification.body}
                                </div>

                                <div class="flex flex-row"> 
                                    <div class='inline font-sans ml-auto mr-4 text-xl text-gray-100 mt-2 mx-6 border-b-1'>
                                        <span> at {new Date(notification.datetime).toLocaleString()} </span>
                                    </div>
                                </div>

                                <div class='fixed font-sans text-6xl text-gray-100 left-2 bottom-2'>
                                    {#if !notification.read}
                                        <svg class="fill-current text-gray-100" viewBox="0 0 16 16" width="16" height="16">
                                            <circle cx="8" cy="8" r="8"></circle>
                                        </svg>
                                    {:else}
                                        <svg class="fill-current text-gray-100" viewBox="0 0 24 24" width="16" height="16">
                                            <path d="M20.285 2l-11.285 11.567-5.286-5.011-3.714 3.716 9 8.728 15-15.285z"/>
                                        </svg>
                                    {/if}
                                </div>
                                
                            </DetailField> 
                        </div>
                    {/each}
                {:else}
                        <DetailField class="relative my-3 py-1 flex-shrink min-w-transaction max-w-4xl">
                            <div class='font-sans text-gray-50 text-2xl mt-2 mx-4 border-b-1'>
                                No notifications.
                            </div>
                        </DetailField>
                {/if}
                
            </div>
            
            <div class="m-2"></div>
            
        </CardBG>
    </div>
    
</div>

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

.max-h-medium {
    max-height: 50%;
}
</style>