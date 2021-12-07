<script>
	let clazz = "";
	export {clazz as class}
</script>

<div id="overlay" class="overlay {clazz}">
  <div class="overlay-content">
    <slot></slot>
  </div>
</div>

<style>
	/* The Overlay (background) */
.overlay {
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
  overflow-x: hidden; /* Disable horizontal scroll */
  background: linear-gradient(165.31deg, rgba(67, 151, 141, 0.44) 18.49%, rgba(67, 151, 141, 0) 97.15%);
	backdrop-filter: blur(6px);

  transition: 0.5s; /* 0.5 second transition effect to slide in or slide down the overlay (height or width, depending on reveal) */
}

/* Position the content inside the overlay */
.overlay-content {
  position: relative;
  /* top: 25%; 25% from the top */
  width: 100%; /* 100% width */
  height: 100%;
}

</style>